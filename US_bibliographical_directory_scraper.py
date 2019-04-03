from bs4 import BeautifulSoup
import requests
import pandas as pd


def find_politicians(congress):
    """
    scrapes the Bibliographical Directory of the US Congress and returns a DataFrame with politicians'
    serving in that Congress.

    :param congress: congress number (e.g. 114)
    :return: DataFrame with all politicians that participated in the given Congress
    """
    soup = BeautifulSoup(
        requests.post('http://bioguide.congress.gov/biosearch/biosearch1.asp', data={'congress': congress}).text,
        features="lxml")

    politicians_dict = []  # stores politicians information
    rows = soup('table')[1].findAll('tr')[1:]

    for idx, row in enumerate(rows):
        if row.findAll('td')[0].string == ' ':
            # this exception takes care of rows with missing member-name and birth-death information
            # this could happen if the politician has served in two roles during the same Congress (e.g.
            # representative and speaker of the House)
            # if this exception realises, we copy some information from the row above.

            prev_row = rows[idx - 1]

            politician = prev_row.findAll('td')[0].a.string.lower()
            surname = prev_row.findAll('td')[0].a.string.split(',')[0].lower()
            name = prev_row.findAll('td')[0].a.string.split(', ')[1].lower()
            year_of_birth = prev_row.findAll('td')[1].string.split('-')[0]
            year_of_death = prev_row.findAll('td')[1].string.split('-')[1]
            position = row.findAll('td')[2].string.lower()
            party = row.findAll('td')[3].string.lower()
            state = row.findAll('td')[4].string.upper()
            congress = row.findAll('td')[5].contents[0]

        else:
            politician = row.findAll('td')[0].a.string.lower()
            surname = row.findAll('td')[0].a.string.split(',')[0].lower()
            name = row.findAll('td')[0].a.string.split(', ')[1].lower()
            year_of_birth = row.findAll('td')[1].string.split('-')[0]
            year_of_death = row.findAll('td')[1].string.split('-')[1]
            position = row.findAll('td')[2].string.lower()
            party = row.findAll('td')[3].string.lower()
            state = row.findAll('td')[4].string.upper()
            congress = row.findAll('td')[5].contents[0]


        politicians_dict.append({
            "politician": politician,
            "surname": surname,
            "name": name,
            "year_of_birth": year_of_birth,
            "year_of_death": year_of_death,
            "position": position,
            "party": party,
            "state": state,
            "congress": congress})

    return pd.DataFrame(politicians_dict)

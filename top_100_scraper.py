# TODO: move this to ./services/

import requests
import pandas as pd
from pandas.io import sql
from bs4 import BeautifulSoup
from datetime import date
import db


BASE_URL = 'https://www.beatport.com/'


def grab_top_100():

    top_100_page = requests.get(BASE_URL + 'top-100')
    top_100_soup = BeautifulSoup(top_100_page.text, 'html.parser')

    # Grab list items on page that are tracks
    top_100_tracks = [item for item in top_100_soup.find_all(
        'li') if item.get('data-ec-creative')]

    # Grab links to song details from each item
    top_100_links = [link.get('href') for item in top_100_tracks for link in item.find_all(
        'a') if link.get('href')[:7] == '/track/']

    # For each track, grab relevant info
    top_100_details = []
    rank = 1
    for link in top_100_links:
        song_details_page = requests.get(BASE_URL + link)
        song_details_soup = BeautifulSoup(
            song_details_page.text, 'html.parser')

        song_details_dict = {'Rank': rank}
        rank += 1

        for x in song_details_soup.find_all('div'):
            if x.get('class') and x.get('class')[0] == 'interior-track-actions':
                song_details_dict['Track_ID'] = x.get('data-ec-id')

        for x in song_details_soup.find_all('li'):
            if x.get('class') and x.get('class')[0] == 'interior-track-content-item':
                # Do this instead of unpacking to prevent error with multiple genres
                category_and_value = x.find_all('span')
                category_tag = category_and_value[0]
                value_tag = category_and_value[1]
                category = category_tag.contents[0]
                value = value_tag.a.contents[0] if category == 'Genre' or category == 'Label' else value_tag.contents[0]
                # Populate dictionary of relevant song details
                song_details_dict[category] = value

        song_details_dict['Date'] = date.today().strftime(
            "%Y-%m-%d")  # Include date when grabbed
        top_100_details.append(song_details_dict)

    return top_100_details


def append_song_details(top_100_details):
    # Convert this to pandas dataframe and append to file
    df = pd.DataFrame(top_100_details)
    song_details_df = pd.read_csv('./datasets/top_100_details_test.csv')
    song_details_df = song_details_df.append(df)
    song_details_df.to_csv('./datasets/top_100_details_test.csv', index=False)


# read/write pandas dataframe using a mysql database in addition to csv file
def append_to_db(top_100_details=None, init_from_csv=False):

    print('appending to db')
    db_connection = db.get_connection()
    try:
        if init_from_csv:
            song_details_df = pd.read_csv('./datasets/top_100_details_test.csv')
            song_details_df.to_sql(con=db_connection,
                                   name="song_details", if_exists="replace")

        # Append new top 100 songs
        if top_100_details:
            top_100_df = pd.DataFrame(top_100_details)
            top_100_df.to_sql(con=db_connection,
                              name="song_details", if_exists="append")
    finally:
        db_connection.close()


if __name__ == "__main__":
    top_100_details = grab_top_100()

    # TODO: decide if you want to recreate the entire dataframe and write it or just append.
    # The first might be slower and more complex but the latter will cause indices to always be 0-99

    # Recreate entire dataframe from csv. Doing this for now until it's in a web app or dataset is too large
    append_song_details(top_100_details)
    append_to_db(top_100_details=None, init_from_csv=True)

    # Only append new top 100 songs to db
    # append_to_db(top_100_details=top_100_details, init_from_csv=False)

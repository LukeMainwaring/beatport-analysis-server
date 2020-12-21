import os

from flask import Flask
app = Flask(__name__)

from top_100_scraper import append_to_db, grab_top_100, append_song_details

# Routes
@app.route('/')
def hello_world():
    return 'Hello, World!'



# TODO: get all data
@app.route('/api/allData')
def get_all_data():
    return 'getting all data'

# TODO: scrape top 100
@app.route('/api/scrapeTop100')
def scrape_top_100():
    top_100_details = grab_top_100()
    append_song_details(top_100_details)
    append_to_db(top_100_details=None, init_from_csv=True)
    return 'scraping top 100'


# TODO: endpoints to grab specific data if helpful
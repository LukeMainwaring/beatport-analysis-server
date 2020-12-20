import os

from flask import Flask
app = Flask(__name__)

from db import db_connection


# Routes
@app.route('/')
def hello_world():
    return 'Hello, World!'



# TODO: get all data
@app.route('/api/allData')
def get_all_data():
    print(db_connection)
    return 'getting all data'

# TODO: scrape top 100
@app.route('/api/scrapeTop100')
def scrape_top_100():
    return 'scraping top 100'


# TODO: endpoints to grab specific data if helpful
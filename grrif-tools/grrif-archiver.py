### [ GRRIF Archiver || Made by Julien 'fetzu' Bono || Scrapes and saves GRRIF's "recently played" items. ]
## [ CLI is cooler with docopt ]
"""
Usage: grrif-archiver.py [-pst]
  
  Options:
    -h --help
    -p                Outputs the data to stdout.
    -s                Saves the data in a SQLite database.
    -t                Saves the data as text in a YYYY/MM/DD.txt structure.
"""

## [ IMPORTS ]
import os
import requests
import titlecase
from datetime import timedelta, date
from bs4 import BeautifulSoup
from docopt import docopt

# Initializing docopt
if __name__ == '__main__':
    arguments = docopt(__doc__)

# If argument -s was used, import sqlite3 and create/open the db
if arguments['-s'] is True:
    import sqlite3

    # Create an emtpy db if it does not exist yet
    if not os.path.isfile('grrif_data.db'):
        # Create the 'plays' table
        conn = sqlite3.connect('grrif_data.db')
        conn.execute('''CREATE TABLE plays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            time TIME NOT NULL,
            artist TEXT NOT NULL,
            title TEXT NOT NULL
        )''')
        conn.commit()
    else:
        conn = sqlite3.connect('grrif_data.db')
    
    c = conn.cursor()

## [ CONFIGURATION ]
# Set the base URL and the date range to scrape data for
base_url = 'https://www.grrif.ch/recherche-de-titres/?date={}'
start_date = date(2021, 1, 1)
end_date = date(2021, 1, 1)

## [ MAIN LOOP ]
# Loop through the dates and scrape the data for each day
current_date = start_date
while current_date <= end_date:
    # Construct the URL for the current date
    URL = base_url.format(current_date.strftime('%Y-%m-%d'))

    # Send a request to the server and get the response
    response = requests.get(URL)

    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the section of the page containing the data
    data_section = soup.find('div', {'class': 'listing-search-titres'})
    #print(data_section)

    # Find all the data items
    data_items = data_section.find_all('article')
    #print(data_items)

    # Extract the data from each item
    for item in data_items:
        time = item.find('div', {'class': 'hours'}).text.strip()
        artist = item.find('div', {'class': 'artist'}).text.strip()
        title = item.find('div', {'class': 'title'}).text.strip()

        # Prettify the data
        #pretty_time = time
        pretty_artist = titlecase.titlecase(artist)
        pretty_title = titlecase.titlecase(title)

        # Print if -p was used
        if arguments['-p'] is True:
            print(f'{pretty_artist} - {pretty_title} (@{time} on {current_date})')
    
        # Save into a text file

        # Save into the database
        if arguments['-s'] is True:
            c.execute('INSERT INTO plays (date, time, artist, title) VALUES (?, ?, ?, ?)', (current_date.strftime('%Y-%m-%d'), time, pretty_artist, pretty_title))
            conn.commit()

    # Move to the next day
    current_date += timedelta(days=1)

# When all is over, close the connection to the DB if necessary
if arguments['-s'] is True:
    conn.close()
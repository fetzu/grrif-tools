### [ GRRIF Archiver || Made by Julien 'fetzu' Bono || Scrapes and saves GRRIF's "recently played" items. ]

## [ IMPORTS ]
import os
import requests
import titlecase
from datetime import timedelta
from bs4 import BeautifulSoup
import sqlite3

def plays_to_db(BASE_URL, START_DATE, END_DATE):
    database_path = database_handler()
    write_to_db(BASE_URL, START_DATE, END_DATE, database_path)

def database_handler():
    ''' 
    Function to check if the  SQLite database
    with a "plays" table containing the plays exists,
    create it if it doesn't...
    '''
    database_path = os.path.join(os.path.abspath(os.getcwd()), "data", "grrif_data.db")

    # Creates the ../data/ directory if it does not exist yet
    if not os.path.isdir(os.path.dirname(database_path)):
        os.makedirs(os.path.dirname(database_path))

    # Create an emtpy db if it does not exist yet
    if not os.path.isfile(database_path):
        # Create the 'plays' table
        conn = sqlite3.connect(database_path)
        conn.execute('''CREATE TABLE plays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            time TIME NOT NULL,
            artist TEXT NOT NULL,
            title TEXT NOT NULL,
            CONSTRAINT unique_play UNIQUE (date, time)
            );
        ''')

        conn.commit()
        conn.close()
    else:
        pass

    return database_path

def write_to_db(base_url, start_date, end_date, database_path):
    '''
    Function to scrape the website between start_date and end_date
    and write all the plays to a database
    '''
    # Connect to the DB
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    # Main loop
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

        # Find all the data items
        data_items = data_section.find_all('article')

        # Extract the data from each item
        for item in data_items:
            time = item.find('div', {'class': 'hours'}).text.strip()
            artist = item.find('div', {'class': 'artist'}).text.strip()
            title = item.find('div', {'class': 'title'}).text.strip()

            # Prettify the data
            pretty_artist = titlecase.titlecase(artist)
            pretty_title = titlecase.titlecase(title)
        
            # Save into the database
            # Make sure that the entries are not already present
            try:
                c.execute('INSERT INTO plays (date, time, artist, title) VALUES (?, ?, ?, ?)', (current_date.strftime('%Y-%m-%d'), time, pretty_artist, pretty_title))
                conn.commit()
            except sqlite3.IntegrityError:
                #print("Error: row already exists")
                continue
        
        # Move to the next day
        current_date += timedelta(days=1)

    # When all is over, close the connection to the DB
    conn.close()

def plays_to_txt(base_url, start_date, end_date):
    '''
    Function to scrape the website between start_date and end_date
    and write all the plays to text files in a YYYY/MM/DD.txt structure
    '''
    # Set the path for the files and creates the ../data/plays directory if it does not exist yet
    plays_path = os.path.join(os.path.abspath(os.getcwd()), "data", "plays")
    os.makedirs(os.path.join(os.path.abspath(os.getcwd()), "data", "plays"), exist_ok=True)

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

        # Find all the data items
        data_items = data_section.find_all('article')

        # Extract the data from each item
        for item in reversed(data_items):
            time = item.find('div', {'class': 'hours'}).text.strip()
            artist = item.find('div', {'class': 'artist'}).text.strip()
            title = item.find('div', {'class': 'title'}).text.strip()

            # Prettify the data
            pretty_artist = titlecase.titlecase(artist)
            pretty_title = titlecase.titlecase(title)
        
            # Creates the a /YYYY/MM/ structure as needed within the ../data/plays directory
            dirtree = os.path.join(plays_path, current_date.strftime('%Y'), current_date.strftime('%m'))
            os.makedirs(dirtree, exist_ok=True)

            # Format and write the data to a DD.txt file
            formatteddata = f'{pretty_artist} - {pretty_title} (@{time})'
            currentfile = os.path.join(dirtree, f'{current_date.strftime("%d")}.txt')
            with open(currentfile, 'a') as f:
                f.write(formatteddata)
                f.write('\n')
        
        # Move to the next day
        current_date += timedelta(days=1)

def plays_to_stdout(base_url, start_date, end_date):
    '''
    Function to scrape the website between start_date and end_date
    and output the data to stdout
    '''
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

        # Find all the data items
        data_items = data_section.find_all('article')

        # Extract the data from each item
        for item in reversed(data_items):
            time = item.find('div', {'class': 'hours'}).text.strip()
            artist = item.find('div', {'class': 'artist'}).text.strip()
            title = item.find('div', {'class': 'title'}).text.strip()

            # Prettify the data
            pretty_artist = titlecase.titlecase(artist)
            pretty_title = titlecase.titlecase(title)
        
            # Print the data to stdout
            print(f'{pretty_artist} - {pretty_title} (@{time} on {current_date})')
        
        # Move to the next day
        current_date += timedelta(days=1)
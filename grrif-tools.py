### [ GRRIF Tools by Julien 'fetzu' Bono ]
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
from datetime import date
from docopt import docopt

# Initializing docopt
if __name__ == '__main__':
    arguments = docopt(__doc__)

## [ CONFIGURATION ]
# Set the base URL and the date range to scrape data for
BASE_URL = 'https://www.grrif.ch/recherche-de-titres/?date={}'
START_DATE = date(2021, 1, 1)
END_DATE = date(2021, 1, 1)

## [ MAIN ]
# The "save to SQLite database" option was chosen
if arguments['-s'] is True:
    # Import the necessary functions
    from grrif_tools.grrif_archiver import plays_to_db

    # Create/open the database
    plays_to_db(BASE_URL, START_DATE, END_DATE)

# The "save to text files" option was chosen
if arguments['-t'] is True:
    # Import the necessary functions
    from grrif_tools.grrif_archiver import plays_to_txt

    # Create/open the database
    plays_to_txt(BASE_URL, START_DATE, END_DATE)

# The "output data to stdout" option was chosen
if arguments['-p'] is True:
    # Import the necessary functions
    from grrif_tools.grrif_archiver import plays_to_stdout

    # Create/open the database
    plays_to_stdout(BASE_URL, START_DATE, END_DATE)
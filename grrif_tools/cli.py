### [ GRRIF Tools by Julien 'fetzu' Bono ]
## [ IMPORTS ]
import sys
import argparse
from datetime import date, datetime

## [ CONFIGURATION ]
__version__ = "0.0.0"

## [ Is CLI even cooler with argparse? ]
parser = argparse.ArgumentParser(
    description='A set of tools for Cool Cats™. Allows you to archive GRRIF\'s play history and scrobble it to last.fm (upcoming).'
)

subparsers = parser.add_subparsers(dest='subcommand')

archive_parser = subparsers.add_parser(
    'archive',
    help='Archive GRRIF\'s play history.'
)
archive_parser.add_argument(
    'destination',
    choices=['print', 'db', 'txt'],
    help='Specify where to archive the play history (print to stdout, save to SQLite database or to text in YYYY/MM/DD.txt file(s)).',
)
archive_parser.add_argument(
    'from_date',
    nargs='?',
    default='2021-01-01',
    help='Specify the start date for the archive in YYYY-MM-DD format. Defaults to 2021-01-01.',
)
archive_parser.add_argument(
    'to_date',
    nargs='?',
    default=date.today().strftime('%Y-%m-%d'),
    help=f"Specify the start date for the archive in YYYY-MM-DD format. Defaults to today ({date.today().strftime('%Y-%m-%d')})",
)

scrobble_parser = subparsers.add_parser(
    'scrobble',
    help='Scrobble to Last.fm.',
)
scrobble_parser.add_argument(
    'from_date',
    nargs='?',
    default='2021-01-01',
    help='Specify the start date for the archive in YYYY-MM-DD format. Defaults to 2021-01-01.',
)
scrobble_parser.add_argument(
    'to_date',
    nargs='?',
    default=date.today().strftime('%Y-%m-%d'),
    help=f"Specify the start date for the archive in YYYY-MM-DD format. Defaults to today ({date.today().strftime('%Y-%m-%d')})",
)

args = parser.parse_args()

## [ MAIN ]
def main():
    print('##########################################\n'
          f'##### [ GRRIF Tools version {__version__} ] ######\n'
          '##########################################\n')

    # Displays argparse's help message if no arguments are given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # Set the base URL to scrape data from
    BASE_URL = 'https://www.grrif.ch/recherche-de-titres/?date={}'

    # Set the date range to scrape data for
    START_DATE = datetime.strptime(args.from_date, '%Y-%m-%d')
    END_DATE = datetime.strptime(args.to_date, '%Y-%m-%d')

    # Archive was passed !
    if args.subcommand == 'archive':
        # The "save to SQLite database" option was chosen
        if args.destination == 'db':
            # Import the necessary functions
            from .grrif_archiver import plays_to_db

            # Create/open the database
            plays_to_db(BASE_URL, START_DATE, END_DATE)

        # The "save to text files" option was chosen
        if args.destination == 'txt':
            # Import the necessary functions
            from .grrif_archiver import plays_to_txt

            # Create/open the database
            plays_to_txt(BASE_URL, START_DATE, END_DATE)

        # The "output data to stdout" option was chosen
        if args.destination == 'print':
            # Import the necessary functions
            from .grrif_archiver import plays_to_stdout

            # Create/open the database
            plays_to_stdout(BASE_URL, START_DATE, END_DATE)

    # Scrobble was passed !
    if args.subcommand == 'scrobble':
        print("Uh-oh, this doesn't exist yet!")

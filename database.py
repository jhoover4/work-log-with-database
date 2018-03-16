import os
import re
import csv
from datetime import datetime

from entry import Entry


class Database:

    def __init__(self, database_name='work_entries'):
        self.database_name = database_name + '.csv'
        self.database_file_path = os.path.dirname(os.path.realpath(__file__)) + self.database_name

    def create_database(self):
        """Creates csv if it doesn't already exist."""

        if not os.path.exists(self.database_file_path):
            open(self.database_name, 'a').close()

    def read_database(self):
        """Opens up data to be worked with."""

        entries = []

        with open(self.database_name) as f:
            data = csv.DictReader(f)

            for row in data:
                entry_data = dict()

                entry_data['Date'] = row['Date']
                entry_data['Title'] = row['Title']
                entry_data['Time Spent'] = row['Time Spent']
                entry_data['Notes'] = row['Notes']

                entries.append(entry_data)

        return entries

    def add_entry(self, entry):
        """Takes one entry."""

        with open(self.database_name, 'a') as f:
            fieldnames = entry.fields
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if os.stat(self.database_name).st_size == 0:
                writer.writeheader()

            writer.writerow(entry.to_dict())


class Search(Database):

    def __init__(self):
        """Initially reads csv so we don't have to repeatedly search for entries"""

        super().__init__()
        self.entries = self.read_database()

    def exact_date(self, date):
        """Finds entry from an exact date search and returns a list of matching objects."""

        entries_found = []

        for data in self.entries:
            if date in data['Date']:
                entries_found.append(Entry.from_dict(data))

        return entries_found

    def range_of_dates(self, start_date, end_date):
        """Finds entry from a ranged date search and returns a list of matching objects."""

        start_date = datetime.strptime(start_date, "%m/%d/%Y")
        end_date = datetime.strptime(end_date, "%m/%d/%Y")

        entries_found = []

        for data in self.entries:
            data_date = datetime.strptime(data['Date'], "%m/%d/%Y")

            if data_date >= start_date and data_date <= end_date:
                entries_found.append(Entry.from_dict(data))

        return entries_found

    def exact_search(self, search_term):
        """Finds entry from an exact title or notes search and returns a list of matching objects."""

        entries_found = []

        for data in self.entries:
            if search_term.lower() in data['Title'].lower() or search_term.lower() in data['Notes'].lower():
                entries_found.append(Entry.from_dict(data))

        return entries_found

    def regex_pattern(self, pattern):
        """Finds entry from a regex title search and returns a list of matching objects."""

        entries_found = []

        for data in self.entries:
            if re.search(pattern, data['Title']) or re.search(pattern, data['Notes']):
                entries_found.append(Entry.from_dict(data))

        return entries_found

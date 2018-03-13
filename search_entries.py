import re
import csv
from datetime import datetime


from write_entries import Entry


class Search:

    def __init__(self):
        """Initially reads csv so we don't have to repeatedly search for entries"""

        self.entries = []

        with open('work_entries.csv') as f:
            data = csv.DictReader(f)

            for row in data:
                entry_data = dict()

                entry_data['Date'] = row['Date']
                entry_data['Title'] = row['Title']
                entry_data['Time Spent'] = row['Time Spent']
                entry_data['Notes'] = row['Notes']

                self.entries.append(entry_data)

    def exact_date(self, date):
        """
        Finds entry from an exact date search and returns a list of matching objects

        """

        entries_found = []

        for data in self.entries:
            if date in data['Date']:
                entries_found.append(Entry.from_dict(data))

        return entries_found

    def range_of_dates(self):
        """
        Finds entry from a ranged date search and returns a list of matching objects

        """

        # TODO: use delta to get difference between dates

        base = datetime.datetime.today()
        date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays)]

    def exact_search(self, search_term):
        """
        Finds entry from an exact title search and returns a list of matching objects

        """

        entries_found = []

        for data in self.entries:
            if search_term in data['Title']:
                entries_found.append(Entry.from_dict(data))

        return entries_found

    def regex_pattern(self, pattern):
        """
        Finds entry from a regex title search and returns a list of matching objects

        """

        entries_found = []

        for data in self.entries:
            if re.search(pattern, data['Title']):
                entries_found.append(Entry.from_dict(data))

        return entries_found
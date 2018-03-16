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

        # TODO: Need to be able to choose from list of found entries

        # When
        # finding
        # by
        # date, I
        # should
        # be
        # presented
        # with a list of dates with entries and be able to choose one to see entries from .

        entries_found = []

        for data in self.entries:
            if date in data['Date']:
                entries_found.append(Entry.from_dict(data))

        return entries_found

    def range_of_dates(self):
        """
        Finds entry from a ranged date search and returns a list of matching objects

        """

        # TODO: Need to be able to choose from list of found entries
        # TODO: use delta to get difference between dates

        base = datetime.datetime.today()
        date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays)]

    def exact_search(self, search_term):
        """
        Finds entry from an exact title or notes and returns a list of matching objects

        """

        entries_found = []

        for data in self.entries:
            if search_term in data['Title']:
                entries_found.append(Entry.from_dict(data))

        # TODO: add search in notes

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

    def search_list(self, selected_entries):
        """User UI to search a set of entries"""

        if not selected_entries:
            # if list is empty
            print("There are no entries matching your search")

            return
        text = "Please select a work entry.\n"
        i = 1
        for entry in selected_entries:
            text += str(i) + ") " + entry.title + "\n"
            i += 1

        print(text)
        user_input = input("\n> ")

        if user_input.lower() == "q":
            return

        a = [str(x) for x in range(len(selected_entries) + 1)]

        while user_input not in a:
            print("Not a valid entry. Please enter a number or press 'q' to quit ")
            user_input = input("\n> ")

            if user_input.lower() == "q":
                return

        return selected_entries[int(user_input) - 1]

    def page_entry(self, entries):
        """Prints an entry object for user"""

        for entry in entries:
            prompt = "Page through returned entries.\n\n"
            prompt += self.display_entry(entry)
            prompt += "(p)revious entry\n"
            prompt += "(n)ext entry\n"

            user_input = input(prompt)

            while user_input.lower() not in ['p', 'n']:
                print("Please enter valid input\n")
                user_input = input(prompt)

        return text

    def display_entry(self, entry):
        """Prints an entry object for user"""

        text = ""

        a = entry.to_dict()

        for key, value in entry.to_dict().items():
            text += key + " : " + value + "\n"

        return text

class Modify_Entries():
    """Entries need to be able to be added, deleted and edited"""

    def __init__(self):
        search = Search()

        self.all_entries = search.entries

    @staticmethod
    def add_entries(entries):
        """Takes a list of Entry objects"""

        with open('work_entries.csv', 'a') as f:

            fieldnames = entries[0].fields

            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()

            if len(entries) == 0:
                # if we only have one entry a different method needs to be used
                writer.writerow(entries.to_dict())
            else:
                entry_list = []

                for entry in entries:
                    entry_list.append(entry.to_dict())

                writer.writerows(entry_list)

    def del_entry(self, entry, title):
        """Takes one entry. Can take more if needed"""

        for entry in self.all_entries:
            if entry.title == title:
                del entry

        Modify_Entries.add_entries(self.all_entries)

    def edit_entry(self, entry, title):
        """Takes one entry. Can take more if needed"""

        for entry in self.all_entries:
            if entry.title == title:
                del entry

    def set_index(self):

        return len(self.all_entries)
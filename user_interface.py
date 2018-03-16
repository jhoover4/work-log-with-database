import os
from datetime import datetime


from entry import Entry
from database import Search


class InterfaceHelpers:

    def __init__(self, database):
        self.database = database

    @staticmethod
    def clear():
        """Clears screen for user."""

        os.system('cls' if os.name == 'nt' else 'clear')

    def add_task(self):
        """For adding new tasks to the csv file.
        Must have a date, title, time spent, and optional body text.
        """

        # task date
        self.clear()
        task_date = input("Date of the task (Please use DD/MM/YYYY): \n")

        while not Entry.date_check(task_date):
            self.clear()
            print("Error: {} doesn't seem to be a valid date.\n\n".format(task_date))

            task_date = input("Please use DD/MM/YYYY: \n")

        # task title
        self.clear()
        task_title = input("Title of the task: \n")

        # task time spent
        self.clear()
        time_spent = input("Time spent (integer of rounded minutes): \n")
        while not Entry.time_check(time_spent):
            self.clear()
            time_spent = input("Please use a valid number of minutes: \n")

        # task notes
        self.clear()
        notes = input("Notes (Optional, you can leave this empty): \n")

        new_entry = Entry(task_date, task_title, time_spent, notes)

        self.database.add_entries([new_entry])

        self.clear()
        input("The entry has been added! Press any key to return to the menu\n")

    def search_task(self):
        """For searching tasks from the csv file.
        Must have a date, title, time spent, and optional body text"""

        search_ui_input = ['a', 'b', 'c', 'd', 'e', 'q']

        while True:
            self.clear()

            prompt = "Do you want to search by:\n\n"
            prompt += "a) Exact Date\n"
            prompt += "b) Range of Dates\n"
            prompt += "c) Exact Search\n"
            prompt += "d) Regex Pattern\n"
            prompt += "e) Return to Menu\n\n"
            prompt += "> "

            user_input = str(input(prompt)).strip()

            while user_input not in search_ui_input:
                self.clear()

                print(prompt)
                user_input = str(input("Please enter valid input\n")).strip()

            search_csv = Search()

            if user_input.lower() == "e":
                break

            self.clear()

            if user_input.lower() == "a":
                task_date = input("Date of the task (Please use DD/MM/YYYY):\n")

                while not Entry.date_check(task_date):
                    self.clear()
                    print("Error: {} doesn't seem to be a valid date.\n\n".format(task_date))
                    task_date = input("Date of the task (Please use DD/MM/YYYY):\n")

                entries = search_csv.exact_date(task_date)

            if user_input.lower() == "b":
                start_date = input("Start date in range (Please use DD/MM/YYYY):\n")
                end_date = input("End date in range (Please use DD/MM/YYYY):\n")

                while not Entry.date_check(start_date) or not Entry.date_check(end_date):
                    self.clear()
                    print("Error: {} doesn't seem to be a valid date.\n\n".format(task_date))

                    print("Start date in range:\n")
                    start_date = input("Please use DD/MM/YYYY: \n")

                    print("End date in range:\n")
                    end_date = input("Please use DD/MM/YYYY: \n")

                entries = search_csv.range_of_dates(start_date, end_date)

            if user_input.lower() == "c":
                task_title = input("Search by task title or notes: \n")

                entries = search_csv.exact_search(task_title)

            if user_input.lower() == "d":
                pattern = input("Search by task title or notes with a regex pattern (case sensitive): \n")

                entries = search_csv.regex_pattern(pattern)

            if not entries:
                print("No entries available\n\n")
            else:
                if len(entries) > 1:
                    self.search_returned_entries(entries)
                else:
                    self.entry_pagination(entries)

    def entry_pagination(self, entries):
        """Pages through returned entries for user"""

        # sort by oldest date to newest date
        entries.sort(key=lambda entry: datetime.strptime(entry.date, '%m/%d/%Y'))

        user_input = ''
        i = 0

        while user_input.lower() != 'q' and i <= len(entries) - 1:
            self.clear()
            valid_input = ['q', 'e']

            if len(entries) == 1:
                prompt = "One entry returned. Press (q) to return to menu or (e) to edit.\n\n"
                prompt += entries[i].display_entry() + "\n"
                prompt += "Press any key to return to menu."
                input(prompt)

                return

            prompt = "Page through returned entries. Press (q) to return to menu or (e) to edit.\n\n"
            prompt += entries[i].display_entry() + "\n"

            if i != 0:
                prompt += "(p)revious\n"
                valid_input.append('p')
            if i != len(entries) - 1:
                prompt += "(n)ext\n"
                valid_input.append('n')

            user_input = input(prompt)

            while user_input.lower() not in valid_input:
                self.clear()

                print("Please enter valid input\n")
                user_input = input(prompt)

            if user_input.lower() == 'p':
                i -= 1
            else:
                i += 1

            # TODO: Add ability to edit entry.

    def date_search(self, entries):
        user_input = input("Please enter a date:\n> ")

        while not Entry.date_check(user_input):
            user_input = input("Please use MM/DD/YYYY: \n")

        entries_found = []

        for entry in entries:
            if entry.date == user_input:
                entries_found.append(entry)

        self.entry_pagination(entries_found)

    def search_returned_entries(self, selected_entries):
        """User UI to search a set of entries."""

        valid_input = ['a', 'b', 'c', 'q']

        prompt = "There are multiple returned entries. How would you like to search them?\n"
        prompt += "a) Search by date\n"
        prompt += "b) Page through entries\n"
        prompt += "c) Return to menu\n\n"
        prompt += "> "

        user_input = input(prompt)

        while user_input.lower() not in valid_input:
            print("Not a valid entry. Please choose an option or press 'q' to quit ")
            user_input = input("\n> ")

        if user_input.lower() == "c" or user_input.lower() == "q":
            return

        if user_input.lower() == "a":
            self.date_search(selected_entries)

        if user_input.lower() == "b":
            self.entry_pagination(selected_entries)
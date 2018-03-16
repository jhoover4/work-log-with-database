import os

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
        Must have a date, title, time spent, and optional body text"""

        self.clear()

        print("Date of the task")
        task_date = input("Please use DD/MM/YYYY: \n")

        while not Entry.date_check(task_date):
            self.clear()
            print("Error: {} doesn't seem to be a valid date.\n\n".format(task_date))

            task_date = input("Please use DD/MM/YYYY: \n")

        # no need to validate task_title
        task_title = input("Title of the task: \n")

        time_spent = input("Time spent (rounded minutes): \n")
        while not Entry.time_check(time_spent):
            self.clear()
            time_spent = input("Please use a valid number of minutes: \n")

        notes = input("Notes (Optional, you can leave this empty): \n")

        new_entry = Entry(task_date, task_title, time_spent, notes)

        self.database.add_entries([new_entry])

        input("The entry has been added. Press any key to return to the menu\n")

    def search_task(self):
        """For searching tasks from the csv file.
        Must have a date, title, time spent, and optional body text"""

        search_ui_input = ['a', 'b', 'c', 'd', 'e']

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

            if user_input.lower() == "a":
                print("Date of the task:\n")
                task_date = input("Please use DD/MM/YYYY: \n")

                while not Entry.date_check(task_date):
                    self.clear()
                    print("Error: {} doesn't seem to be a valid date.\n\n".format(task_date))
                    print("Date of the task:\n")
                    task_date = input("Please use DD/MM/YYYY: \n")

                entries = search_csv.exact_date(task_date)

            if user_input.lower() == "b":
                print("Start date in range:\n")
                start_date = input("Please use DD/MM/YYYY: \n")

                print("End date in range:\n")
                end_date = input("Please use DD/MM/YYYY: \n")

                while Entry.date_check(start_date) == False or Entry.date_check(end_date) == False:
                    self.clear()
                    print("Error: {} doesn't seem to be a valid date.\n\n".format(task_date))

                    print("Start date in range:\n")
                    start_date = input("Please use DD/MM/YYYY: \n")

                    print("End date in range:\n")
                    end_date = input("Please use DD/MM/YYYY: \n")

                entries = search_csv.range_of_dates(start_date, end_date)

            if user_input.lower() == "c":
                # no need to validate task title
                task_title = input("Search by task title or notes: \n")

                entries = search_csv.exact_search(task_title)

            if user_input.lower() == "d":
                pattern = input("Search by task title or notes with a regex pattern: \n")

                entries = search_csv.regex_pattern(pattern)

            if len(entries) > 1:
                self.search_returned_entries(entries)
            else:
                print("Returned entry:")
                print("=" * 15 + "\n")

                if not entries:
                    print("No entries available\n\n")
                else:
                    for entry in entries:
                        print("Title: " + entry.title + "\nDate: " + entry.date + "\nTime spent: " +
                              entry.time_spent + "\nNotes:\n" + entry.notes)
                        print("=" * 15)

                input("Press any key to return to the menu\n>")

    def entry_pagination(self, entries):
        """Pages through returned entries for user"""

        for i in range(len(entries)):
            prompt = "Page through returned entries.\n\n"
            prompt += entries[i].display_entry()
            if i != 0:
                prompt += "(p)revious entry\n"
            if i != len(entries) - 1:
                prompt += "(n)ext entry\n"

            new_input = input(prompt)

            while new_input.lower() not in ['p', 'n']:
                print("Please enter valid input\n")
                new_input = input(prompt)

    def date_search(self, entries):
        pass

    def search_returned_entries(self, selected_entries):
        """User UI to search a set of entries."""

        valid_input = ['a', 'b', 'c']

        prompt = "There are multiple returned entries. How would you like to search them?\n"
        prompt += "a) Search by date\n"
        prompt += "b) Page through entries\n"
        prompt += "c) Return to menu\n\n"
        prompt += "> "

        while user_input.lower() not in valid_input:
            print("Not a valid entry. Please enter a number or press 'q' to quit ")
            user_input = input("\n> ")

        if user_input.lower() == "c" or user_input.lower() == "q":
            return

        if user_input.lower() == "a":
            self.date_search(selected_entries)

        if user_input.lower() == "b":
            self.date_search(selected_entries)
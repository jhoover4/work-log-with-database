import os
import re


from entry import Entry
from database import Search, Database

def clear():
    """Clears screen"""

    os.system('cls' if os.name == 'nt' else 'clear')


def user_interface():
    """Command line menu providing an option to either encrypt or decrypt a value.
    Add input settings required to perform the cipher process"""

    ui_input = ['a', 'b', 'c', 'q']

    while True:
        clear()

        # create database if needed
        global database

        database = Database()
        database.create_database()

        prompt = "Welcome to the Work Log project for the Treehouse Techdegree!\n\n"
        prompt += "Choose an option:\n"
        prompt += "a) Add new entry\n"
        prompt += "b) Search in existing entries\n"
        prompt += "c) Quit program\n\n"
        prompt += "> "

        user_input = str(input(prompt)).strip()

        while user_input not in ui_input:
            clear()

            print(prompt)
            user_input = str(input("Please enter valid input\n")).strip()

        if user_input.lower() == "c" or user_input.lower() == "q":
            break

        if user_input.lower() == "a":
            add_task_ui()

        if user_input.lower() == "b":
            search_task_ui()

def add_task_ui():
    """For adding new tasks to the csv file.
    Must have a date, title, time spent, and optional body text"""

    clear()

    print("Date of the task")
    task_date = input("Please use DD/MM/YYYY: \n")

    while Entry.date_check(task_date) == False:
        clear()
        print("Error: {} doesn't seem to be a valid date.\n\n".format(task_date))

        task_date = input("Please use DD/MM/YYYY: \n")

    # no need to validate task_title
    task_title = input("Title of the task: \n")

    time_spent = input("Time spent (rounded minutes): \n")
    while Entry.time_check(time_spent) == False:
        clear()
        time_spent = input("Please use a valid number of minutes: \n")

    notes = input("Notes (Optional, you can leave this empty): \n")

    new_entry = Entry(task_date, task_title, time_spent, notes)
    database.add_entry(new_entry)

    input("The entry has been added. Press any key to return to the menu\n")

def search_task_ui():
    """For searching tasks from the csv file.
    Must have a date, title, time spent, and optional body text"""

    search_ui_input = ['a', 'b', 'c', 'd', 'e']

    while True:
        clear()

        prompt = "Do you want to search by:\n\n"
        prompt += "a) Exact Date\n"
        prompt += "b) Range of Dates\n"
        prompt += "c) Exact Search\n"
        prompt += "d) Regex Pattern\n"
        prompt += "e) Return to Menu\n\n"
        prompt += "> "

        user_input = str(input(prompt)).strip()

        while user_input not in search_ui_input:
            clear()

            print(prompt)
            user_input = str(input("Please enter valid input\n")).strip()

        search_csv = Search()

        if user_input.lower() == "e":
            break

        if user_input.lower() == "a":
            print("Date of the task:\n")
            task_date = input("Please use DD/MM/YYYY: \n")

            while Entry.date_check(task_date) == False:
                clear()
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
                clear()
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

        print("Returned entries:")
        print("=" * 15 + "\n")

        if not entries:
            print("No entries available\n\n")
        else:
            for entry in entries:
                print("Title: " + entry.title + "\nDate: " + entry.date + "\nTime spent: " +
                      entry.time_spent + "\nNotes:\n" + entry.notes)
                print("=" * 15)

        input("Press any key to return to the menu\n>")


if __name__ == "__main__":
    user_interface()
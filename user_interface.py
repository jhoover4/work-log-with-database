import os
from datetime import datetime

from helpers import HelperFunctions
from models import Task, Employee


class InterfaceHelpers:

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

        while not HelperFunctions.date_check(task_date):
            self.clear()
            print("Error: {} doesn't seem to be a valid date.\n\n".format(task_date))

            task_date = input("Please use DD/MM/YYYY: \n")

        # task title
        self.clear()
        task_title = input("Title of the task: \n")

        # task time spent
        self.clear()
        time_spent = input("Time spent (integer of rounded minutes): \n")
        while not HelperFunctions.time_check(time_spent):
            self.clear()
            time_spent = input("Time spent (integer of rounded minutes): \n"
                               "Please use a valid number of minutes: \n")

        # task notes
        self.clear()
        notes = input("Notes (Optional, you can leave this empty): \n")

        # employee
        self.clear()
        employee_input = input("Employee: \n")

        try:
            employee = Employee.get(Employee.name == employee_input)
        except:
            employee = Employee.create(name=employee_input)

        Task.create(
            task_date=task_date,
            title=task_title,
            time_spent=time_spent,
            notes=notes,
            employee=employee)

        self.clear()
        input("The task has been added! Press any key to return to the menu\n")

    def search_task(self):
        """For searching tasks from the csv file.
        Must have a date, title, time spent, and optional body text"""

        search_ui_input = ['a', 'b', 'c', 'd', 'e', 'f', 'q']
        entries = None

        while True:
            self.clear()

            prompt = "Do you want to search by:\n\n"
            prompt += "a) Employee\n"
            prompt += "b) Task Date Range\n"
            prompt += "c) Task Time Spent\n"
            prompt += "d) Search Term\n"
            prompt += "e) Return to Menu\n\n"
            prompt += "> "

            user_input = str(input(prompt)).strip()

            while user_input not in search_ui_input:
                self.clear()

                print(prompt)
                user_input = str(input("Please enter valid input\n")).strip()

            if user_input.lower() == "e":
                break

            self.clear()

            if user_input.lower() == "a":
                entries = self.search_employees()

            if user_input.lower() == "b":
                entries = self.search_dates()

            if user_input.lower() == "c":
                task_time_spent = input("Search by task time spent: \n")

                entries = Task.select().where(Task.time_spent == task_time_spent)

            if user_input.lower() == "d":
                task_title = input("Search by task title or notes: \n")

                entries = Task.select().where((Task.title == task_title) | (Task.notes == task_title))

            if entries is None:
                print("No entries available\n\n")
            else:
                self.entry_pagination(entries)

    def display_task(self, entry):
        """Displays task data for user."""

        text = ""

        text += 'Task Date: ' + entry.task_date + "\n"
        text += 'Title: ' + entry.title + "\n"
        text += 'Time Spent: ' + str(entry.time_spent) + "\n"
        text += 'Notes: ' + entry.notes + "\n"
        text += 'Employee: ' + entry.employee.name + "\n"

        return text

    def edit_task(self, entry):
        """UI for user to edit a task."""

        user_input = ''

        while user_input.lower() != 'q':
            self.clear()
            user_input = ''
            valid_input = ['q', 'a', 'b', 'c', 'd', 'e']

            prompt = "What would you like to edit?\n\n"

            prompt += "a) Task Date: " + entry.task_date + "\n"
            prompt += "b) Title: " + entry.title + "\n"
            prompt += "c) Time Spent: " + str(entry.time_spent) + "\n"
            prompt += "d) Notes: " + entry.notes + "\n"
            prompt += "e) Employee: " + entry.employee.name + "\n\n"
            prompt += ">"

            while user_input.lower() not in valid_input:
                self.clear()

                print("Please enter valid input\n")
                user_input = input(prompt)

            response = ''
            if user_input == "a":
                response = "Update Task Date:\n>"
                edit_input = input(response)

                entry.task_date = edit_input

            if user_input == "b":
                response = "Update Title:\n>"
                edit_input = input(response)

                entry.title = edit_input

            if user_input == "c":
                response = "Update Time Spent:\n>"
                edit_input = input(response)

                entry.time_spent = edit_input

            if user_input == "d":
                response = "Update Notes:\n>"
                edit_input = input(response)

                entry.notes = edit_input

            if user_input == "e":
                response = "Update Employee:\n>"
                edit_input = input(response)

                entry.employee = edit_input

            entry.save()

    def entry_pagination(self, entries):
        """Pages through returned entries for user"""

        user_input = ''
        i = 0
        entries = entries.select().order_by(Task.task_date)
        query_len = entries.count()

        while user_input.lower() != 'q' and i <= query_len:
            self.clear()
            valid_input = ['q', 'e', 'd']

            if query_len == 1:
                prompt = "One task returned. Press (q) to return to menu or (e) to edit.\n\n"
            else:
                prompt = "Page through returned tasks. Press (q) to return to menu or (e) to edit.\n\n"

            prompt += self.display_task(entries[i]) + "\n"

            if i != 0 and query_len != 1:
                prompt += "(p)revious\n"
                valid_input.append('p')
            if i != query_len - 1 and query_len != 1:
                prompt += "(n)ext\n"
                valid_input.append('n')

            user_input = input(prompt + ">")

            while user_input.lower() not in valid_input:
                self.clear()
                user_input = input(prompt + "Please enter valid input\n>")

            if user_input.lower() == 'p':
                i -= 1
            elif user_input.lower() == 'd':
                entries[i].delete_instance()
            elif user_input.lower() == 'e':
                self.edit_task(entries[i])
            else:
                i += 1

    @staticmethod
    def search_employees():
        """Displays all employees in database and lets user view entries of selected employee."""

        employees = Employee.select()

        valid_input = ['q']

        prompt = "Please select an employee using the name or id.\n"

        for task in employees:
            prompt += str(task.id) + ") " + task.name.title() + "\n"
            valid_input.append(str(task.id))
            valid_input.append(task.name.lower().strip())

        prompt += "\n> "

        user_input = input(prompt).lower()
        while user_input.strip() not in valid_input:
            print("Not a valid employee. Please choose another option or press 'q' to quit ")
            user_input = input("\n> ")

        found_tasks = (Task
                       .select()
                       .join(Employee)
                       .where(Employee.name == user_input.strip().title()))

        while isinstance(found_tasks, list):
            # if there are two names that are the same
            print("Multiple matches found. Please choose a correct match.\n")

            for task in found_tasks:
                print(task.id + ") " + task.name.title() + "\n")
                valid_input.append(str(task.id))
                valid_input.append(task.name.lower())

            while user_input not in valid_input:
                print("Not a valid task. Please choose another option or press 'q' to quit ")
                user_input = input("\n> ")

            found_tasks = (Task
                           .select()
                           .join(Employee)
                           .where(Employee.name == user_input.title()))

        return found_tasks


    def search_dates(self):
        """Displays all dates in database and lets user choose a date to view entries."""

        dates = Task.select()

        valid_input = ['q']

        prompt = "\nPlease select an task using a date range. Please use DD/MM/YYYY.\n"

        for task in dates:
            prompt += str(task.id) + ") " + str(task.task_date) + "\n"
            valid_input.append(str(task.id))

        prompt += "\nStart date:\n> "

        start_date = input(prompt).lower()
        end_date = input("\nEnd date:\n> ").lower()
        while not HelperFunctions.date_check(start_date) or not HelperFunctions.date_check(end_date):
            self.clear()

            print("Error: {} doesn't seem to be a valid date.\n\n".format(start_date))

            start_date = input(prompt).lower()
            end_date = input("\nEnd date:\n> ").lower()

        try:
            found_entries = (Task
                             .select()
                             .where(Task.task_date.between(start_date, end_date)))
        except:
            print("Not a valid range. Please try again or press 'q' to quit ")

            found_entries = self.search_dates()

        return found_entries

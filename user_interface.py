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
            time_spent = input("Please use a valid number of minutes: \n")

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

                entries = Task.select().where((Task.title == task_title) | (Task.time_spent == task_title))

            if entries is None:
                print("No entries available\n\n")
            else:
                self.entry_pagination(entries)

    def display_entry(self, entry):
        text = ""

        text += 'Task Date: ' + entry.task_date + "\n"
        text += 'Title: ' + entry.title + "\n"
        text += 'Time Spent: ' + str(entry.time_spent) + "\n"
        text += 'Notes: ' + entry.notes + "\n"
        text += 'Employee: ' + entry.employee.name + "\n"

        return text

    def entry_pagination(self, entries):
        """Pages through returned entries for user"""

        user_input = ''
        i = 0
        query_len = entries.count()

        for task in entries.select().order_by(Task.task_date).paginate(1, 1):
            self.clear()
            valid_input = ['q', 'e', 'd']

            if query_len == 1:
                prompt = "One task returned. Press (q) to return to menu or (e) to edit.\n\n"
                prompt += self.display_entry(entries[i]) + "\n"
                prompt += "Press any key to return to menu."
                input(prompt)

                return

            while user_input.lower() != 'q':
                self.clear()
                valid_input = ['q', 'e', 'd']

                prompt = "Page through returned tasks. Press (q) to return to menu or (e) to edit.\n\n"
                prompt += self.display_entry(task) + "\n"

                if i != 0:
                    prompt += "(p)revious\n"
                    valid_input.append('p')
                if i != query_len - 1:
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

            # TODO: Add ability to edit task.
            # TODO: Add ability to delete task.

    @staticmethod
    def search_employees():
        """Displays all employees in database and lets user view entries of selected employee."""

        employees = Employee.select()

        valid_input = ['q']

        for task in employees:
            print(str(task.id) + ") " + task.name.title() + "\n")
            valid_input.append(str(task.id))
            valid_input.append(task.name.lower())

        prompt = "\nPlease select an task using the name or id.\n"
        prompt += "> "

        user_input = input(prompt).lower()
        while user_input not in valid_input:
            print("Not a valid task. Please choose another option or press 'q' to quit ")
            user_input = input("\n> ")

        found_tasks = (Task
                       .select()
                       .join(Employee)
                       .where(Employee.name == user_input.title()))

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

        for task in dates:
            print(str(task.id) + ") " + str(task.task_date) + "\n")
            valid_input.append(str(task.id))

        prompt = "\nPlease select an task using a date range. Please use DD/MM/YYYY.\n"
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

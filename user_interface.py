import os

from helpers import HelperFunctions
import models


class InterfaceHelpers:

    @staticmethod
    def clear():
        """Clears screen for user."""

        os.system('cls' if os.name == 'nt' else 'clear')

    def input_date(self, msg):
        self.clear()
        task_date = input(msg)

        while not HelperFunctions.date_check(task_date):
            self.clear()
            err_msg = "ERROR: {} isn't a valid date.\n\n".format(task_date)

            task_date = input(err_msg + msg)

        return task_date

    def input_time(self, msg):
        self.clear()
        time_spent = input(msg)

        while not HelperFunctions.time_check(time_spent):
            self.clear()
            err_msg = "ERROR: {} isn't a valid number of minutes.\n\n".format(time_spent)

            time_spent = input(err_msg + msg)

        return time_spent

    def input_employee(self, msg):
        employee_input = input(msg)

        while not employee_input.isalpha():
            self.clear()
            err_msg = "ERROR: {} isn't a valid name.\n\n".format(employee_input)

            employee_input = input(err_msg + msg)

        return employee_input

    def input_text(self, msg):
        self.clear()
        notes = input(msg)

        return notes

    def add_task(self):
        """For adding new tasks to the csv file.
        Must have a date, title, time spent, and optional body text.
        """

        task_date = self.input_date("Date of the task (Please use DD/MM/YYYY): \n")
        task_title = self.input_text("Title of the task: \n")
        time_spent = self.input_time("Time spent (integer of rounded minutes): \n")
        notes = self.input_text("Notes (Optional, you can leave this empty): \n")
        employee_input = self.input_employee("Employee name:\n>")

        try:
            employee = models.Employee.get(models.Employee.name == employee_input)
        except models.DoesNotExist:
            employee = models.Employee.create(name=employee_input)

        models.Task.create(
            task_date=task_date,
            title=task_title,
            time_spent=time_spent,
            notes=notes,
            employee=employee)

        self.clear()
        input("The task has been added! Press any key to return to the menu\n")

    def task_submenu(self, display_text):
        """Used as a menu for both editing and searching tasks."""

        valid_input = ['a', 'b', 'c', 'd', 'e', 'q']
        self.clear()

        user_input = str(input(display_text)).strip()

        while user_input not in valid_input:
            self.clear()
            user_input = str(input(display_text + "Please enter valid input\n")).strip()

        return user_input

    def search_task(self):
        """For searching tasks from the csv file.
        Must have a date, title, time spent, and optional body text.
        """

        entries = None

        prompt = "Do you want to search by:\n\n"
        prompt += "a) Employee\n"
        prompt += "b) Task Date Range\n"
        prompt += "c) Task Time Spent\n"
        prompt += "d) Search Term\n"
        prompt += "e) Return to Menu\n\n"
        prompt += "> "

        while True:
            user_input = self.task_submenu(prompt)

            if user_input.lower() == "e":
                break

            self.clear()
            if user_input.lower() == "a":
                entries = self.search_employees()

            if user_input.lower() == "b":
                entries = self.search_dates()

            if user_input.lower() == "c":
                task_time_spent = input("Search by task time spent: \n")

                entries = models.Task.select().where(models.Task.time_spent == task_time_spent)

            if user_input.lower() == "d":
                task_title = input("Search by task title or notes: \n")

                entries = models.Task.select().where((models.Task.title == task_title)
                                                     | (models.Task.notes == task_title))

            if entries is None:
                print("No entries available\n\n")
            else:
                self.entry_pagination(entries)

    def display_task(self, task):
        """Displays task data for user."""

        text = ""

        text += 'Task Date: ' + task.task_date + "\n"
        text += 'Title: ' + task.title + "\n"
        text += 'Time Spent: ' + str(task.time_spent) + "\n"
        text += 'Notes: ' + task.notes + "\n"
        text += 'Employee: ' + task.employee.name + "\n"

        return text

    def edit_task(self, entry):
        """UI for user to edit a task."""

        user_input = ''
        prompt = "What would you like to edit? Press (q) to return to tasks.\n\n"
        prompt += "a) Task Date: " + entry.task_date + "\n"
        prompt += "b) Title: " + entry.title + "\n"
        prompt += "c) Time Spent: " + str(entry.time_spent) + "\n"
        prompt += "d) Notes: " + entry.notes + "\n"
        prompt += "e) Employee: " + entry.employee.name + "\n\n"
        prompt += ">"

        while user_input.lower() != 'q':
            user_input = self.task_submenu(prompt)

            if user_input == "a":
                entry.task_date = self.input_date("Update Task Date:\n>")
            if user_input == "b":
                entry.title = self.input_text("Update Title:\n>")
            if user_input == "c":
                entry.time_spent = self.input_time("Update Time Spent:\n>")
            if user_input == "d":
                entry.notes = self.input_text("Update Notes:\n>")
            if user_input == "e":
                entry.employee = self.input_employee("Update Employee:\n>")

            entry.save()

    def entry_pagination(self, entries):
        """Pages through returned entries for user"""

        user_input = ''
        i = 0
        entries = entries.select().order_by(models.Task.task_date)
        query_len = entries.count()

        while user_input.lower() != 'q' and i <= query_len:
            self.clear()
            valid_input = ['q', 'e', 'd']

            if query_len == 1:
                prompt = "One task returned. Press (q) to return to menu, (d) to delete, or (e) to edit.\n\n"
            else:
                prompt = "Page through returned tasks. Press (q) to return to menu, (d) to delete, or (e) to edit.\n\n"

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

        employees = models.Employee.select()

        valid_input = ['q']

        prompt = "Please select an employee using the name.\n"

        for task in employees:
            prompt += str(task.id) + ") " + task.name.title() + "\n"
            valid_input.append(str(task.id))
            valid_input.append(task.name.lower().strip())

        prompt += "\n> "

        user_input = input(prompt).lower()
        while user_input.strip() not in valid_input:
            print("Not a valid employee. Please choose another option or press 'q' to quit ")
            user_input = input("\n> ")

        found_tasks = (models.Task
                       .select()
                       .join(models.Employee)
                       .where(models.Employee.name == user_input.strip().title()))

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

            found_tasks = (models.Task
                           .select()
                           .join(models.Employee)
                           .where(models.Employee.name == user_input.title()))

        return found_tasks

    def search_dates(self):
        """Displays all dates in database and lets user choose a date to view entries."""

        dates = models.Task.select()

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

            print("ERROR: {} isn't a valid date.\n\n".format(start_date))

            start_date = input(prompt).lower()
            end_date = input("\nEnd date:\n> ").lower()

        try:
            found_entries = (models.Task
                             .select()
                             .where(models.Task.task_date.between(start_date, end_date)))
        except models.DoesNotExist:
            print("Not a valid range. Please try again or press 'q' to quit ")

            found_entries = self.search_dates()

        return found_entries

import os

from helpers import HelperFunctions
import models


class InterfaceHelpers:

    @staticmethod
    def clear():
        """Clears screen for user."""

        os.system('cls' if os.name == 'nt' else 'clear')

    def ask_for_valid_input(self, prompt, add_quit=False):
        self.clear()

        if add_quit:
            new_prompt = prompt + "\nPlease enter valid input. Press q to quit.\n>"
        else:
            new_prompt = prompt + "\nPlease enter valid input.\n>"

        user_input = input(new_prompt).strip().lower()

        return user_input

    def input_date(self, msg):
        self.clear()
        task_date = input(msg)

        while not HelperFunctions.date_check(task_date):
            task_date = self.ask_for_valid_input(msg)

        return task_date

    def input_time(self, msg):
        self.clear()
        time_spent = input(msg)

        while not HelperFunctions.time_check(time_spent):
            time_spent = self.ask_for_valid_input(msg)

        return time_spent

    def input_employee(self, msg):
        employee_input = input(msg)

        while not employee_input.isalpha():
            employee_input = self.ask_for_valid_input(msg)

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
            user_input = self.ask_for_valid_input(display_text)

        return user_input

    def search_task_menu(self):
        """For searching tasks from the csv file.
        Must have a date, title, time spent, and optional body text.
        """

        prompt = "Do you want to search by:\n\n"
        prompt += "a) Employee\n"
        prompt += "b) Task Date Range\n"
        prompt += "c) Task Time Spent\n"
        prompt += "d) Search Term\n"
        prompt += "e) Return to Menu\n\n"
        prompt += "> "

        while self.search_task(self.task_submenu(prompt)) is True:
            self.search_task(self.task_submenu(prompt))

    def search_task(self, menu_choice):
        entries = None

        if menu_choice.lower() == "e":
            return False

        self.clear()
        if menu_choice.lower() == "a":
            entries = self.search_employees()

        if menu_choice.lower() == "b":
            entries = self.search_dates()

        if menu_choice.lower() == "c":
            task_time_spent = input("Search by task time spent: \n")

            entries = models.Task.select().where(models.Task.time_spent == task_time_spent)

        if menu_choice.lower() == "d":
            task_title = input("Search by task title or notes: \n")

            entries = models.Task.select().where((models.Task.title == task_title)
                                                 | (models.Task.notes == task_title))

        if entries is None:
            print("No entries available.\n\n")
        else:
            self.entry_pagination(entries)

        return True

    def display_task(self, task):
        """Displays task data for user."""

        text = ""

        text += 'Task Date: ' + task.task_date + "\n"
        text += 'Title: ' + task.title + "\n"
        text += 'Time Spent: ' + str(task.time_spent) + "\n"
        text += 'Notes: ' + task.notes + "\n"
        text += 'Employee: ' + task.employee.name + "\n"

        return text

    def edit_task_menu(self, entry):
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
            self.edit_task(user_input, entry)

    def edit_task(self, menu_choice, entry):

        if menu_choice == "a":
            entry.task_date = self.input_date("Update Task Date:\n>")
        if menu_choice == "b":
            entry.title = self.input_text("Update Title:\n>")
        if menu_choice == "c":
            entry.time_spent = self.input_time("Update Time Spent:\n>")
        if menu_choice == "d":
            entry.notes = self.input_text("Update Notes:\n>")
        if menu_choice == "e":
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
                self.edit_task_menu(entries[i])
            else:
                i += 1

    def list_items(self, prompt, items):

        is_employee = (items.model.__name__ == 'Employee')

        if len(items) < 1:
            prompt = "No items available."

        if len(items) == 1:
            prompt += str(items[0].id) + ") "
            if is_employee:
                prompt += items[0].name.title() + "\n"
            else:
                prompt += items[0].title.title() + "\n"
        else:
            for item in items:
                prompt += str(item.id) + ") "
                if is_employee:
                    prompt += item.name.title() + "\n"
                else:
                    prompt += item.title.title() + "\n"

        return prompt

    def add_valid_input(self, items):
        valid_input = ['q']

        for item in items:
            valid_input.append(str(item.id))
            if (items.model.__name__ == 'Employee'):
                valid_input.append(item.name.lower().strip())
            else:
                valid_input.append(item.title.lower().strip())

        return valid_input

    def multiple_tasks(self, tasks):
        """If there are two names that are the same."""

        prompt = self.list_items('Multiple matches found. Please choose a correct match.\n', tasks)
        prompt += "\n> "
        valid_input = self.add_valid_input(tasks)

        user_input = input(prompt)
        while user_input not in valid_input:
            user_input = self.ask_for_valid_input(prompt)

        found_tasks = (models.Task
                       .select()
                       .join(models.Employee)
                       .where(models.Employee.name == user_input.title()))

        return found_tasks

    def search_employees(self):
        """Displays all employees in database and lets user view entries of selected employee."""

        employees = models.Employee.select()
        prompt = self.list_items(employees)
        prompt += "\n> "
        valid_input = self.add_valid_input('Multiple matches found. Please choose a correct match.\n', employees)

        user_input = input(prompt).lower()
        while user_input.strip() not in valid_input:
            user_input = self.ask_for_valid_input(prompt)

        found_tasks = (models.Task
                       .select()
                       .join(models.Employee)
                       .where(models.Employee.name == user_input.strip().title()))

        while isinstance(found_tasks, list):
            found_tasks = self.multiple_tasks(found_tasks)

        return found_tasks

    def search_dates(self):
        """Displays all dates in database and lets user choose a date to view entries."""

        tasks = models.Task.select()

        prompt = self.list_items("\nSelect a task using a date range. Please use DD/MM/YYYY.", tasks)
        start_date_prompt = prompt + "\nStart date:\n> "
        end_date_prompt = prompt + "\nEnd date:\n> "
        valid_input = self.add_valid_input(tasks)

        start_date = self.input_date(start_date_prompt)
        while start_date.strip() not in valid_input:
            start_date = self.input_date(start_date_prompt)
        end_date = self.input_date(end_date_prompt)
        while end_date.strip() not in valid_input:
            end_date = self.input_date(end_date_prompt)

        try:
            found_entries = (models.Task
                             .select()
                             .where(models.Task.task_date.between(start_date, end_date)))
        except models.DoesNotExist:
            print("Not a valid range. Please try again or press 'q' to quit ")

            found_entries = self.search_dates()

        return found_entries

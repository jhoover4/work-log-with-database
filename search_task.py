import unittest
import models

from user_interface import UserInterface


class SearchTask(UserInterface):

    def search_task_ui(self):
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

        while self.search_task_options(self.task_submenu(prompt)) is True:
            self.search_task_options(self.task_submenu(prompt))

    def search_task_options(self, menu_choice):
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

        if entries:
            self.entry_pagination(entries)
        else:
            print("No entries available.\n\n")

        return True

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

    def search_employees(self):
        """Displays all employees in database and lets user view entries of selected employee."""

        employees = models.Employee.select()
        prompt = self.list_items('Please select an employee using the name.\n', employees)
        prompt += "\n> "
        valid_input = self.add_valid_input(employees)

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

        start_date = self.input_date(start_date_prompt)
        end_date = self.input_date(end_date_prompt)

        try:
            found_entries = (models.Task
                             .select()
                             .where(models.Task.task_date.between(start_date, end_date)))
        except models.DoesNotExist:
            print("Not a valid range. Please try again or press 'q' to quit ")

            found_entries = self.search_dates()

        return found_entries

    @staticmethod
    def list_items(prompt, items):

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

    @staticmethod
    def add_valid_input(items):
        valid_input = ['q']

        for item in items:
            valid_input.append(str(item.id))

            if items.model.__name__ == 'Employee':
                valid_input.append(item.name.lower().strip())
            else:
                valid_input.append(item.title.lower().strip())

        return valid_input

    @staticmethod
    def display_task(task):
        """Displays task data for user."""

        text = ""

        text += 'Task Date: ' + task.task_date + "\n"
        text += 'Title: ' + task.title + "\n"
        text += 'Time Spent: ' + str(task.time_spent) + "\n"
        text += 'Notes: ' + task.notes + "\n"
        text += 'Employee: ' + task.employee.name + "\n"

        return text

    @staticmethod
    def edit_task_menu(task):
        """UI for user to edit a task."""

        prompt = "What would you like to edit? Press (q) to return to tasks.\n\n"
        prompt += "a) Task Date: " + task.task_date + "\n"
        prompt += "b) Title: " + task.title + "\n"
        prompt += "c) Time Spent: " + str(task.time_spent) + "\n"
        prompt += "d) Notes: " + task.notes + "\n"
        prompt += "e) Employee: " + task.employee.name + "\n\n"
        prompt += ">"

        return prompt

    def edit_task_menu_loop(self, task):
        user_input = ''
        prompt = self.edit_task_menu(task)

        while user_input.lower() != 'q':
            user_input = self.task_submenu(prompt)
            self.edit_task(user_input, task)

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

if __name__ == '__main__':
    unittest.main()
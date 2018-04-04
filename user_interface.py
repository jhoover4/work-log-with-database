import os
from datetime import datetime


class UserInterface:

    def return_to_menu(self, add_msg=''):
        self.clear()

        return "{}. Press any key to return to the menu\n".format(add_msg)

    @staticmethod
    def date_check(date_str):
        """Dates must be in DD/MM/YYYY format."""

        date_good = True

        try:
            datetime.strptime(date_str, "%m/%d/%Y")
        except ValueError:
            date_good = False

        return date_good

    @staticmethod
    def time_check(time_str):
        """Times must be in minutes format."""

        time_good = True

        try:
            datetime.strptime(time_str, "%M")
        except ValueError:
            time_good = False

        return time_good

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
        """Processes user input and verifies it."""

        self.clear()
        task_date = input(msg)

        while not self.date_check(task_date):
            task_date = self.ask_for_valid_input(msg)

        return task_date

    def input_time(self, msg):
        self.clear()
        time_spent = input(msg)

        while not self.time_check(time_spent):
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

    def task_submenu(self, display_text):
        """Used as a menu for both editing and searching tasks."""

        valid_input = ['a', 'b', 'c', 'd', 'e', 'q']
        self.clear()

        user_input = str(input(display_text)).strip()

        while user_input not in valid_input:
            user_input = self.ask_for_valid_input(display_text)

        return user_input

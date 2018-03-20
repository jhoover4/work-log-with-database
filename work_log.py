from models import Employee, Task, db
from user_interface import InterfaceHelpers


def work_log():
    """Command line menu providing an option to either encrypt or decrypt a value.
    Add input settings required to perform the cipher process"""

    db.connect()
    db.create_tables([Employee, Task])

    valid_input = ['a', 'b', 'c', 'q']

    while True:
        user_interface = InterfaceHelpers()

        user_interface.clear()

        prompt = "Welcome to the Work Log project for the Treehouse Techdegree!\n\n"
        prompt += "Choose an option:\n"
        prompt += "a) Add new entry\n"
        prompt += "b) Search in existing entries\n"
        prompt += "c) Quit program\n\n"
        prompt += "> "

        user_input = str(input(prompt)).strip()

        while user_input not in valid_input:
            user_interface.clear()

            print(prompt)
            user_input = str(input("Please enter valid input\n")).strip()

        if user_input.lower() == "c" or user_input.lower() == "q":
            print("Thanks for using work log!\n")
            break

        if user_input.lower() == "a":
            user_interface.add_task()

        if user_input.lower() == "b":
            user_interface.search_task()


if __name__ == "__main__":
    work_log()

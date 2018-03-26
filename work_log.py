import models
from user_interface import InterfaceHelpers

user_interface = InterfaceHelpers()


def main_menu():
    """Main menu lets user choose between adding or searching entries."""

    valid_input = ['a', 'b', 'c', 'q']

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

    return user_input.lower()


def work_log(menu_choice):
    """Main loop for the work log application."""

    if menu_choice == "c" or menu_choice.lower() == "q":
        print("Thanks for using work log!\n")
        models.db.close()
        return False

    if menu_choice == "a":
        user_interface.add_task()

    if menu_choice == "b":
        user_interface.search_task()

    return True


if __name__ == "__main__":
    models.initialize_db()
    while work_log(main_menu()) is True:
        work_log(main_menu())
    models.db.close()

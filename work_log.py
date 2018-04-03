import models
from user_interface import InterfaceHelpers

user_interface = InterfaceHelpers()



def main_menu():
    """Menu prompt for main loop of application."""

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
        user_input = user_interface.ask_for_valid_input(prompt)

    return user_input.lower()


def main_loop(menu_choice):
    """Main branches for the application,
    users can choose to add an entry or search existing entries.
    """

    if menu_choice == "c" or menu_choice.lower() == "q":
        print("Thanks for using work log!\n")
        models.db.close()
        return False

    if menu_choice == "a":
        user_interface.add_task()

    if menu_choice == "b":
        user_interface.search_task_menu()

    return True


def run_work_log():
    """Set up work_log database and run main loop."""

    models.initialize_db()

    while main_loop(main_menu()) is True:
        main_loop(main_menu())

    models.db.close()


if __name__ == "__main__":
    run_work_log()

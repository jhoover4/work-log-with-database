import models


from user_interface import UserInterface

class AddTask(UserInterface):

    def add_task_ui(self):
        """For adding new tasks to the csv file.
        Must have a date, title, time spent, and optional body text.
        """

        task_date = self.input_date("Date of the task (Please use DD/MM/YYYY): \n")
        task_title = self.input_text("Title of the task: \n")
        time_spent = self.input_time("Time spent (integer of rounded minutes): \n")
        notes = self.input_text("Notes (Optional, you can leave this empty): \n")
        employee_input = self.input_employee("Employee name: \n")

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

        input(self.return_to_menu())
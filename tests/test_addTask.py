import unittest
from unittest.mock import patch
import models


from add_task import AddTask


class TestAddTask(unittest.TestCase):
    def setUp(self):
        models.initialize_db()
        self.ui_obj = AddTask()

    def tearDown(self):
        tasks = models.Task.select()
        for task in tasks:
            task.delete_instance()

        employees = models.Employee.select()
        for employee in employees:
            employee.delete_instance()

        try:
            models.db.close()
        except models.OperationalError:
            pass

    @patch('builtins.input')
    def test_add_task(self, mock):
        mock.side_effect = ['06/14/1990', 'Test2', '13', 'These are notes. ', 'Jordan', 'q']
        self.ui_obj.add_task_ui()

        try:
            models.Task.get(models.Task.title == 'Test2')
        except models.DoesNotExist:
            self.fail("Couldn't find inputted task.")

    @patch('builtins.input')
    def test_add_task_new_employee(self, mock):
        mock.side_effect = ['06/11/1990', 'Test3', '15', 'These are better notes. ', 'Nirvana', 'q']
        self.ui_obj.add_task_ui()

        try:
            models.Employee.get(models.Employee.name == 'Nirvana')
        except models.DoesNotExist:
            self.fail("Couldn't find inputted task.")

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch

import models
import helpers
import user_interface
import work_log

class TaskTests(unittest.TestCase):

    def setUp(self):
        models.initialize_db()

        self.task_date = '06/13/1990'
        self.title = 'Test'
        self.time_spent = 15

        try:
            self.employee = models.Employee.get(models.Employee.name == 'Jordan')
        except:
            self.employee = models.Employee.create(name='Jordan')

        self.test_task = models.Task.create(
            task_date=self.task_date,
            title=self.title,
            time_spent=self.time_spent,
            employee=self.employee)

    def tearDown(self):
        try:
            self.test_task.delete_instance()
        except:
            pass

        models.db.close()

    def test_check_entry_table(self):
        assert models.Task.table_exists()

    def test_task_date(self):
        task = models.Task.get(task_date=self.task_date)
        self.assertEqual(task.task_date, self.task_date)

    def test_title(self):
        task = models.Task.get(title=self.title)
        self.assertEqual(task.title, self.title)

    def test_time_spent(self):
        task = models.Task.get(time_spent=self.time_spent)
        self.assertEqual(task.time_spent, self.time_spent)

    # def test_notes(self):
    #     task = models.Task.get(task_date=self.task_date)
    #     self.assertEqual(task.task_date, self.task_date)

    def test_employee(self):
        task = models.Task.get(employee=self.employee)
        self.assertEqual(task.employee, self.employee)

    def test_task_repeat_title(self):
        with self.assertRaises(ValueError):
            models.Task.create(
                task_date='06/14/1990',
                title='Test',
                time_spent=20,
                employee='Joel')

    def test_delete_task(self):
        models.Task.get(title="Test").delete_instance()
        with self.assertRaises(Exception):
            models.Task.get(title="Test").delete_instance()


class EmployeeTests(unittest.TestCase):
    pass


class HelpersTests(unittest.TestCase):

    def test_date_check(self):
        assert helpers.HelperFunctions.date_check('06131990') is False
        assert helpers.HelperFunctions.date_check('06/13/1990') is True

    def test_time_check(self):
        assert helpers.HelperFunctions.time_check('1000') is False
        assert helpers.HelperFunctions.time_check('15') is True


class InterfaceHelpersTests(unittest.TestCase):
    def setUp(self):

        self.user_interface = user_interface.InterfaceHelpers()

        self.task_date_input = '06/13/1990'
        self.title_input = 'Test'
        self.time_spent_input = 15
        self.notes_input = 'Testing'
        self.employee_input = 'Jordan'

    @patch('builtins.input', return_value='q')
    def test_quit_program(self):
        work_log.work_log()

        self.assertRaises(SystemExit)

    @patch('builtins.input', return_value='a')
    def test_search_task(self, mock_search_employees):
        self.user_interface.search_task()

        self.assertTrue(self.user_interface.mock_search_employees.called_with())

    @patch('work-log-with-database.get_input', return_value='no')
    def test_answer_no(self, input):
        self.assertEqual(answer(), 'you entered no')


if __name__ == '__main__':
    unittest.main()

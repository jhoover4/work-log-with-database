import unittest
from unittest.mock import patch
from unittest import mock
import io
import sys

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
        except models.DoesNotExist:
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


class WorkLogTests(unittest.TestCase):

    @patch('builtins.input')
    def test_main_menu(self, mock):
        mock.side_effect = ['a']
        self.assertEqual(work_log.main_menu(), 'a')

    def test_work_log_end_loop(self):
        self.assertEqual(work_log.work_log('q'), False)
        self.assertEqual(work_log.work_log('c'), False)

    @patch.object(user_interface.InterfaceHelpers, 'add_task')
    def test_work_log_add_task(self, mock):
        work_log.work_log('a')
        self.assertTrue(mock.called)

    @patch.object(user_interface.InterfaceHelpers, 'search_task')
    def test_work_log_search_task(self, mock):
        work_log.work_log('b')
        self.assertTrue(mock.called)


class InterfaceHelpersTests(unittest.TestCase):
    def setUp(self):
        models.initialize_db()
        self.ui_obj = user_interface.InterfaceHelpers()

        self.task_date_input = '06/13/1990'
        self.title_input = 'Test'
        self.time_spent_input = '15'
        self.notes_input = 'Testing'
        self.employee_input = 'Jordan'

        try:
            self.employee = models.Employee.get(models.Employee.name == 'Jordan')
        except:
            self.employee = models.Employee.create(name='Jordan')

        self.test_task = models.Task.create(
            task_date=self.task_date_input,
            title=self.title_input,
            time_spent=self.notes_input,
            employee=self.employee)

    def tearDown(self):
        try:
            self.test_task.delete_instance()
        except models.DoesNotExist:
            pass

        models.db.close()

    @patch('builtins.input')
    def test_input_date(self, mock):
        mock.side_effect = ['06/13/199']
        mock.side_effect = ['06/13/1990']
        self.assertEqual(self.ui_obj.input_date(''), self.task_date_input)

    @patch('builtins.input')
    def test_input_time(self, mock):
        mock.side_effect = [15]
        mock.side_effect = ['1000']
        mock.side_effect = ['15']
        self.assertEqual(self.ui_obj.input_time(''), self.time_spent_input)

    @patch('builtins.input')
    def test_input_employee(self, mock):
        mock.side_effect = [1]
        mock.side_effect = ['Jordan']
        self.assertEqual(self.ui_obj.input_employee(''), self.employee_input)

    @patch('builtins.input')
    def test_input_text(self, mock):
        mock.side_effect = ['Test']
        self.assertEqual(self.ui_obj.input_text(''), self.title_input)

    def test_display_task(self):
        text = ""
        text += "Task Date: 06/13/1990\n"
        text += "Title: Test\n"
        text += "Time Spent: 15\n"
        text += "Notes: Testing\n"
        text += "Employee: Jordan\n"

        self.assertEqual(text, self.ui_obj.display_task(self.test_task))

if __name__ == '__main__':
    unittest.main()

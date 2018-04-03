import unittest
from unittest.mock import patch

import models
import user_interface


class TestInterfaceHelpers(unittest.TestCase):
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
        except models.DoesNotExist:
            self.employee = models.Employee.create(name='Jordan')

        self.test_task = models.Task.create(
            task_date=self.task_date_input,
            title=self.title_input,
            time_spent=self.time_spent_input,
            notes=self.notes_input,
            employee=self.employee)

    def tearDown(self):
        try:
            self.test_task.delete_instance()
            new_model = models.Task.get(models.Task.title == 'Test2')
            new_model.delete_instance()
        except models.DoesNotExist:
            pass

        try:
            models.db.close()
        except models.OperationalError:
            pass

    @patch('builtins.input')
    def test_input_date(self, mock):
        mock.side_effect = ['06/13/199', '06/13/1990']
        self.assertEqual(self.ui_obj.input_date(''), self.task_date_input)

    @patch('builtins.input', side_effect=[15, '1000', '15'])
    def test_input_time(self, mock):
        mock.side_effect = ['15', '1000', '15']

        self.assertEqual(self.ui_obj.input_time(''), self.time_spent_input)

    @patch('builtins.input')
    def test_input_employee(self, mock):
        mock.side_effect = ['1', 'Jordan']
        self.assertEqual(self.employee_input.lower(), self.ui_obj.input_employee(''))

    @patch('builtins.input')
    def test_input_text(self, mock):
        mock.side_effect = ['Test']
        self.assertEqual(self.ui_obj.input_text(''), self.title_input)

    @patch('builtins.input')
    def test_ask_for_valid_input(self, mock):
        mock.side_effect = ['test']
        self.assertEqual(self.ui_obj.ask_for_valid_input(''), 'test')

    @patch('builtins.input')
    def test_ask_for_valid_input_with_quit(self, mock):
        mock.side_effect = ['test']
        self.assertEqual(self.ui_obj.ask_for_valid_input('', add_quit=True), 'test')

    @patch('builtins.input')
    def test_add_task(self, mock):
        mock.side_effect = ['06/14/1990', 'Test2', '13', 'These are notes. ', self.employee.name, 'q']
        self.ui_obj.add_task()

        try:
            models.Task.get(models.Task.title == 'Test2')
        except models.DoesNotExist:
            self.fail("Couldn't find inputted task.")

    # @patch('builtins.input', return_value="\nPlease enter valid input.\n>")
    # def test_task_submenu(self, mock):
    #     mock.side_effect = ['2']
    #
    #     self.ui_obj.task_submenu('')

    @patch('builtins.input')
    def test_task_submenu(self, mock):
        mock.side_effect = ['a']

        self.assertEqual('a', self.ui_obj.task_submenu(''))

    @patch('builtins.input')
    def test_search_task_menu(self, mock):
        mock.side_effect = ['e']

        self.assertFalse(self.ui_obj.search_task_menu())

    @patch('builtins.input')
    def test_edit_task(self, mock):
        mock.side_effect = ['06/14/1990', 'Test2', '13', 'These are notes. ', self.employee.name, 'q']
        self.ui_obj.add_task()

        try:
            models.Task.get(models.Task.title == 'Test2')
        except models.DoesNotExist:
            self.fail("Couldn't find inputted task.")

    @patch.object(user_interface.InterfaceHelpers, 'search_employees')
    def test_search_task_employees(self, mock):
        mock.side_effect = ['Jordan']
        self.ui_obj.search_task('a')
        self.assertTrue(mock.called)

    @patch.object(user_interface.InterfaceHelpers, 'search_dates')
    def test_search_task_dates(self, mock):
        mock.side_effect = ['q']
        self.ui_obj.search_task('b')
        self.assertTrue(mock.called)

    @patch.object(user_interface.InterfaceHelpers, 'entry_pagination')
    def test_search_task_time(self, mock_ui):
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ['15']
            self.ui_obj.search_task('c')
            self.assertTrue(mock_ui.called)

    @patch('builtins.input')
    def test_search_task_return(self, mock):
        mock.side_effect = ['words not in a task']
        self.assertTrue(self.ui_obj.search_task('d'))

    def test_search_task_quit(self):
        self.assertEqual(self.ui_obj.search_task('e'), False)

    def test_list_items_employee(self):
        text = '1) Jordan\n'
        employees = models.Employee.select()

        self.assertEqual(text, self.ui_obj.list_items('', employees))

    def test_list_items_task(self):
        text = '1) Test\n'
        tasks = models.Task.select()

        self.assertEqual(text, self.ui_obj.list_items('', tasks))

    def test_add_valid_input_employee(self):
        valid_input = ['q', '1', 'jordan']
        employees = models.Employee.select()

        self.assertEqual(valid_input, self.ui_obj.add_valid_input(employees))

    def test_add_valid_input_task(self):
        valid_input = ['q', '1', 'test']
        tasks = models.Task.select()

        self.assertEqual(valid_input, self.ui_obj.add_valid_input(tasks))

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

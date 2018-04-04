import unittest
from unittest.mock import patch


import models
from search_task import SearchTask


class TestSearchTask(unittest.TestCase):
    def setUp(self):
        models.initialize_db()

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

        self.ui_obj = SearchTask()

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
    def test_search_task_ui(self, mock):
        mock.side_effect = ['e']

        self.assertFalse(self.ui_obj.search_task_ui())

    @patch.object(SearchTask, 'search_employees')
    def test_search_task_employees(self, mock):
        mock.side_effect = ['Jordan']
        self.ui_obj.search_task_options('a')
        self.assertTrue(mock.called)

    @patch.object(SearchTask, 'search_dates')
    def test_search_task_dates(self, mock_ui):
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ['06/13/1990']
            self.ui_obj.search_task_options('b')
            self.assertTrue(mock_ui.called)

    @patch.object(SearchTask, 'entry_pagination')
    def test_search_task_time(self, mock_ui):
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ['15']
            self.ui_obj.search_task_options('c')
            self.assertTrue(mock_ui.called)

    @patch('builtins.input')
    def test_search_task_return(self, mock):
        mock.side_effect = ['words not in a task']
        self.assertTrue(self.ui_obj.search_task_options('d'))

    def test_search_task_quit(self):
        self.assertEqual(self.ui_obj.search_task_options('e'), False)

    def test_list_items_employee(self):
        text = '1) Jordan\n'
        employees = models.Employee.select()

        self.assertEqual(text, self.ui_obj.list_items('', employees))

    def test_list_items_task(self):
        text = '1) Test\n'
        tasks = models.Task.select()

        self.assertEqual(text, self.ui_obj.list_items('', tasks))

    def test_list_items_empty(self):
        tasks = models.Task.select().where(models.Task.title == 'Not A Real Title')

        self.assertEqual("No items available.", self.ui_obj.list_items('', tasks))

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

    def test_edit_task_menu(self):
        expected_output = "What would you like to edit? Press (q) to return to tasks.\n\n"
        expected_output += "a) Task Date: " + self.test_task.task_date + "\n"
        expected_output += "b) Title: " + self.test_task.title + "\n"
        expected_output += "c) Time Spent: " + str(self.test_task.time_spent) + "\n"
        expected_output += "d) Notes: " + self.test_task.notes + "\n"
        expected_output += "e) Employee: " + self.test_task.employee.name + "\n\n"
        expected_output += ">"

        self.assertEqual(expected_output, self.ui_obj.edit_task_menu(self.test_task))

    @patch.object(SearchTask, 'edit_task_menu')
    def test_edit_task_menu(self, mock_ui):
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ['a', '06/13/1990', 'q']
            self.ui_obj.edit_task_menu_loop(self.test_task)
            self.assertTrue(mock_ui.called)

    @patch.object(SearchTask, 'edit_task_menu')
    def test_edit_task_menu(self, mock_ui):
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ['a', '06/13/1990', 'q']
            self.ui_obj.edit_task_menu_loop(self.test_task)
            self.assertTrue(mock_ui.called)


if __name__ == '__main__':
    unittest.main()

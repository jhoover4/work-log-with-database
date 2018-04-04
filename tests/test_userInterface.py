import unittest
from unittest.mock import patch


from user_interface import UserInterface


class TestUserInterface(unittest.TestCase):

    def setUp(self):
        self.ui_obj = UserInterface()

        self.task_date_input = '06/13/1990'
        self.title_input = 'Test'
        self.time_spent_input = '15'
        self.notes_input = 'Testing'
        self.employee_input = 'Jordan'

    def test_return_to_menu(self):
        self.assertEqual("Test. Press any key to return to the menu\n",
                         self.ui_obj.return_to_menu('Test'))

    @staticmethod
    def test_date_check():
        assert UserInterface.date_check('06131990') is False
        assert UserInterface.date_check('06/13/1990') is True

    @staticmethod
    def test_time_check():
        assert UserInterface.time_check('1000') is False
        assert UserInterface.time_check('15') is True

    @patch('builtins.input')
    def test_ask_for_valid_input(self, mock):
        mock.side_effect = ['test']
        self.assertEqual(self.ui_obj.ask_for_valid_input(''), 'test')

    @patch('builtins.input')
    def test_ask_for_valid_input_with_quit(self, mock):
        mock.side_effect = ['test']
        self.assertEqual(self.ui_obj.ask_for_valid_input('', add_quit=True), 'test')

    @patch('builtins.input')
    def test_input_date(self, mock):
        mock.side_effect = ['06/13/199', '06/13/1990']
        self.assertEqual(self.ui_obj.input_date(''), self.task_date_input)

    @patch('builtins.input')
    def test_input_time(self, mock):
        mock.side_effect = ['1000', '15']
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
    def test_task_submenu(self, mock):
        mock.side_effect = ['1', 'a']
        self.assertEqual('a', self.ui_obj.task_submenu(''))

if __name__ == '__main__':
    unittest.main()

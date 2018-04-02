import unittest
from unittest.mock import patch

import user_interface
import work_log


class TestWorkLog(unittest.TestCase):

    @patch('builtins.input')
    def test_main_menu(self, mock):
        mock.side_effect = ['a']
        self.assertEqual(work_log.main_menu(), 'a')

    def test_work_log_end_loop(self):
        self.assertEqual(work_log.main_loop('q'), False)
        self.assertEqual(work_log.main_loop('c'), False)

    @patch.object(user_interface.InterfaceHelpers, 'add_task')
    def test_work_log_add_task(self, mock):
        work_log.main_loop('a')
        self.assertTrue(mock.called)

    @patch.object(user_interface.InterfaceHelpers, 'search_task_menu')
    def test_work_log_search_task(self, mock):
        work_log.main_loop('b')
        self.assertTrue(mock.called)


if __name__ == '__main__':
    unittest.main()

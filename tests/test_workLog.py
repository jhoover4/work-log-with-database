import unittest
from unittest.mock import patch

import models
from add_task import AddTask
from search_task import SearchTask
import work_log


class TestWorkLog(unittest.TestCase):

    def tearDown(self):
        try:
            models.db.close()
        except models.OperationalError:
            pass

    @patch('builtins.input')
    def test_main_menu(self, mock):
        mock.side_effect = ['wrong entry','a']
        self.assertEqual(work_log.main_menu(), 'a')

    def test_work_log_end_loop(self):
        self.assertEqual(work_log.main_loop('q'), False)
        self.assertEqual(work_log.main_loop('c'), False)

    @patch.object(AddTask, 'add_task_ui')
    def test_work_log_add_task(self, mock):
        work_log.main_loop('a')
        self.assertTrue(mock.called)

    @patch.object(SearchTask, 'search_task_ui')
    def test_work_log_search_task(self, mock):
        work_log.main_loop('b')
        self.assertTrue(mock.called)

    @patch.object(models, 'initialize_db')
    def test_run_work_log(self, mock_ui):
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ['q']
            work_log.run_work_log()
            self.assertTrue(mock_ui.called)

    @patch.object(models.db, 'close')
    def test_run_work_log(self, mock_ui):
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ['wrong input', 'q']
            work_log.run_work_log()
            self.assertTrue(mock_ui.called)

if __name__ == '__main__':
    unittest.main()

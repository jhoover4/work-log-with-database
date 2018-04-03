import unittest

import models


class TestTask(unittest.TestCase):

    def setUp(self):
        models.initialize_db()
        self.task_date = '06/13/1990'
        self.title = 'Test'
        self.time_spent = 15

        try:
            self.employee = models.Employee.get(models.Employee.name == 'Jordan')
        except models.DoesNotExist:
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


class TestEmployee(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()

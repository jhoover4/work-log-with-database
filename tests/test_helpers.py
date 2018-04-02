import unittest

import helpers


class HelpersTests(unittest.TestCase):

    @staticmethod
    def test_date_check():
        assert helpers.HelperFunctions.date_check('06131990') is False
        assert helpers.HelperFunctions.date_check('06/13/1990') is True

    @staticmethod
    def test_time_check():
        assert helpers.HelperFunctions.time_check('1000') is False
        assert helpers.HelperFunctions.time_check('15') is True


if __name__ == '__main__':
    unittest.main()

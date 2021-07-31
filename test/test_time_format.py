import unittest

from ticket_cli.time_format import *


class DateTestCase(unittest.TestCase):
    """Test for the two methods in time_format.py"""
    unformatted_1 = '2001-03-12T21:50:50Z'
    unformatted_2 = '2010-06-08T03:15:45Z'

    def test_date(self):
        formatted_date_1 = getDate(self.unformatted_1)
        self.assertEqual(formatted_date_1, '2001-03-12')
        formatted_date_2 = getDate(self.unformatted_2)
        self.assertEqual(formatted_date_2, '2010-06-08')

    def test_time(self):
        formatted_time_1 = getTime(self.unformatted_1)
        self.assertEqual(formatted_time_1, '21:50:50')
        formatted_time_2 = getTime(self.unformatted_2)
        self.assertEqual(formatted_time_2, '03:15:45')

if __name__ == '__main__':
    unittest.main()

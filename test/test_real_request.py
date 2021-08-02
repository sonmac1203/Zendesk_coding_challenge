import unittest
import requests

from ticket_cli.request import ListRequests, ShowRequest, CountTickets
from ticket_cli.config import *


class TestRequest(unittest.TestCase):
    """Tests for the class ListRequests and ShowRequest"""

    def setUp(self):
        """Create some real requests with different sets of authorization factors"""        
        # Count Request
        self.request_1 = ListRequests('', EMAIL, API_TOKEN)
        self.request_2 = ShowRequest(10, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', EMAIL, API_TOKEN)
        self.request_3 = CountTickets('ççßø˜†µåç', 'NOTANEMAILADDRESS', API_TOKEN)
    
    def test_UnicodeError_thrown(self):
        '''Test if the request raises a UnicodeError'''
        with self.assertRaises(UnicodeError):
            self.request_1.raiseUnicodeError(),
            self.request_2.raiseUnicodeError() 

    def test_InvalidURL_thrown(self):
        '''Test if the request raises a InvalidURL'''
        with self.assertRaises(requests.exceptions.InvalidURL): 
            self.request_3.raiseInvalidURL()


if __name__ == '__main__':
    unittest.main()

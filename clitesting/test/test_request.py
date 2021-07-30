from typing import List
import unittest
from clitesting.authentication import Authentication
from clitesting.request import *
from clitesting.constants import *

class TestRequest(unittest.TestCase):
    """Tests for the class ListRequests and ShowRequest"""

    def setUp(self):
        """Create some requests with different sets of authorization factors"""
        # List Requests
        self.request_1 = ListRequests()  # Default
        self.request_2 = ListRequests('notasubdomain', 'notanemailaddress@fmail.com', 'notanapitoken')  # Parameterized
        self.request_3 = ListRequests(SUBDOMAIN, 'notanemailaddress@fmail.com', 'notanapitoken')
        # Show Request
        self.request_4 = ShowRequest(50)  # Default
        self.request_5 = ShowRequest(10000000,'notasubdomain', 'notanemailaddress@fmail.com', 'notanapitoken')  # Parameterized
        self.request_6 = ShowRequest(1, SUBDOMAIN, EMAIL, 'notanapitoken')

    def test_request_status(self):
       
        """Test the getStatus() method"""
        self.status_1 = self.request_1.getStatus()
        self.assertEqual(self.status_1, 200)
        
        self.status_2 = self.request_2.getStatus()
        self.assertEqual(self.status_2, 404)
        
        self.status_3 = self.request_3.getStatus()
        self.assertEqual(self.status_3, 401)
        
        self.status_4 = self.request_4.getStatus()
        self.assertEqual(self.status_4, 200)
        
        self.status_5 = self.request_5.getStatus()
        self.assertEqual(self.status_5, 404)
        
        self.status_6 = self.request_6.getStatus()
        self.assertEqual(self.status_6, 401)

    def test_check_status(self):

        """Test the checkStatus() method"""
        self.check_1 = self.request_1.checkStatus()
        self.assertIs(self.check_1, True)
        
        self.check_2 = self.request_2.checkStatus()
        self.assertIsNot(self.check_2, True)

        self.check_3 = self.request_3.checkStatus()
        self.assertIsNot(self.check_3, True)

        self.check_4 = self.request_4.checkStatus()
        self.assertIs(self.check_4, True)

        self.check_5 = self.request_5.checkStatus()
        self.assertIsNot(self.check_5, True)

        self.check_6 = self.request_6.checkStatus()
        self.assertIsNot(self.check_6, True)


if __name__ == '__main__':
    unittest.main()

        

        
        
        
        



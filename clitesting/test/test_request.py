import unittest
import requests

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
        self.request_7 = ListRequests(SUBDOMAIN, EMAIL, API_TOKEN, 101)
        # Show Request
        self.request_4 = ShowRequest(50)  # Default
        self.request_5 = ShowRequest(10000000,'notasubdomain', 'notanemailaddress@fmail.com', 'notanapitoken')  # Parameterized
        self.request_6 = ShowRequest(1, SUBDOMAIN, EMAIL, 'notanapitoken')
        
        # Count Request
        self.request_8 = CountTickets('', EMAIL, API_TOKEN)
        self.request_9 = CountTickets('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', EMAIL, API_TOKEN)
        self.request_10 = CountTickets('ççßø˜†µåç', 'NOTANEMAILADDRESS', API_TOKEN)
    
    # Test the code returned from the request
    def test_request_code_200(self):
        """Test if the request returns code 200"""
        self.status_1 = self.request_1.getResponse().status_code
        self.assertEqual(self.status_1, 200)
        
        self.status_4 = self.request_4.getResponse().status_code
        self.assertEqual(self.status_4, 200)
        
    def test_request_code_404(self):
        """Test if the request returns code 404"""
        self.status_2 = self.request_2.getResponse().status_code
        self.assertEqual(self.status_2, 404)

        self.status_5 = self.request_5.getResponse().status_code
        self.assertEqual(self.status_5, 404)

    def test_request_code_401(self):
        """Test if the request returns code 401"""
        self.status_3 = self.request_3.getResponse().status_code
        self.assertEqual(self.status_3, 401)
    
        self.status_6 = self.request_6.getResponse().status_code
        self.assertEqual(self.status_6, 401)

    def test_request_code_400(self):
        """Test if the request returns code 400"""
        self.status_7 = self.request_7.getResponse().status_code
        self.assertEqual(self.status_7, 400)

    # Test exceptions thrown
    def test_RequestCodeError_thrown(self):
        """Test if the request raises a RequestCodeError"""
        with self.assertRaises(RequestCodeError): 
            self.request_2.raiseRequestCodeError()

    def test_UnicodeError_thrown(self):
        """Test if the request raises a UnicodeError"""
        with self.assertRaises(UnicodeError):
            self.request_8.raiseUnicodeError(),
            self.request_9.raiseUnicodeError() 

    def test_InvalidURL_thrown(self):
        """Test if the request raises a InvalidURL"""
        with self.assertRaises(requests.exceptions.InvalidURL): 
            self.request_10.raiseInvalidURL()

    # Test error reported through boolean
    def test_check_error(self):
        """Test the checkError() method"""
        self.check_1 = self.request_1.checkError()
        self.assertIsNot(self.check_1, True)
        
        self.check_2 = self.request_2.checkError()
        self.assertIs(self.check_2, True)

        self.check_3 = self.request_3.checkError()
        self.assertIs(self.check_3, True)

        self.check_4 = self.request_4.checkError()
        self.assertIsNot(self.check_4, True)

        self.check_5 = self.request_5.checkError()
        self.assertIs(self.check_5, True)

        self.check_6 = self.request_6.checkError()
        self.assertIs(self.check_6, True)

        self.check_7 = self.request_7.checkError()
        self.assertIs(self.check_7, True)      


if __name__ == '__main__':
    unittest.main()

        

        
        
        
        



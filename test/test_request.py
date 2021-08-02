import unittest
import requests

from ticket_cli.request import *
from ticket_cli.config import *


class TestRequest(unittest.TestCase):
    """Tests for the class ListRequests and ShowRequest"""

    def setUp(self):
        """Create some requests with different sets of authorization factors"""
        # List Requests
        self.request_1 = ListRequests()  # Default
        self.request_2 = ListRequests('notasubdomain', 'notanemailaddress@fmail.com', 'notanapitoken')  # Parameterized
        self.request_3 = ListRequests(SUBDOMAIN, 'notanemailaddress@fmail.com', 'notanapitoken')
        self.request_4 = ListRequests(SUBDOMAIN, EMAIL, API_TOKEN, 101)

        # False Show Request
        self.request_6 = ShowRequest(10000000, 'notasubdomain', 'notanemailaddress@fmail.com', 'notanapitoken')  # Parameterized
        self.request_7 = ShowRequest(1, SUBDOMAIN, EMAIL, 'notanapitoken')
        
        # Count Request
        self.request_8 = CountTickets('', EMAIL, API_TOKEN)
        self.request_9 = CountTickets('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', EMAIL, API_TOKEN)
        self.request_10 = CountTickets('ççßø˜†µåç', 'NOTANEMAILADDRESS', API_TOKEN)

        # Possibly appropriate Show Request
        self.request_11 = ShowRequest(1)
        self.request_12 = ShowRequest(500)
    
    # Test the code returned from the request
    def test_request_code_200(self):
        """Test if the request returns code 200"""
        self.status_1 = self.request_1.getResponse().status_code
        self.assertEqual(self.status_1, 200)

        if not self.request_11.checkError() and not self.request_12.checkError():  # If the ShowRequest succeeds
            self.assertEqual(self.request_11.getResponse().status_code, 200)
            self.assertEqual(self.request_12.getResponse().status_code, 200)
          
    def test_request_code_404(self):
        """Test if the request returns code 404"""
        self.status_2 = self.request_2.getResponse().status_code
        self.assertEqual(self.status_2, 404)

        self.status_6 = self.request_6.getResponse().status_code
        self.assertEqual(self.status_6, 404)

        if self.request_11.checkError() and not self.request_12.checkError():  # If the ShowRequest fails
            self.assertEqual(self.request_11.getResponse().status_code, 404)
            self.assertEqual(self.request_12.getResponse().status_code, 404)

    def test_request_code_401(self):
        """Test if the request returns code 401"""
        self.status_3 = self.request_3.getResponse().status_code
        self.assertEqual(self.status_3, 401)
    
        self.status_7 = self.request_7.getResponse().status_code
        self.assertEqual(self.status_7, 401)

    def test_request_code_400(self):
        """Test if the request returns code 400"""
        self.status_4 = self.request_4.getResponse().status_code
        self.assertEqual(self.status_4, 400)

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
        self.assertIs(self.check_4, True)

        self.check_6 = self.request_6.checkError()
        self.assertIs(self.check_6, True)

        self.check_7 = self.request_7.checkError()
        self.assertIs(self.check_7, True)

    # Test if the ShowRequest return the desired ticket
    def test_ticket_id(self):
        if not self.request_11.checkError(): 
            requested_id = self.request_11.id
            returned_id = self.request_11.getResponse().json()['ticket']['id']
            self.assertEqual(requested_id, returned_id)      


if __name__ == '__main__':
    unittest.main()

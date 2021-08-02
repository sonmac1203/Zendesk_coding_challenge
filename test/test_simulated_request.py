import unittest
import json


from unittest.mock import patch
from ticket_cli.request import ListRequests, ShowRequest, RequestCodeError


class MockResponse:
    '''This class initialzes a mock response'''
    def __init__(self, json_data="", status_code=None):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        '''Exclusively returns json_data to match with .json() in request.py'''
        return self.json_data


# Define Simulated Responses
def mock_list_response(url="", auth=""):
    '''Create a dummy successfull list response using json data from list_response.json'''
    with open('test/mock_json_files/list_response.json') as f:
        json_data = json.load(f)
    response = MockResponse(json_data, 200)
    return response


def mock_empty_list_response(url="", auth=""):
    '''Create a dummy successful empty list response using json data from empty_list_response.json'''
    with open('test/mock_json_files/empty_list_response.json') as f:
        json_data = json.load(f)
    response = MockResponse(json_data, 200)
    return response   


def mock_ticket_response(url="", auth=""):
    '''Create a dummy successfull ticket response using json data from ticket_response.json'''
    with open('test/mock_json_files/ticket_response.json') as f:
        json_data = json.load(f)
    response = MockResponse(json_data, 200)
    return response


def mock_ticket_fail_response(url="", auth=""):
    '''Create a dummy fail ticket response using json data from ticket_fail_response.json'''
    with open('test/mock_json_files/ticket_fail_response.json') as f:
        json_data = json.load(f)
    response = MockResponse(json_data, 404)
    return response


def mock_count_response(url="", auth=""):
    '''Create a dummy successfull count response using json data from count_response.json'''
    with open('test/mock_json_files/count_response.json') as f:
        json_data = json.load(f)
    response = MockResponse(json_data, 200)
    return response


def mock_response_400(url="", auth=""):
    '''Create a dummy fail response with 400 Error'''
    response = MockResponse(400)
    return response


def mock_response_401(url="", auth=""):
    '''Create a dummy fail response with 401 Error'''
    response = MockResponse(401)
    return response


def mock_response_404(url="", auth=""):
    '''Create a dummy fail response with 404 Error'''
    response = MockResponse(404)
    return response


# Testing
class TestMockResponse(unittest.TestCase):
    """Test the mock responses created above"""
    @patch ('ticket_cli.request.requests.get', side_effect=mock_list_response)
    def test_error_free(self, mock_func):
        '''Test if the response is error-free'''
        request = ListRequests()
        self.assertIsNot(request.checkError(), True)
    
    @patch ('ticket_cli.request.requests.get', side_effect=mock_response_404)
    def test_404Error_thrown(self, mock_func):
        '''Test if a response with 404 code will raise an exception'''
        request = ListRequests()
        with self.assertRaises(RequestCodeError):
            request.raiseRequestCodeError()

    @patch ('ticket_cli.request.requests.get', side_effect=mock_response_400)
    def test_400Error_thrown(self, mock_func):
        '''Test if a response with 400 code will raise an exception'''
        request = ListRequests()
        with self.assertRaises(RequestCodeError):
            request.raiseRequestCodeError()

    @patch ('ticket_cli.request.requests.get', side_effect=mock_response_401)
    def test_401Error_thrown(self, mock_func):
        '''Test if a response with 401 code will raise an exception'''
        request = ListRequests()
        with self.assertRaises(RequestCodeError):
            request.raiseRequestCodeError()

    @patch('ticket_cli.request.requests.get', side_effect=mock_ticket_response)
    def test_ticket_id(self, mock_func):
        '''Test if ticket id initialized is the same as ticket id returned'''
        request = ShowRequest(1)
        self.assertEqual(request.id, request.getResponse().json()['ticket']['id'])
        self.assertIsNot(request.checkError(), True)

    @patch('ticket_cli.request.requests.get', side_effect=mock_empty_list_response)
    def test_empty_list(self, mock_func):
        '''Test if the response is empty as expected'''
        request = ListRequests()
        self.assertIs(request.checkEmpty(), True)

    @patch('ticket_cli.request.requests.get', side_effect=mock_count_response)
    def test_count_response(self, mock_func):
        '''Test if getTotalTickets returns the expected number of tickets'''
        requests = ListRequests()
        self.assertEqual(requests.getTotalTickets(), 30)

    @patch('ticket_cli.request.requests.get', side_effect=mock_ticket_fail_response)
    def test_fail_ticket_response(self, mock_func):
        '''Test if the fail ticket fails as expected'''
        request = ShowRequest(500)
        self.assertIs(request.check400And404(), True)
        self.assertEqual(request.getResponse().json()['error'], 'RecordNotFound')


if __name__ == '__main__':
    unittest.main()

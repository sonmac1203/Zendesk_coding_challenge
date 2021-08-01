import requests

from ticket_cli.config import *
from ticket_cli.time_format import *
from ticket_cli.menus import printPageMenu, printEmptyPageMenu, printConnectionErrorMenu
from ticket_cli.error_display import *


class ListRequests:

    def __init__(self, subdomain = None, email = None, api_token = None, page_size = PAGE_LIMIT):
        """Set dafault/customized authentication factors, page size, and URL of the request"""
        if subdomain is not None and email is not None and api_token is not None:
            self.subdomain = subdomain
            self.email = email
            self.api_token = api_token
            self.page_size = page_size
        else:
            self.subdomain = SUBDOMAIN
            self.email = EMAIL
            self.api_token = API_TOKEN
            self.page_size = PAGE_LIMIT
        self.url = 'https://' + self.subdomain + '.zendesk.com/api/v2/tickets.json?page[size]=' + str(self.page_size)
    
    def setURL(self, url):
        """Set the URL for the request"""
        self.url = url

    def getResponse(self):
        """Return the response from the API"""
        response = requests.get(self.url, auth = (self.email + '/token' , self.api_token))
        return response

    def getTotalTickets(self):
        """Return the total number of tickets using the Count Tickets API and return None if error"""
        count = CountTickets(self.subdomain, self.email, self.api_token)
        try:
            return count.getResponse().json()['count']['value']
        except requests.exceptions.ConnectionError:
            return None

    def checkInformError(self):
        """Check for errors when making the request, catch them, and inform them"""
        try:
            response = requests.get(self.url, auth = (self.email + '/token' , self.api_token))
            if response.status_code != 200:
                raise RequestCodeError

        except requests.exceptions.ConnectionError:
            printConnectionError()
            return True
        except UnicodeError:
            printUnicodeError()
            return True
        except requests.exceptions.InvalidURL:
            printInvalidURL()
            return True
        except requests.exceptions.Timeout:
            printTimeout()
            return True
        except RequestCodeError:
            self.informError(response.status_code)
            return True
        return False

    def viewResponse(self):
        """Display the list of tickets to the console"""
        while True:  # Ask if the user wants to see the total number of tickets then call the API
            ans_ticket = input("\nDo you want to see the total number of tickets? (yes/no): ")
            if ans_ticket in ['yes', 'YES', 'Yes', 'y']:
                print("\nGetting the numnber of tickets ...")
                total_tickets = self.getTotalTickets()
                if total_tickets:
                    print("\nThere are {} tickets at the moment".format(total_tickets))
                else:
                    print("\nCannot determine the number of tickets")
                break
            elif ans_ticket in ['no', 'NO', 'No', 'n']:
                break
                        
        page_number = 1
        while True:
            while True:  # This loop helps to reload the page
                try:
                    responses_json = self.getResponse().json()  # Convert the response to json format
                    if responses_json['tickets']:
                        for ticket in responses_json['tickets']:  # Looping through the list of tickets and print each of them out
                            print("\n#{0} - Ticket with subject '{1}', requested by {2} on {3} at {4} UTC".format(
                                ticket['id'],
                                ticket['subject'],
                                ticket['requester_id'],
                                getDate(ticket['created_at']),
                                getTime(ticket['created_at'])))
                        print("\nPage {}".format(page_number))
                        break
                    else:  # Executes when there is no ticket on the page
                        printEmptyPageMenu()
                        while True:
                            ans = input("\nChoice: ")
                            if ans == '1':
                                break
                            elif ans == '2':
                                return

                # Handle ConnectionError when 
                # loading a new page fails
                except requests.exceptions.ConnectionError:
                    printConnectionErrorMenu()
                    while True:
                        ans = input("\nChoice: ")
                        if ans == '1':
                            break
                        elif ans == '2':
                            return
            while True:    
                printPageMenu()
                ans = input("\nChoice: ")
                if ans == '1':
                    self.setURL(responses_json['links']['prev'])
                    page_number -= 1
                    if page_number < 1: 
                        print("\nYou are at the first page")
                        page_number += 1
                    else: 
                        break
                elif ans == '2':
                    self.setURL(responses_json['links']['next'])
                    page_number += 1
                    if not responses_json['meta']['has_more']:
                        print("\nYou are at the final page")
                        page_number -= 1
                    else: 
                        break
                elif ans == '3':
                    return
                else: 
                    print("\nPlease choose again")

    def informError(self, status):
        """Inform the user about the code error they encounter when making the request"""
        if status == 400:
            print400Error()
        elif status == 401:
            print401Error()
        elif status == 403:
            print403Error()
        elif status == 404:
            print404Error()
        elif status == 405:
            print405Error()
        elif status == 409:
            print409Error()
        elif status == 500:
            print500Error()
        elif status == 503:
            print503Error()

    # Methods for unit testing
    def raiseRequestCodeError(self):
        """Raise RequestCodeError for unit testing"""
        response = requests.get(self.url, auth = (self.email + '/token' , self.api_token))
        if response.status_code != 200:
            raise RequestCodeError

    def raiseUnicodeError(self):
        """Raise UnicodeError for unit testing"""
        response = requests.get(self.url, auth = (self.email + '/token' , self.api_token))

    def raiseInvalidURL(self):
        """Raise InvalidURL for unit testing"""
        response = requests.get(self.url, auth = (self.email + '/token' , self.api_token))

    def checkError(self):
        """Check for errors when making the request and catch them"""
        try:
            response = requests.get(self.url, auth = (self.email + '/token' , self.api_token))
            if response.status_code != 200:
                raise RequestCodeError
        except (UnicodeError, requests.exceptions.InvalidURL, RequestCodeError) as e:
            return True
        return False


class ShowRequest(ListRequests):

    def __init__(self, id, subdomain = None, email = None, api_token = None):
        """Set default/customized authentication factors and URL of the request"""
        if subdomain is not None and email is not None and api_token is not None:
            self.subdomain = subdomain
            self.email = email
            self.api_token = api_token
        else:
            self.subdomain = SUBDOMAIN
            self.email = EMAIL
            self.api_token = API_TOKEN
        self.url = 'https://' + self.subdomain + '.zendesk.com/api/v2/tickets/' + str(id) + '.json'

    def viewResponse(self):
        """Display the chosen ticket to the console"""
        try:
            ticket_json = self.getResponse().json()  # Convert the response to json format 
            print("\n#{0} - Ticket with subject '{1}', requested by {2} on {3} at {4} UTC\n-> Description: {5}".format(  # Display the desired ticket
                ticket_json['ticket']['id'],
                ticket_json['ticket']['subject'],
                ticket_json['ticket']['requester_id'],
                getDate(ticket_json['ticket']['created_at']),
                getTime(ticket_json['ticket']['created_at']),
                ticket_json['ticket']['description']))
        except requests.exceptions.ConnectionError:
            printConnectionError()


class CountTickets(ShowRequest):

    def __init__(self, subdomain, email, api_token):
        """Set dafault/customized authentication factors and URL of the request"""
        self.subdomain = subdomain
        self.email = email
        self.api_token = api_token
        self.url = 'https://' + self.subdomain + '.zendesk.com/api/v2/tickets/count.json'

class RequestCodeError(Exception):
    """Create a custom exception called RequestCodeError"""
    pass

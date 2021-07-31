import requests

from .constants import *
from .time_format import *


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
        return count.getResponse().json()['count']['value']

    def checkInformError(self):
        """Check for errors when making the request, catch them, and inform them"""
        try:
            response = requests.get(self.url, auth = (self.email + '/token' , self.api_token))
            if response.status_code != 200:
                raise RequestCodeError
        except UnicodeError:
            print("\nError: UnicodeError")
            print("The subdomain was not appropriate. Please try again")
            return True
        except requests.exceptions.InvalidURL:
            print("\nError: InvalidURL")
            print("The request URL was invalid. Please try again")
            return True
        except requests.exceptions.Timeout:
            print("\nError: Timeut")
            print("The request timed out. Please try again")
            return True
        except RequestCodeError:
            self.informError(response.status_code)
            return True
        return False

    def checkStatus(self):
        """Check if the request was successfully completed"""
        return not self.checkInformError()

    def viewResponse(self):
        """Display the list of tickets to the console"""
        while True:  # Ask if the user wants to see the total number of tickets then call the API
            ans_ticket = input("\n\tDo you want to see the total number of tickets? (yes/no): ")
            if ans_ticket in ['yes', 'YES', 'Yes', 'y']:
                print("\n\tGetting the numnber of tickets ...")
                total_tickets = self.getTotalTickets()
                if total_tickets:
                    print("\n\tThere are {} tickets at the moment".format(total_tickets))
                else:
                    print("\n\tCannot determine the number of tickets")
                break
            elif ans_ticket in ['no', 'NO', 'No', 'n']:
                break
                        
        page_number = 1
        while True:
            while True:  # This loop helps to reload the page
                responses_json = self.getResponse().json()  # Convert the response to json format
                if responses_json['tickets']:
                    for ticket in responses_json['tickets']:  # Looping through the list of tickets and print each of them out
                        print("\n#{0} - Ticket with subject '{1}', requested by {2} on {3} at {4} UTC".format(
                            ticket['id'],
                            ticket['subject'],
                            ticket['requester_id'],
                            getDate(ticket['created_at']),
                            getTime(ticket['created_at'])))
                    print("\n\tPage {}".format(page_number))
                    break
                else: 
                    print("\nAll tickets have been displayed on the previous page")
                    print("\n\t-> Press 1 to Reload")
                    print("\t-> Press 2 to go back to MAIN MENU")
                    print("\tNOTE: Reload if you have recently added a new ticket.")
                    while True:
                        ans = input("\n\tChoice: ")
                        if ans == '1':
                            break
                        elif ans == '2':
                            return
            while True:    
                print("\n\t-> Press 1 to go to the previous page")
                print("\t-> Press 2 to go to the next page")
                print("\t-> Press 3 to go back to MAIN MENU")
                print("\tNOTE: If the next page has no ticket to display, you CANNOT go back. Sorry for this inconvenient!")
                ans = input("\n\tChoice: ")
                if ans == '1':
                    self.setURL(responses_json['links']['prev'])
                    page_number -= 1
                    if page_number < 1: 
                        print("\n\tYou are at the first page")
                        page_number += 1
                    else: 
                        break
                elif ans == '2':
                    self.setURL(responses_json['links']['next'])
                    page_number += 1
                    if not responses_json['meta']['has_more']:
                        print("\n\tYou are at the final page")
                        page_number -= 1
                    else: 
                        break
                elif ans == '3':
                    return
                else: 
                    print("\n\tPlease choose again")

    def informError(self, status):
        """Inform the user about the code error they encounter when making the request"""
        if status == 400:
            print("\nError: " + str(status) + " BAD REQUEST")
            print("Sorry, the request was invalid. Please try again")
        elif status == 401:
            print("\nError: " + str(status) + " UNAUTHORIZED")
            print("Sorry, the request did not consist of an authentication token or the authentication token was expired. Please try again")
        elif status == 403:
            print("\nError: " + str(status) + " FORBIDDEN")
            print("Sorry, you did not have permission to access the requested resource. Please try again")
        elif status == 404:
            print("\nError: " + str(status) + " NOT FOUND")
            print("Sorry, the requested resource was not found. Please try again")
        elif status == 405:
            print("\nError: " + str(status) + " METHOD NOT ALLOWED")
            print("Sorry, the HTTP method in the request was not supported by the resource. Please try again")
        elif status == 409:
            print("\nError: " + str(status) + " CONFLICT")
            print("Sorry, the request could not be completed due to a conflict. Please try again")
        elif status == 500:
            print("\nError: " + str(status) + " INTERNAL SERVER ERROR")
            print("Sorry, the request was not completed because of an internal error on the server side. Please try again")
        elif status == 503:
            print("\nError: " + str(status) + " SERVICE UNAVAILABLE")
            print("Sorry, the server was unvailable. Please try again")

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
        ticket_json = self.getResponse().json()  # Convert the response to json format 
        print("\n#{0} - Ticket with subject '{1}', requested by {2} on {3} at {4} UTC\n-> Description: {5}".format(  # Display the desired ticket
            ticket_json['ticket']['id'],
            ticket_json['ticket']['subject'],
            ticket_json['ticket']['requester_id'],
            getDate(ticket_json['ticket']['created_at']),
            getTime(ticket_json['ticket']['created_at']),
            ticket_json['ticket']['description']))


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

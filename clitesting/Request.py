import requests

from .time_format import *
from .authentication import Authentication


class ListRequests:

    def __init__(self, subdomain = None, email = None, api_token = None, page_size = None):
        """Set dafault/customized authentication factors, page size, and URL of the request"""
        if subdomain and email and api_token:
            self.subdomain = subdomain
            self.email = email
            self.api_token = api_token
            self.page_size = page_size
        else:
            authentication = Authentication()
            self.subdomain = authentication.subdomain
            self.email = authentication.email
            self.api_token = authentication.api_token
            self.page_size = 25
        self.url = 'https://' + self.subdomain + '.zendesk.com/api/v2/tickets.json?page[size]=' + str(self.page_size)
    
    def setURL(self, url):
        """Set the URL for the request"""
        self.url = url

    def getResponse(self):
        """Return the response from the API"""
        response = requests.get(
        self.url, 
        auth = (self.email + '/token' , self.api_token))
        return response

    def getStatus(self):
        """Return the status of the response"""
        status = self.getResponse().status_code
        return status
    
    def getTotalTickets(self):
        """Return the total number of tickets using the Count Tickets API and return None if error"""
        count = CountTickets()
        if count.checkStatus():
            return count.getResponse().json()['count']['value']
        else:
            count.informError()
            return None

    def checkStatus(self):
        """Check if the request was successfully completed"""
        return self.getStatus() == 200

    def viewResponse(self):
        """Display the list of tickets to the console"""
        while True: # Ask if the user wants to see the total number of tickets then call the API
            ans_ticket = input("\n\tDo you want to determine the total number of tickets? (yes/no): ")
            if ans_ticket in ['yes', 'YES', 'Yes']:
                print("\n\tGetting the numnber of tickets ...")
                total_tickets = self.getTotalTickets()
                if total_tickets:
                    print("\n\tThere are {} tickets to display".format(total_tickets))
                else:
                    print("\n\tCannot determine the number of tickets")
                break
            elif ans_ticket in ['no', 'NO', 'No']:
                break
                        
        page_number = 1
        while True:
            responses_json = self.getResponse().json()  # Convert the response to json format
            for ticket in responses_json['tickets']:
                id = ticket['id']
                subject = ticket['subject']
                requester_id = ticket['requester_id']
                date = get_date(ticket['created_at'])
                time = get_time(ticket['created_at'])
                print("\n{0}. Ticket with subject '{1}', requested by {2} on {3} at {4}".format(id, subject, requester_id, date, time))
            print("\n\tPage {}".format(page_number))
            while True:    
                print("\n\t-> Press 1 to go to the previous page")
                print("\t-> Press 2 to go to the next page")
                print("\t-> Press 3 to proceed")
                ans = input("\n\tChoice: ")
                if ans == '1':
                    self.setURL(responses_json['links']['prev'])
                    page_number -= 1
                    if page_number < 1:
                        print("\n\tYou are at the first page")
                        page_number += 1
                    else: break
                elif ans == '2':
                    self.setURL(responses_json['links']['next'])
                    page_number += 1
                    if not responses_json['meta']['has_more']:
                        print("\n\tYou are at the final page")
                        page_number -= 1
                    else: break
                elif ans == '3':
                    return
                else: 
                    print("\n\tPlease choose again")


    def informError(self):
        """Inform the client about the error they encounter"""
        if self.getStatus() == 400:
            print("\nError: " + str(self.getStatus()) + " BAD REQUEST")
            print("Sorry, the request was invalid. Please try again")
        elif self.getStatus() == 401:
            print("\nError: " + str(self.getStatus()) + " UNAUTHORIZED")
            print("Sorry, the request did not consist of an authentication token or the authentication token was expired. Please try again")
        elif self.getStatus() == 403:
            print("\nError: " + str(self.getStatus()) + " FORBIDDEN")
            print("Sorry, you did not have permission to access the requested resource. Please try again")
        elif self.getStatus() == 404:
            print("\nError: " + str(self.getStatus()) + " NOT FOUND")
            print("Sorry, the requested resource was not found. Please try again")
        elif self.getStatus() == 405:
            print("\nError: " + str(self.getStatus()) + " METHOD NOT ALLOWED")
            print("Sorry, the HTTP method in the request was not supported by the resource. Please try again")
        elif self.getStatus() == 409:
            print("\nError: " + str(self.getStatus()) + " CONFLICT")
            print("Sorry, the request could not be completed due to a conflict. Please try again")
        elif self.getStatus() == 500:
            print("\nError: " + str(self.getStatus()) + " INTERNAL SERVER ERROR")
            print("Sorry, the request was not completed because of an internal error on the server side. Please try again")
        elif self.getStatus() == 503:
            print("\nError: " + str(self.getStatus()) + " SERVICE UNAVAILABLE")
            print("Sorry, the server was unvailable. Please try again")


class ShowRequest(ListRequests):

    def __init__(self, id, subdomain = None, email = None, api_token = None):
        """Set default/customized authentication factors and URL of the request"""
        if subdomain and email and api_token:
            self.subdomain = subdomain
            self.email = email
            self.api_token = api_token
        else:
            authentication = Authentication()
            self.subdomain = authentication.subdomain
            self.email = authentication.email
            self.api_token = authentication.api_token
        self.url = 'https://' + self.subdomain + '.zendesk.com/api/v2/tickets/' + str(id) + '.json'

    def viewResponse(self):
        """Display the chosen ticket to the console"""
        ticket_json = self.getResponse().json()  # Convert the response to json format 
        subject = ticket_json['ticket']['subject']
        requester_id = ticket_json['ticket']['requester_id']
        date = get_date(ticket_json['ticket']['created_at'])
        time = get_time(ticket_json['ticket']['created_at'])
        print("\nTicket with subject '{0}', requested by {1} on {2} at {3} GMT".format(subject, requester_id, date, time))


class CountTickets(ShowRequest):

    def __init__(self, subdomain = None, email = None, api_token = None):
        """Set dafault/customized authentication factors, page size, and URL of the request"""
        if subdomain and email and api_token:
            self.subdomain = subdomain
            self.email = email
            self.api_token = api_token
        else:
            authentication = Authentication()
            self.subdomain = authentication.subdomain
            self.email = authentication.email
            self.api_token = authentication.api_token
        self.url = 'https://' + self.subdomain + '.zendesk.com/api/v2/tickets/count.json'
    

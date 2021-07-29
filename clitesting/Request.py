import requests

from .time_format import *
from .constants import *


class ListRequests:

    def __init__(self):
        self.url = 'https://' + SUBDOMAIN + '.zendesk.com/api/v2/requests.json'
    
    def getResponse(self):
        """Return the response from the API"""
        self.response = requests.get(self.url, auth=(EMAIL+ '/token' , API_TOKEN))
        return self.response

    def getStatus(self):
        """Return the status of the response"""
        self.status = self.getResponse().status_code
        return self.status
    
    def checkStatus(self):
        """Check if the request was successfully completed"""
        return self.getStatus() == 200

    def informError(self):
        """Inform the client about the error they encounter"""
        if self.status == 400:
            print("\nError: " + str(self.status) + " BAD REQUEST")
            print("Sorry, the request was invalid. Please try again")
        elif self.status == 401:
            print("\nError: " + str(self.status) + " UNAUTHORIZED")
            print("Sorry, the request did not consist of an authentication token or the authentication token was expired. Please try again")
        elif self.status == 403:
            print("\nError: " + str(self.status) + " FORBIDDEN")
            print("Sorry, you did not have permission to access the requested resource. Please try again")
        elif self.status == 404:
            print("\nError: " + str(self.status) + " NOT FOUND")
            print("Sorry, the requested resource was not found. Please try again")
        elif self.status == 405:
            print("\nError: " + str(self.status) + " METHOD NOT ALLOWED")
            print("Sorry, the HTTP method in the request was not supported by the resource. Please try again")
        elif self.status == 409:
            print("\nError: " + str(self.status) + " CONFLICT")
            print("Sorry, the request could not be completed due to a conflict. Please try again")
        elif self.status == 500:
            print("\nError: " + str(self.status) + " INTERNAL SERVER ERROR")
            print("Sorry, the request was not completed because of an internal error on the server side. Please try again")
        elif self.status == 503:
            print("\nError: " + str(self.status) + " SERVICE UNAVAILABLE")
            print("Sorry, the server was unvailable. Please try again")

    def viewResponse(self):
        """Display the list of tickets to the console"""
        responses_json = self.getResponse().json()  # Convert the response to json format
        total_tickets = responses_json['count']
        print("\nThere are {} tickets to display".format(total_tickets))  # Display the total number of tickets 
        for i in range(25):  # Show the first 25 tickets
                subject = responses_json['requests'][i]['subject']
                requester_id = responses_json['requests'][i]['requester_id']
                date = get_date(responses_json['requests'][i]['created_at'])
                time = get_time(responses_json['requests'][i]['created_at'])
                print("\n{0}. Ticket with subject '{1}', requested by {2} on {3} at {4} GMT".format(i+1, subject, requester_id, date, time))

        # The if statement below executes if there are more than 25 tickets
        # and they need to be shown in different pages
        if total_tickets > 25:
            total_pages = (total_tickets-1) // 25 + 1
            print("\n\tThere are {} pages in total".format(total_pages))
            while (True):
                print("\n\t-> Press 1 to go to other pages")
                print("\t-> Press 2 to proceed")
                ans = input("\n\tChoice: ")
                if ans == '1':
                    while True:
                        try:
                            page = int(input("\n\t-> Go to page: "))
                            if (page <= total_pages):
                                break
                            else:
                                print("\n\tPlease enter an integer no greater than {}".format(total_pages))
                        except ValueError:
                            print("\n\tPlease enter an integer no greater than {}".format(total_pages))
                        
                    for i in range(25*(page-1), 25*page):  # Display the tickets in the corresponding page
                        subject = responses_json['requests'][i]['subject']
                        requester_id = responses_json['requests'][i]['requester_id']
                        date = get_date(responses_json['requests'][i]['created_at'])
                        time = get_time(responses_json['requests'][i]['created_at'])
                        print("\n{0}. Ticket with subject '{1}', requested by {2} on {3} at {4} GMT".format(i+1, subject, requester_id, date, time))
                elif ans == '2':
                    return
                else:
                    print("\n\tPlease choose again")


class ShowRequest(ListRequests):

    def __init__(self, id):
        self.url = 'https://' + SUBDOMAIN + '.zendesk.com/api/v2/requests/' + str(id+1) + '.json'

    def viewResponse(self):
        """Display the chosen ticket to the console"""
        ticket_json = self.getResponse().json()  # Convert the response to json format 
        subject = ticket_json['request']['subject']
        requester_id = ticket_json['request']['requester_id']
        date = get_date(ticket_json['request']['created_at'])
        time = get_time(ticket_json['request']['created_at'])
        print("\nTicket with subject '{0}', requested by {1} on {2} at {3} GMT\n".format(subject, requester_id, date, time))



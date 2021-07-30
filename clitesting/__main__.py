from .request import *

def main():

    print('\nWELCOME TO THE TICKET VIEWER')
    print('\nDo you want to use the default settings or customized settings (for testing purpose)?')
    while True:
        ans_custom = getOptionStart()  # Receives '1' or '2' or 'quit'
        if ans_custom == '1':
            custom = False
        elif ans_custom == '2':
            subdomain = input("-> Please enter your Zendesk subdomain: ")
            email = input("-> Please enter your email address: ")
            api_token = input("-> Please enter your API token: ")
            custom = True
        else:
            sayGoodbye()
            return

        while True:
            ans_2 = getOptionMainMenu()  # Receives '1' or '2' or 'quit'
            if ans_2 == '1':
                if custom:
                    request = ListRequests(subdomain, email, api_token)
                else:
                    request = ListRequests()
                if (request.checkStatus()): # Check if there is any issue with the request
                    print("\n\tSuccessfully requested the tickets! Please wait ...")
                    request.viewResponse()
                else:
                    break
            elif ans_2 == '2':
                ticket_id = getTicketId()
                if custom:
                    request = ShowRequest(ticket_id, subdomain, email, api_token)
                else: 
                    request = ShowRequest(ticket_id)
                if (request.checkStatus()): # Check if there is any issue with the request
                    print("\n\tSuccessfully requested the ticket! Please wait ...")
                    request.viewResponse()
                else:
                    break
            else:
                sayGoodbye()
                return

def getTicketId():
    """Receive the ticket number to display"""
    while True:
        try:
            ans = int(input("\tPlease enter ticket id: "))
            break
        except ValueError:
            print("\n\tPlease enter an integer\n")
    return ans

# Methods to display menus and statements
def getOptionMainMenu():
    """Receive an option from the user in the MAIN MENU"""
    while True:
        print("\n\tMAIN MENU: Select one of the options below:")
        print("\t-> Press 1 to view all the tickets")
        print("\t-> Press 2 to view a single ticket")
        print("\t-> Type 'quit' to exit the program")
        ans = input("\n\tChoice: ")
        if ans in ['1', '2', 'quit', 'QUIT', 'Quit', 'Q']:
            break
        else:
            print("\n\tPlease choose again")
    return ans

def getOptionStart():
    """Receive an option from the user at the beginning of the program"""
    while True: 
        print('\n-> Press 1 to go with default settings')
        print('-> Press 2 to go with customized settings')
        print("-> Type 'quit' to exit the program")
        ans = input("\nChoice: ")
        if ans in ['1', '2', 'quit', 'QUIT', 'Quit', 'Q']:
            break
    return ans

def sayGoodbye():
    print("\nThank you for using the program. Goodbye!\n")



if __name__ == '__main__':
    main()

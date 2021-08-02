from ticket_cli.request import ListRequests, ShowRequest
from ticket_cli.menus import printMainMenu, printStartMenu


def main():

    print('\n-----------------------------WELCOME TO THE TICKET VIEWER-----------------------------')
    print('\nDo you want to use the default settings or customized settings (for testing purposes)?')
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
                if not request.checkInformError():  # Check if there is any issue with the request
                    print("\nSuccessfully requested the tickets! Please wait ...")
                    request.viewResponse()
                else:
                    break
            elif ans_2 == '2':
                ticket_id = getTicketId()
                if custom:
                    request = ShowRequest(ticket_id, subdomain, email, api_token)
                else:
                    request = ShowRequest(ticket_id)
                if not request.checkInformError(): # Check if there is any issue with the request
                    print("\nSuccessfully requested the ticket! Please wait ...")
                    request.viewResponse()
                else:
                    break
            else:
                sayGoodbye()
                return


def getTicketId():
    '''Receive the ticket number to display'''
    while True:
        try:
            ans = int(input("\nPlease enter ticket #id: "))
            break
        except ValueError:
            print("\nPlease enter an integer\n")
    return ans


# Methods to display menus and statements
def getOptionMainMenu():
    '''Receive an option from the user in the MAIN MENU'''
    while True:
        printMainMenu()
        ans = input("\nChoice: ")
        if ans in ['1', '2', 'quit', 'QUIT', 'Quit', 'Q']:
            break
        else:
            print("\nPlease choose again")
    return ans


def getOptionStart():
    '''Receive an option from the user at the beginning of the program'''
    while True: 
        printStartMenu()
        ans = input("\nChoice: ")
        if ans in ['1', '2', 'quit', 'QUIT', 'Quit', 'Q']:
            break
    return ans


def sayGoodbye():
    '''Print gooodye statements'''
    print("\nThank you for using the program. Goodbye!")
    print("Created by Son Mac, August 2021\n")


if __name__ == '__main__':
    main()

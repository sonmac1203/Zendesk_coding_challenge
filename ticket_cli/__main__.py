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

        cont = True
        while cont:
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
                while True:  # This while loop ensures user can enter #id again when 404 Not found is raises
                    ticket_id = getTicketId()
                    if ticket_id != -1: #  -1 means the user wants to go back to MAIN MENU
                        if custom:
                            request = ShowRequest(ticket_id, subdomain, email, api_token)
                        else:
                            request = ShowRequest(ticket_id)
                        if not request.checkInformError(): # Check if there is any issue with the request
                            print("\nSuccessfully requested the ticket! Please wait ...")
                            request.viewResponse()
                            break
                        elif request.check400And404():  # If the error raised is either 400 or 404, the user is allow to renter
                            continue
                        else:
                            cont = False  # Set the variable to break the loop
                            break
                    else:
                        break
            else:
                sayGoodbye()
                return


def getTicketId():
    '''Receive the ticket number to display'''
    while True:
        try:
            ans = int(input("\nPlease enter ticket #id or '-1' to go back to MAIN MENU: "))
            break
        except ValueError:
            print("\nPlease enter an integer")
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

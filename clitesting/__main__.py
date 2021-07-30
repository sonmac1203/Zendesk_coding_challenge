from .request import *


def main():
    print('\nWELCOME TO THE TICKET VIEWER\n')
    flag_ans_1 = True
    while(flag_ans_1):
        ans_1 = input("\tType 'menu' to view the options menu or type 'quit' to exit the program: ")
        if ans_1 in ['menu', 'Menu', 'MENU']:
            flag_ans_1 = False
            while (True):
                ans_2 = getOption()
                if ans_2 == '1':
                    input("\tPress Return/Enter to request the tickets ...")
                    request = ListRequests()
                    if (request.checkStatus()):
                        print("\n\tSuccessfully requested the tickets! Please wait ...")
                        request.viewResponse()
                    else:
                        request.informError()
                elif ans_2 == '2':
                    ticket_number = getTicketNumber()
                    input("\tPress enter to request the ticket ...")
                    request = ShowRequest(ticket_number)
                    if (request.checkStatus()):
                        print("\n\tSuccessfully requested the tickets! Please wait ...")
                        request.viewResponse()
                    else:
                        request.informError()
                elif ans_2 in ['quit', 'Quit', 'QUIT']:
                    print("\nThank you for using the program. Goodbye!\n")
                    return
                else:
                    print("\n\tPlease choose again")
        elif ans_1 == ['quit', 'Quit', 'QUIT']:
            flag_ans_1 = False
            print("\nThank you for using the program. Goodbye!\n")
            return
        else:
            print("\n\tPlease choose again\n")


def getOption():
    """Receive an option from the client"""
    print("\n\tMAIN MENU: Select one of the options below:")
    print("\t-> Press 1 to view all the tickets")
    print("\t-> Press 2 to view a single ticket")
    print("\t-> Type 'quit' to exit the program")
    answer = input("\n\tChoice: ")
    return answer


def getTicketNumber():
    """Receive the ticket number to display"""
    while True:
        try:
            ans = int(input("\tPlease enter ticket id: "))
            break
        except ValueError:
            print("\n\tPlease enter an integer\n")
    return ans


if __name__ == '__main__':
    main()

def printMainMenu():
    """Display options in Main Menu"""
    print("\nMAIN MENU: Select one of the options below:")
    print("-> Press 1 to view all the tickets")
    print("-> Press 2 to view a single ticket")
    print("-> Type 'quit' to exit the program")

def printStartMenu():
    """Display options in Start Menu"""
    print('\n-> Press 1 to go with default settings')
    print('-> Press 2 to go with customized settings (for testing purposes)')
    print("-> Type 'quit' to exit the program")

def printPageMenu():
    """Display options for paging"""
    print("\n-> Press 1 to go to the previous page")
    print("-> Press 2 to go to the next page")
    print("-> Press 3 to go back to MAIN MENU")
    print("NOTE: If the next page has no ticket to display, you CANNOT go back. Sorry for this inconvenience!")

def printEmptyPageMenu():
    """Display options when loaded page is empty"""
    print("\nNo ticket to display")
    print("\n-> Press 1 to Reload")
    print("-> Press 2 to go back to MAIN MENU")
    print("NOTE: Reload if you have recently added a new ticket.")
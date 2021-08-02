def print400Error():
    print("\nError: 400 BAD REQUEST")
    print("Sorry, the request was invalid. Please try again")


def print401Error():
    print("\nError: 401 UNAUTHORIZED")
    print("""Sorry, the request did not consist of an authentication token 
    or the authentication token was expired. Please try again""")


def print403Error():
    print("\nError: 403 FORBIDDEN")
    print("Sorry, you did not have permission to access the requested resource. Please try again")


def print404Error():
    print("\nError: 404 NOT FOUND")
    print("Sorry, the requested resource was not found. Please try again")


def print405Error():
    print("\nError: 405 METHOD NOT ALLOWED")
    print("Sorry, the HTTP method in the request was not supported by the resource. Please try again")


def print409Error():
    print("\nError: 409 CONFLICT")
    print("Sorry, the request could not be completed due to a conflict. Please try again")


def print500Error():
    print("\nError: 500 INTERNAL SERVER ERROR")
    print("""Sorry, the request was not completed because of 
    an internal error on the server side. Please try again""")


def print503Error():
    print("\nError: 503 SERVICE UNAVAILABLE")
    print("Sorry, the server was unvailable. Please try again")


def printConnectionError():
    print("\nError: ConnectionError")
    print("There is some issues with the connection. Please try again")


def printUnicodeError():
    print("\nError: UnicodeError")
    print("The subdomain was not appropriate. Please try again")


def printInvalidURL():
    print("\nError: InvalidURL")
    print("The request URL was invalid. Please try again")


def printTimeout():
    print("\nError: Timeut")
    print("The request timed out. Please try again")


# Zendesk_draft# Zendesk Coding Challenge 2021
This is a CLI Ticket Viewer that is built for the Coding Challenge proposed by Zendesk in August 2021.
This Ticket Viewer will:
- Connect to the Zendesk API
- Request all the tickets for your account 
- Display them in a list
- Display individual tickets details
- Page through tickets when more than 25 tickets are returned
## About
- Author: Son Tran Thien Mac
- Language: Python
- Libraries: [requests](https://docs.python-requests.org/en/master/), unittest
- Date: 07/27/21 to 08/03/21

## Installation
### Requirements and Recommendations
- Must have the lastest version of Python installed
- Must have pip installed
- Should run the program in a Python virtual environment. See [this link](https://docs.python.org/3/library/venv.html) for more details
### Procedure
1. Clone this Github repository

        $ git clone https://github.com/sonmac1203/Zendesk_coding_challenge_2021.git

2. Redirect to the root directory of this repository
3. Download and install **Requests**

        $ python -m pip install requests
    
4. Install the program

        $ pip3 install -e .
        
5. Run the program

        $ python3 ticket_cli
        
### Test
Run the unit tests

        $ python3 -m unittest
        
## Interface
![Interface](/images/interface.png)



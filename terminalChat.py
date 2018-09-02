import getpass
from termcolor import colored
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

class terminalChat():
    pusher = None
    channel = None
    chatroom = None
    clientPusher = None
    user = None
    users  = {
        "samuel": "samuel'spassword",
        "daniel": "daniel'spassword",
        "tobi": "tobi'spassword",
        "sarah": "sarah'spassword"
    }
    chatrooms = ["sports", "general", "education", "health", "technology"]

    # Now is the main entry point of application

    def main(self):
        self.login()
        self.selectChatroom()
        while True:
            self.getInput()

        
    # This function would handle logins to system. 
    # I will try integrating an API/database to verify credentials of users

    def login(self):
        username = input("Please enter your username: ")
        password = getpass.getpass("Please enter %s's Password: " % username)
        if username in self.users:
            if self.users[username] == password:
                self.user = username
            else:
                print(colored("Your password is incorrect", "red"))
                self.login()
        else:
            print(colored("No such user exists", "red"))
            self.login()

    #Now once a user logs in, let him select a chatroom to join
    
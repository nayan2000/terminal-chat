import getpass
from termcolor import colored
from dotenv import load_dotenv

from pusher import Pusher
import pysher
import os
import json
#import all the pusher app keys from env file
try:
    load_dotenv(dotenv_path='.env')
except:
    load_dotenv(dotenv_path='sample.env')

class terminalChat():
    #initially set the variables to None
    #on valid inputs from the user, they will be assigned values
    #see info.txt for what do these variables actually mean
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
    
    def selectChatroom(self):
        print(colored("Info! Available chatrooms are %s" % str(self.chatrooms), "blue"))
        chatroom = input(colored("Please select a chatroom : ", "green"))
        if chatroom in self.chatrooms:
            self.chatroom = chatroom
            self.initPusher()
        
        else:
            print(colored("Sorry! No such chatroom exists", "red"))
            self.selectChatroom()

    
    #This function will get input message from the user

    def getInput(self):
        message = input(colored("{}: ".format(self.user), "green"))
        self.pusher.trigger(self.chatroom, u'newmessage', {"user": self.user, "message": message})

    # Pusher and channel based functions below
    
    #below function initializes both Http Server Pusher as well as clientPusher 
    def initPusher(self):
        self.pusher = Pusher(
            app_id = os.getenv('PUSHER_APP_ID', None),
            key = os.getenv('PUSHER_APP_KEY', None),
            secret = os.getenv('PUSHER_APP_SECRET', None),
            cluster = os.getenv('PUSHER_APP_CLUSTER', None)
            )
        self.clientPusher = pysher.Pusher(
            os.getenv('PUSHER_APP_KEY', None),
            os.getenv('PUSHER_APP_CLUSTER', None)

        )
        self.clientPusher.connection.bind('pusher:connection_established', self.connectHandler)
        self.clientPusher.connect()


    #below functon is called once pusher has successfully established a connection
    def connectHandler(self, data):
        self.channel = self.clientPusher.subscribe(self.chatroom)
        self.channel.bind('newmessage', self.pusherCallback)

    #below function is called once pusher receives a new event
    def pusherCallback(self, message):
        message = json.loads(message)
        if message['user'] != self.user:
            print(colored(" {} : {}".format(message['user'], message['message']), "blue"))
            print(colored("{} : ".format(self.user), "green"))


if __name__ == "__main__":
    terminalChat().main()

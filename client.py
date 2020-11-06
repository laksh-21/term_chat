import socket
from information import *

class Client():

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.user_name = None
        self.client.connect(SERVER_ADDRESS)

    def main(self):
        # START ALL PROCESSES
        pass

    def send_type(self, command):
        """TO TELL SERVER WHAT KIND OF SERVICE YOU WANT"""
        message_length = get_message_length(command)
        self.client.send(message_length)
        command_encoded = command.encode(FORMAT)
        self.client.send(command_encoded)

    def send_text(self, text):
        text_length = get_message_length(text)
        self.client.send(text_length)

        text_encoded = text.encode(FORMAT)
        self.client.send(text_encoded)

    def send_message(self, message):
        """TO SEND A GLOBAL MESSAGE IN CURRENT ROOM"""
        self.send_type(TEXT_MESSAGE)
        self.send_text(message)

    def login(self):
        """LOGS THE USER IN"""
        self.send_type(LOGIN)
        user_name = input("Enter your username: ")
        self.user_name = user_name
        self.send_text(self.user_name)



c = Client()
c.login()
msg = input("Enter your message: ")
c.send_message(msg)
input()
c.send_type(DISCONNET_MESSAGE)
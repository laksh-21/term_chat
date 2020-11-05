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

    def send_message(self, message):
        """TO SEND A GLOBAL MESSAGE IN CURRENT ROOM"""
        self.send_type(TEXT_MESSAGE)
        message_length = get_message_length(message)
        self.client.send(message_length)

        message_encoded = message.encode(FORMAT)
        self.client.send(message_encoded)

    def login(self):
        pass


c = Client()
msg = input("Enter your message: ")
c.send_message(msg)
input()
c.send_message(DISCONNET_MESSAGE)
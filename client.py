import socket
import threading
from information import *

class Client():

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.user_name = None
        self.active = False
        self.client.connect(SERVER_ADDRESS)

    def main(self):
        self.login()
        self.active = True

        recieve_thread = threading.Thread(target=self.recieve_messages)
        send_thread = threading.Thread(target=self.send_messages)
        
        recieve_thread.start()
        send_thread.start()

    def send_type(self, command):
        """ TO SEND THE TYPE OF SERVICE WE WANT TO THE SERVER

        Args:
            command (str): THE TYPE OF SERVICE THE CLIENT REQUIRES
        """      

        message_length = get_message_length(command)
        self.client.send(message_length)
        command_encoded = command.encode(FORMAT)
        self.client.send(command_encoded)

    def send_text(self, text):
        """SENDS ANY TEXT TO THE SERVER

        Args:
            text (str): THE TEXT THAT NEEDS TO BE SENT
        """   

        text_length = get_message_length(text)
        self.client.send(text_length)

        text_encoded = text.encode(FORMAT)
        self.client.send(text_encoded)

    def send_messages(self):
        """TO SEND A GLOBAL MESSAGE IN CURRENT ROOM
        """        
        while self.active:
            self.send_type(TEXT_MESSAGE)
            message = input()
            self.send_text(message)
        
    def get_text(self):
        text_length = self.client.recv(LEN_LENGTH).decode(FORMAT)
        if text_length:
            text_length = int(text_length)
            text = self.client.recv(text_length).decode(FORMAT)
            return text
        else:
            return False

    def recieve_messages(self):
        """TO RECIEVE ANY MESSAGES FROM THE SERVER
        """        
        while self.active:
            text = self.get_text()
            if text:
                print(text)

    def login(self):
        """SENDS THE USER'S NAME TO THE SERVER AND SETS THE USER'S NAME
        """          
        self.send_type(LOGIN)
        user_name = input("Enter your username: ")
        self.user_name = user_name
        self.send_text(self.user_name)



c = Client()
c.main()
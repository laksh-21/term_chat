import socket
import threading
from information import *
from termcolor import cprint

class Client():

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.user_name = None
        self.active = False
        try:
            self.client.connect(SERVER_ADDRESS)
        except Exception as e:
            print("[ERROR]", e)
            exit(0)

    def main(self):
        done = self.login()
        if not done:
            return
        self.active = True

        self.recieve_thread = threading.Thread(target=self.recieve_messages)
        self.send_thread = threading.Thread(target=self.send_messages)
        
        self.recieve_thread.start()
        self.send_thread.start()

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
            message = input()
            self.send_text(message)
            if message == DISCONNECT_MESSAGE:
                self.client.close()
                self.active = False

        
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
            try:
                color = self.get_text()
                text = self.get_text()
                if text:
                    cprint(text, color)
            except:
                print("[DISCONNECTED]")

    def login(self):
        """SENDS THE USER'S NAME TO THE SERVER AND SETS THE USER'S NAME
        """          
        try:
            user_name = input("Enter your username: ")
            self.user_name = user_name
            self.send_text(self.user_name)
            return True
        except:
            print("\n[UNEXPECTED EXIT BY USER]")
            return False


c = Client()
c.main()
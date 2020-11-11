import socket
import threading
from information import *
from termcolor import cprint
import json

class Client():

    def __init__(self):
        """CONNECTS THE USER TO THE SERVER
        """        
        self.HOST_NAME      = socket.gethostname()
        self.HOST           = "192.168.43.4"
        self.PORT           = 8010
        self.CLIENT_ADDRESS = (self.HOST, self.PORT)
        self.client         = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.user_name      = None
        self.active         = False
        try:
            self.client.connect(self.CLIENT_ADDRESS)
        except Exception as e:
            print("[ERROR]", e)
            exit(0)

    def main(self):
        """SETS UP SEND AND RECIEVE THREADS AND LOGS USER IN
        """        
        done = self.login()
        if not done:
            return
        
        self.active         = True

        self.display_welcome_message()

        self.recieve_thread = threading.Thread(target=self.recieve_messages)
        self.send_thread    = threading.Thread(target=self.send_messages)
        
        self.recieve_thread.start()
        self.send_thread.start()

        while True:
            if not self.active:
                self.client.shutdown(socket.SHUT_RDWR)
                self.client.close()
                self.recieve_thread.join()
                self.send_thread.join()
                cprint("You have been disconnected.", 'magenta')
                break



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
            if message == '/disc':
                self.client.send(b'/disconnect')
                self.active = False
            elif message == '/active':
                self.client.send(b'/active_members')
            else:
                self.client.send(b'/message')
                self.send_text(message)

        
    def get_text(self):
        """GETS ANY INCOMING MESSAGE FROM SERVER

        Returns:
            str/bool: RETURNS FALSE IF NO TEXT RECIEVED, TEXT IS ANY IS RECIEVED
        """        
        text_length = self.client.recv(BUFFER).decode(FORMAT)
        if text_length:
            text_length = int(text_length)
            text = self.client.recv(text_length).decode(FORMAT)
            return text
        else:
            return False

    def get_active_users(self):
        active_user_list = self.client.recv(BUFFER)
        active_user_list = json.loads(active_user_list)
        print("Active users:")
        for number, user in enumerate(active_user_list):
            cprint("{}: {}".format(number+1, user), 'magenta')


    def recieve_messages(self):
        """TO RECIEVE ANY MESSAGES FROM THE SERVER
        """        
        while self.active:
            try:
                command = self.client.recv(BUFFER).decode(FORMAT)
                if command == '/sending_message':
                    color = self.get_text()
                    text = self.get_text()
                    cprint(text, color)
                elif command == '/active_members':
                    self.get_active_users()

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
        except Exception as e:
            print("\n[UNEXPECTED EXIT BY USER]", e)
            return False
    
    def display_welcome_message(self):
        print("Welcome! {}".format(self.user_name))
        print("You can perform the following operations by \ntyping the corresponding commands:")
        for i, command in enumerate(SPECIAL_CODES):
            cprint("{}: {}".format(i+1, command), "magenta")


c = Client()
c.main()
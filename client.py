import socket
import json
import threading
from termcolor import cprint,colored
from information import FORMAT,BUFFER,SYS_COLOR,sysprint

class Client:
    def __init__(self):
        """ Initializes the Client informations
        """        
        self.HOST       = socket.gethostbyname(socket.gethostname())
        self.PORT       = 8800
        self.ADDRESS    = (self.HOST, self.PORT)
        self.user_name  = None
        self.group_name = None
        self.active     = False
        self.disconnect = False
        self.take_input = True
        self.message    = None

    def main(self):
        """ Connects the client to the server socket aand logs the user in
            The input and output threads are created and started
        """        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect(self.ADDRESS)

        self.lock = threading.Lock()
        self.condition = threading.Condition()

        self.get_info()
        self.send_info()

        self.start_threads()

        if self.active:
            self.print_menu()

        while True:
            if not self.active:
                self.disconnect_client()
                break

    def get_input(self):
        """ Gets the user input and interprets what the user wants to do.
        """        
        while self.active:
            self.lock.acquire()
            self.message = input()
            self.lock.release()

            with self.condition:
                self.condition.notify()
            
            if self.message == '/1':
                self.send('/disconnect')
                break
            elif self.message == '/2':
                self.send('/active_members')
            elif self.message == '/3':
                self.print_menu()
            elif self.take_input:
                self.lock.acquire()
                self.send('/send_message')


    def listen(self):
        """ Listens to that the server is sending and processes all the requests.
        """        
        while True:
            message = self.get()
            if message == '/disconnect':
                self.send('.')
                self.active = False
                break
            elif message == '/send_message':
                self.send(self.message)
                self.lock.release()
            elif message == '/active_members':
                self.get_active_members()
            else:
                color = self.get()
                cprint(message, color)

    def get_active_members(self):
        """ Recieves the list of active members in current from the server and prints them
        """        
        self.send('.')
        active_members = json.loads(self.get())
        sysprint("Active members in {}".format(self.group_name))
        for num, member in enumerate(active_members):
            sysprint("{}. {}".format(num+1, member))
    
    def disconnect_client(self):
        """ Shuts down the client-server conncetion and the threads are dissolved
        """        
        self.server_socket.shutdown(socket.SHUT_RDWR)
        self.server_socket.close()
        self.end_threads()
        sysprint("Disconnected!")
    
    def start_threads(self):
        """ The unput and listen threads are created and started
        """        
        self.input_thread = threading.Thread(target=self.get_input)
        self.listen_thread = threading.Thread(target=self.listen)
        self.input_thread.start()
        self.listen_thread.start()
    
    def end_threads(self):
        """ The input and output threads are dissolved
        """        
        self.input_thread.join()
        self.listen_thread.join()
        
    def print_menu(self):
        """ Prints the command menu for the user
        """        
        sysprint("You can do these operations by typing such commands")
        sysprint("/1 : Disconnect")
        sysprint("/2 : Display Active Users")
        sysprint("/3 : Print menu again")
        sysprint("Type anything else to send a message")

    def get_info(self):
        """ Gets the User Name and Group name of the user
        """        
        cprint("Welcome to Term-Chat!")
        self.user_name = input(colored("Enter your username: ", SYS_COLOR))
        self.group_name = input(colored("Enter the Group Name: ", SYS_COLOR))
    
    def send_info(self):
        """ Sends the user information to the server in order to be logged in
        """        
        self.send(self.user_name)
        command = self.get()
        self.send(self.group_name)
        command = self.get()
        if command == '/ready':
            sysprint("You have joined the group {}!".format(self.group_name))
            self.active = True
        elif command == '/error':
            sysprint("[ERROR]")
    
    def send(self, message):
        """ Sends a particular message in byte form to the server

        Args:
            message (str): The message that needs to be sent
        """        
        self.server_socket.send(bytes(message, FORMAT))
    
    def get(self):
        """ Recieves what message has been sent by the user

        Returns:
            str: The message sent by the user
        """        
        command = self.server_socket.recv(BUFFER).decode(FORMAT)
        return command

client = Client()
client.main()
import socket
import json
import User
import Group
import threading
from termcolor import cprint
from information import BUFFER, FORMAT, sysprint

class Server:
    def __init__(self):
        """ Initializes the Server information
        """        
        self.HOST       = socket.gethostbyname(socket.gethostname())
        self.PORT       = 8800
        self.ADDRESS    = (self.HOST, self.PORT)
        self.groups     = {}
    
    def main(self):
        """ Accepts incoming connections
        """        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(self.ADDRESS)
        self.server_socket.listen()
        sysprint("Server is now Listening")
        while True:
            client_socket, address = self.server_socket.accept()
            user = self.create_user(client_socket, address)
            self.serve(user)

    def serve(self, user):
        """ Logs the new connection in and starts a thread for it.

        Args:
            user (User): The new conncetion that was incoming
        """        
        self.login_user(user)
        self.send(user, '/ready')
        threading.Thread(target=self.serve_client, args=(user,)).start()
    
    def login_user(self, user):
        """ Logs the user in and gets the group name. A new group is created
            if the group requested does not exist already.

        Args:
            user (User): The user who is supposed to be logged in
        """        
        user_name = self.get(user)
        user.user_name = user_name
        self.send(user, '/sendgroup')
        group_name = self.get(user)
        user.group_name = group_name
        if group_name in self.groups.keys():
            self.groups[group_name].connect(user)
        else:
            self.groups[group_name] = Group.Group(group_name)
            self.groups[group_name].connect(user)

    def serve_client(self, user):
        """ Manages all the operations for a patricular user

        Args:
            user (User): The user who needs to be served
        """        
        while True:
            message = self.get(user)
            if not message:
                self.group_disconnect(user)
                break
            if message == '/disconnect':
                self.disconnect_user(user)
                break
            elif message == '/send_message':
                self.broadcast_message(user)
            elif message == '/active_members':
                self.send_active_members(user)
            else:
                print("[NOT A VALID COMMAND]", message)
        self.groups[user.group_name].broadcast(user, "has left the chat.")
    
    def create_user(self, client_socket, address):
        """ A new user object is created

        Args:
            client_socket (socket.socket): The client socket of the user
            address (tuple): The address of the user

        Returns:
            User: The new user object that has been created
        """        
        user = User.User(client_socket, address)
        return user
    
    def disconnect_user(self, user):
        """ Disonnects the user from the group it was in.

        Args:
            user ([type]): [description]
        """        
        self.send(user, '/disconnect')
        self.get(user) # Unused Command
        self.group_disconnect(user)
        print("[DISCONNECTION]", user.address)
    
    def group_disconnect(self, user):
        """ Disconnects the user from the group it had joined

        Args:
            user (User): The user who needs to be disconnected
        """        
        self.groups[user.group_name].disconnect_user(user)

    def broadcast_message(self, user):
        """ Broadcasts the message sent by a user to all the other users in the group

        Args:
            user (User): The user who sent the message
        """        
        self.send(user, '/send_message')
        text = self.get(user)
        self.groups[user.group_name].broadcast(user, text)
    
    def send_active_members(self, user):
        """ Sends the list of active members to the user that requested it

        Args:
            user (User): The user who requested it
        """        
        self.send(user, '/active_members')
        self.get(user) # Unused command
        self.groups[user.group_name].send_active_users(user)

    def send(self, user, message):
        """ Sends the message to the user in byte form

        Args:
            user (User): The user who needs to be sent
            message (str): The message that is supposed to be sent
        """        
        user.client_socket.send(bytes(message, FORMAT))
    
    def get(self, user):
        """ Gets the message in byte form from the user

        Args:
            user (User): The user who we need to get the message from

        Returns:
            str: The decoded message sent by the user
        """        
        message = user.client_socket.recv(BUFFER).decode(FORMAT)
        return message


server = Server()
server.main()
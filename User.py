from random import choice
from information import COLORS

class User:
    def __init__(self, client_socket, address):
        """Initializes the User object

        Args:
            client_socket (socket.socket): The client socket
            address (tuple): The client address
        """        
        self.user_name      = None
        self.client_socket  = client_socket
        self.address        = address
        self.active         = False
        self.logged         = False
        self.color          = choice(COLORS)
        self.group_name     = None
        self.joined         = False
    
    def set_user_name(self, user_name):
        """ Sets the username of the user

        Args:
            user_name (str): The username of the user
        """        
        self.user_name = user_name
    
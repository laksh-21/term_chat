import User
import json
from information import FORMAT,BUFFER
import time

class Group:
    def __init__(self, name):
        """Initializes the Group object

        Args:
            name (str): The name of the group
        """        
        self.group_name     = name
        self.active_members = []
    
    def disconnect_user(self, user: User):
        """Removes the user from the active users list

        Args:
            user (User): The user who needs to be disconnected
        """        
        self.active_members.remove(user)

    def connect(self, user: User):
        """Adds the user to the active users list

        Args:
            user (User): THE USER WHO NEEDS TO JOIN THE ROOM
        """        
        self.active_members.append(user)

    def broadcast(self, user: User, message):
        """Broadcasts the message to all the users in the group

        Args:
            message (str): What message the user sent
            user (User): Which user send the messaGE
        """        
        for users in self.active_members:
            if users != user:
                message = "{}: {}".format(user.user_name, message)
                users.client_socket.send(bytes(message, FORMAT))
                time.sleep(0.1)
                users.client_socket.send(bytes(user.color, FORMAT))

    def send_active_users(self, user: User):
        """Sends the list of active users to the user who requested it

        Args:
            user (User): The user who requested it
        """   
        active_members = [member.user_name for member in self.active_members]
        active_user_list = json.dumps(active_members).encode(FORMAT)
        user.client_socket.send(active_user_list)


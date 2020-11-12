import User
from information import *

class Group:
    def __init__(self, name):
        self.group_name = name
        self.active_members = []
    
    def disconnect_user(self, user):
        self.active_members.remove(user)

    def connect(self, user):
        self.active_members.append(user)

    def send_color(self, user, color):
        """SENDS THE COLOR OF THE TEXT TO THE CLIENT

        Args:
            user (User): THE USER TO WHOM THE COLOR SHOULD BE SENT
            color (str): THE COLOR THAT SHOULD BE SENT
        """    

        color_length = get_message_length(color)
        user.client_socket.send(color_length)
        color_encoded = color.encode(FORMAT)
        user.client_socket.send(color_encoded)

    def send_text(self, user, text):
        """SENDS ANY TEXT TO THE CLIENT

        Args:
            text (str): THE TEXT THAT NEEDS TO BE SENT
        """   
        text_length = get_message_length(text)
        user.client_socket.send(text_length)
        text_encoded = text.encode(FORMAT)
        user.client_socket.send(text_encoded)

    def broadcast(self, message, user):
        for users in self.active_members:
            if users != user:
                users.client_socket.send(b'/sending_message')
                text = "{}: {}".format(user.user_name, message)
                self.send_color(users, user.color)
                self.send_text(users, text)
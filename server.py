import socket
import threading
import User
import Group
import json
from information import *

# GLOBAL VARIABLES
ACTIVE_USERS = []
GROUPS = {}

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "192.168.43.4"
# HOST = socket.gethostbyname(socket.gethostname())
PORT = 8010

SERVER_ADDRESS = (HOST, PORT)
server.bind(SERVER_ADDRESS)

def get_text(user):
    """GETS THE TEXT FROM A CLIENT SOCKET

    Args:
        user (User): THE USER WHO IS SENDING THE MESSAGE

    Returns:
        [str/bool]: RETURNS TEXT IF THE SERVER GOT THE MESSAGE, FALSE IF IT DIDN'T
    """    
    text_length = user.client_socket.recv(BUFFER).decode(FORMAT)
    if text_length:
        text_length = int(text_length)
        text = user.client_socket.recv(text_length).decode(FORMAT)
        return text
    else:
        return False

def user_login(user):
    """lOGS THE USER IN WITH THEIR USERNAME

    Args:
        user (User): THE USER WHO IS LOGGING IN
    """    
    user_name = get_text(user)
    if user_name:
        user.user_name = user_name
        ACTIVE_USERS.append(user)
        user.logged = True

def user_join_room(user):
    """LETS THE USER JOIN A ROOM. IF THE ROOM DOES NOT ALREADY EXIST, IT IS CREATED.

    Args:
        user (User): THE USER WHO'S JOINING THE ROOM

    Returns:
        boolean: IF THE USER JOINED OR NOT
    """    
    group_name = get_text(user)
    if group_name:
        user.group_name = group_name
        user.joined = True
        if group_name in GROUPS.keys():
            GROUPS[group_name].connect(user)
        else:
            GROUPS[group_name] = Group.Group(group_name)
            GROUPS[group_name].connect(user)
        return True
    else:
        return False
        

def disconnect_user(user):
    """REMOVES THE USER FROM THE ACTIVE USERS LIST SO THE SERVER STOPS SERVING THIS CLIENT SOCKET

    Args:
        user (User): THE USER WHO NEEDS TO BE DISCONNECTED
    """    
    user.active = False
    GROUPS[user.group_name].disconnect_user(user)
    print("[USER DISCONNECTION] {address}".format(address=user.address))

def send_active_users(user):
    """SENDS THE LIST OF ACTIVE USERS TO THE USER WHO REQUESTED IT

    Args:
        user (User): THE USER WHO REQUESTED IT
    """    
    user.client_socket.send(b'/active_members')
    active_members = [member.user_name for member in GROUPS[user.group_name].active_members]
    active_user_list = json.dumps(active_members).encode(FORMAT)
    user.client_socket.send(active_user_list)

def serve_client(user):
    """ THE SERVER SERVES THE CLIENT THAT CONNECTS TO THE SERVER

    Args:
        user (User): THE USER THAT NEEDS TO BE SERVED
    """    
    print("[NEW CONNECTION] {address}".format(address=user.address))
    user_login(user)
    if not user.logged:
        disconnect_user(user)
        return
    
    user_join_room(user)
    if not user.joined:
        disconnect_user(user)
        return

    message = "has joined the room."
    GROUPS[user.group_name].broadcast(message, user)

    while user.active:
        command = user.client_socket.recv(BUFFER).decode(FORMAT)
        if command == '/message':
            text = get_text(user)
            GROUPS[user.group_name].broadcast(text, user)
            pass
        elif command == '/disconnect':
            disconnect_user(user)
        elif command == '/active_members':
            send_active_users(user)
        else:
            disconnect_user(user)
    
    ACTIVE_USERS.remove(user)
    message = "has left the chat."
    GROUPS[user.group_name].broadcast(message, user)

def create_user(client_socket, address):
    """CREATES A User OBJECT

    Args:
        client_socket (sokcet.socket): THE CLIENT SOCKET WHICH REQUIRES SERVICE
        address (tuple): PORT OF CLIENT

    Returns:
        User: RETURNS THE OBJECT OF USER
    """    
    user = User.User(client_socket, address)
    user.active = True
    return user

def listen():
    """LISTENS FOR ANY CONNECTION REQUESTS
    """    
    server.listen()
    listening = True
    while listening:
        try:
            client_socket, address = server.accept()
            user = create_user(client_socket, address)
            thread = threading.Thread(target=serve_client, args=(user,))
            thread.start()
        except Exception as e:
            print("[FAILURE: SERVER CRASHED]", e)

print("[LISTENING] Server is now started and listening {}".format(HOST))
listen()

import socket
import threading
from information import *
import User

# GLOBAL VARIABLES
ACTIVE_USERS = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDRESS)


def get_command(user):
    """GETS WHAT KIND OF SERVICE THE USER IS ASKING FOR"""
    command_length = user.client_socket.recv(LEN_LENGTH).decode(FORMAT)
    if command_length:
        command_length = int(command_length)
        command = user.client_socket.recv(command_length).decode(FORMAT)
        return command
    else:
        return False

def get_text(user):
    text_length = user.client_socket.recv(LEN_LENGTH).decode(FORMAT)
    if text_length:
        text_length = int(text_length)
        text = user.client_socket.recv(text_length).decode(FORMAT)
        return text
    else:
        return False

def send_text(user, text):
    """SENDS ANY TEXT TO THE CLIENT

    Args:
        text (str): THE TEXT THAT NEEDS TO BE SENT
    """   

    text_length = get_message_length(text)
    user.client_socket.send(text_length)

    text_encoded = text.encode(FORMAT)
    user.client_socket.send(text_encoded)

def broadcast(user, message):
    """FOR THE MESSAGE SENT BY A USER TO BE SEEN BY EVERYONE

    Args:
        user (User): THE USER WHO SENT THE MESSAGE
        message (str): THE SESSAGE SENT BY USER
    """    

    for users in ACTIVE_USERS:
        if users != user:
            text = "{}: {}".format(user.user_name, message)
            send_text(users, text)
            
def global_message(user):
    """PUTS A TEXT MESSAGE IN THE GLOBAL CHAT

    Args:
        user (User): THE USER WHO IS SENDING THIS GLOBAL MESSAGE
    """    

    message = get_text(user)
    if message:
        print("[{who}]: {what}".format(who=user.user_name, what=message))
        broadcast(user, message)


def user_login(user):
    """lOGS THE USER IN WITH THEIR USERNAME

    Args:
        user (User): THE USER WHO IS LOGGING IN
    """    
    command = get_command(user)
    if(command == LOGIN):
        user_name = get_text(user)
        if user_name:
            user.user_name = user_name
            ACTIVE_USERS.append(user)
    # MAKE IT SO THE SERVER SENDS BACK A MESSAGE ABOUT WHAT HAPPENED

def disconnect_user(user):
    user.active = False
    user.client_socket.close()

def serve_client(user):
    print("[NEW CONNECTION] {address}".format(address=user.address))

    user_login(user)

    message = "has joined the chat."
    broadcast(user, message)

    while user.active:
        command = get_command(user)
        if command:
            if(command == TEXT_MESSAGE):
                global_message(user)
            elif(command == DISCONNET_MESSAGE):
                disconnect_user(user)
        else:
            disconnect_user(user)
    
    ACTIVE_USERS.remove(user)
    print("[USER DISCONNECTION] {address}".format(address=user.address))

    message = "has left the chat."
    broadcast(user, message)
    

def create_user(client_socket, address):
    user = User.User(client_socket, address)
    return user

def listen():
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

print("[LISTENING] Server is now started and listening {}".format(SERVER))
listen()

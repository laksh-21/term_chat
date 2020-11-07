import socket
import threading
from information import *
import User

# GLOBAL VARIABLES
ACTIVE_USERS = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDRESS)

def get_text(user):
    """GETS THE TEXT FROM A CLIENT SOCKET

    Args:
        user (User): THE USER WHO IS SENDING THE MESSAGE

    Returns:
        [str/bool]: RETURNS TEXT IF THE SERVER GOT THE MESSAGE, FALSE IF IT DIDN'T
    """    
    text_length = user.client_socket.recv(LEN_LENGTH).decode(FORMAT)
    if text_length:
        text_length = int(text_length)
        text = user.client_socket.recv(text_length).decode(FORMAT)
        return text
    else:
        return False

def send_color(user, color):
    """SENDS THE COLOR OF THE TEXT TO THE CLIENT

    Args:
        user (User): THE USER TO WHOM THE COLOR SHOULD BE SENT
        color (str): THE COLOR THAT SHOULD BE SENT
    """    

    color_length = get_message_length(color)
    user.client_socket.send(color_length)
    color_encoded = color.encode(FORMAT)
    user.client_socket.send(color_encoded)

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
            send_color(users, user.color)
            send_text(users, text)

def user_login(user):
    """lOGS THE USER IN WITH THEIR USERNAME

    Args:
        user (User): THE USER WHO IS LOGGING IN
    """    
    # command = get_command(user)
    # if(command == LOGIN):
    user_name = get_text(user)
    if user_name:
        user.user_name = user_name
        ACTIVE_USERS.append(user)
        user.logged = True

def disconnect_user(user):
    """REMOVES THE USER FROM THE ACTIVE USERS LIST SO THE SERVER STOPS SERVING THIS CLIENT SOCKET

    Args:
        user (User): THE USER WHO NEEDS TO BE DISCONNECTED
    """    
    user.active = False
    user.client_socket.close()
    print("[USER DISCONNECTION] {address}".format(address=user.address))

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

    message = "has joined the chat."
    broadcast(user, message)

    while user.active:
        text = get_text(user)
        if text:
            if(text == DISCONNECT_MESSAGE):
                disconnect_user(user)
            else:
                broadcast(user, text)
        else:
            disconnect_user(user)
    
    ACTIVE_USERS.remove(user)
    message = "has left the chat."
    broadcast(user, message)
    

def create_user(client_socket, address):
    """CREATES A User OBJECT

    Args:
        client_socket (sokcet.socket): THE CLIENT SOCKET WHICH REQUIRES SERVICE
        address (tuple): PORT OF CLIENT

    Returns:
        [type]: [description]
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

print("[LISTENING] Server is now started and listening {}".format(SERVER))
listen()

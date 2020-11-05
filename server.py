import socket
import threading
from information import *

ADDRESS = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDRESS)

def get_command(connection, address):
    command_length = connection.recv(LEN_LENGTH).decode(FORMAT)
    if command_length:
        command_length = int(command_length)
        command = connection.recv(command_length).decode(FORMAT)
        return command
    else:
        return False

def global_message(connection, address):
        message_length = connection.recv(LEN_LENGTH).decode(FORMAT)
        if message_length:
            message_length = int(message_length)
            message = connection.recv(message_length).decode(FORMAT)

            if message == DISCONNET_MESSAGE:
                print("[{who}]: is disconnecting".format(who=address))
            else:
                print("[{who}]: {what}".format(who=address, what=message))


def serve_client(connection, address):
    print("[NEW CONNECTION] {address}".format(address=address))
    connected = True
    while connected:
        command = get_command(connection, address)
        if command:
            if(command == TEXT_MESSAGE):
                global_message(connection, address)
        else:
            connected = False


def listen():
    server.listen()
    listening = True
    while listening:
        connection, address = server.accept()
        thread = threading.Thread(target=serve_client, args=(connection, address))
        thread.start()

print("[LISTENING] Server is now started and listening {}".format(SERVER))
listen()

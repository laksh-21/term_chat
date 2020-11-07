SERVER = "127.0.1.1"
LEN_LENGTH = 64
PORT = 5500
SERVER_ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
COLORS = ['red', 'green', 'blue', 'cyan']

# CODES
DISCONNECT_MESSAGE = "!DIS!"
LOGIN_SUCCESSFUL = "!LOG!"
LOGIN_UNSUCCESSFUL = "!!LOG!"


def get_message_length(message):
    message_length = str(len(message))
    message_length_encoded = message_length.encode(FORMAT)
    message_length_encoded += b' '*(LEN_LENGTH - len(message_length_encoded))
    return message_length_encoded

# GLOABAL CONSTANTS
BUFFER = 1024
FORMAT = "utf-8"
COLORS = ['red', 'green', 'blue', 'cyan']

# CODES
DISCONNECT_MESSAGE = "!DIS!"
LOGIN_SUCCESSFUL = "!LOG!"
LOGIN_UNSUCCESSFUL = "!!LOG!"


def get_message_length(message):
    """TO CALCULATE THE LENGHT OF THE MESSAGE YOU'RE ABOUT TO SEND

    Args:
        message (str): MESSAGE TO SEND

    Returns:
        str: THE LENGTH OF THE MESSAGE ELONGATED TO BUFFER SIZE
    """    
    message_length = str(len(message))
    message_length_encoded = message_length.encode(FORMAT)
    message_length_encoded += b' '*(BUFFER - len(message_length_encoded))
    return message_length_encoded

from termcolor import cprint

# GLOABAL CONSTANTS
BUFFER = 1024
FORMAT = "utf-8"
SEPERATOR = "<SEP>"
SYS_COLOR = 'magenta'
COLORS = ['red', 'green', 'blue', 'cyan']
CODE = {'disconnect'    : '/disconnect',
        'message'       : '/send_message',
        'online'        : '/active_members',
        'ready'         : '/ready',
        'error'         : '/error',
        'fileTransferS' : '/sending_file',
        'fileTransferC' : '/recieving_file',
        'all_sent'      : '/transfer_done',
        'sendFileName'  : '/send_file_name',
        'sendFile'      : '/send_file'}

def sysprint(text):
    cprint(text, SYS_COLOR)

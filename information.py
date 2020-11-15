from termcolor import cprint

# GLOABAL CONSTANTS
BUFFER = 1024
FORMAT = "utf-8"
SYS_COLOR = 'magenta'
COLORS = ['red', 'green', 'blue', 'cyan']

def sysprint(text):
    cprint(text, SYS_COLOR)

import os, sys
import time
import random 

def term_size() -> tuple:
    x = os.get_terminal_size()
    return x.coloumns, x.lines

def ctxt(colour:str, txt:str) -> str:
    code:int = 0
    colour = colour.lower()
    if colour == "red":
        code = 31
    elif colour == "green":
        code = 32
    elif colour == "yellow":
        code = 33
    elif colour == "blue":
        code = 34
    elif colour == "magenta":
        code = 35
    elif colour == "cyan":
        code = 36
    return f"\033[{code}m{txt}\033[0m"

print()


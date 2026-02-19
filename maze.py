import os, sys
import time
import random 

class coltxt:
    def __init__(self):
        self.BOLD = "\033[1m"
        self.colours = {"red":31, 
                        "green":32, 
                        "yellow":33, 
                        "blue":34, 
                        "magenta":35, 
                        "cyan":36
                        }
    
    def ctxt(self, colour:str, txt:str) -> str:
        colour = colour.lower() # LOWER REMEMBER FOR DICT!
        if colour in self.colours:
            return f"\033[{self.colours.get(colour)}m{txt}\033[0m" #Return required ANSI format to colour text 
        return txt
    
    def btxt(self, txt:str) -> str:
        return f"\033[1m{self.BOLD}\033[0m"

def term_size() -> tuple:
    x = os.get_terminal_size()
    return x.coloumns, x.lines # width, length

#Variable
ctext = coltxt()   



w,_ = term_size()
print(ctext.btxt("#"*w))
print("h")




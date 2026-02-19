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
                        "cyan":36,
                        "bred": 91,
                        }
    
    def ctxt(self, colour:str, txt:str) -> str:
        colour = colour.lower() # LOWER REMEMBER FOR DICT!
        if colour in self.colours:
            return f"\033[{self.colours.get(colour)}m{txt}\033[0m" #Return required ANSI format to colour text 
        return txt
    
    def btxt(self, txt:str) -> str:
        return f"\033[1m{txt}\033[0m"

def term_size() -> tuple:
    x = os.get_terminal_size()
    return x.columns, x.lines # width, length

#Variable
ctext = coltxt()   



w,_ = term_size()
l1 = "Welcome to Airarret by Ayan"
print(ctext.btxt("#"*w))
print(f"{ctext.btxt("# ")}{ctext.ctxt("bred",l1)}{" "*(w-(4+len(l1)))}{ctext.btxt(" #")}")
print(ctext.btxt("#"*w))

print("\r Start Game? (yes/no): ", end="")
x = input("").lower()
if x in ['y', "yes", "ya"]:
    print(ctext.ctxt("green","Okay lets go :)"))
else:
    print(ctext.btxt("Awh >:("))
import os, sys
from time import sleep
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


class GameState:
    def __init__(self):
        self.door = "🚪"
        self.path = "_"
        self.character = "🯅"
    
    def resize(self, size:int) -> None: # Ask the user to resize their terminal so game works properly
        while True:
            os.system("clear")
            w,l = term_size()
            if w < size:
                _ = input(ctext.btxt("Please resize window (horizontally), press enter once DONE"))
            else:
                break
    

    def level1(self):
        self.resize(100)
        print("")



#Variable
ctext = coltxt()   



w,_ = term_size()
l1 = "Welcome to Airarret by Ayan"
print(ctext.btxt("#"*w))
print(f"{ctext.btxt('# ')}{ctext.ctxt('bred',l1)}{' '*(w-(4+len(l1)))}{ctext.btxt(' #')}")
print(ctext.btxt("#"*w))

while True:
    print(ctext.btxt("\r Start Game? (yes/no): "), end='')
    x = input("").lower()

    if x in ['y', "yes", "ya"]:
        print(ctext.ctxt("green","Okay lets go :)"))
        break
    elif x in ['n', 'no', 'nah']:
        os.system("clear")
        print(ctext.btxt("Awh >:("))
        sys.exit()
    else:
        os.system("clear")
        print(ctext.ctxt("red", "Gibberish ? I asked yes or no question :) "))
        sleep(1)

g = GameState()
g.level1()
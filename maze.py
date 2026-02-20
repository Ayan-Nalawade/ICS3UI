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
    def ancient_characters(self, text: str, time:float) -> None:
        newtxt: str = ""
        for e in text:
            newtxt = newtxt+e
            print(f"\r {newtxt}", end='')
            sleep(time)
        print()
        

    

    def level1(self):
        global usrin1
        usrin1 = ""

        self.resize(100)
        self.ancient_characters(ctext.btxt("You are trapped inside of a cave and have to escape! One wrong move and you DIE! "), 0.05)
        os.system("clear")
        self.ancient_characters(f"{self.path*20}{self.character}{self.path*20}{self.door} {self.door} {self.door}", 0.01)
        self.ancient_characters(f"{' '*17}  You{' '*20}A  B  C", 0.01)

        print("\n\n\n\n") # Spaces :)

        self.ancient_characters(ctext.ctxt("red", "(Creepy Angel): Which door will it be? Be careful, you don't want ghosts to get you..."), 0.05)
        while True:
            usrin1 = input(ctext.btxt("Your choice? (A, B, C): ")).lower()
            if usrin1 not in ["a", "b", "c"]:
                continue
            else:
                break
        
        if 'a'==usrin1:
            print("a")
        elif 'b'==usrin1:
            print("b")
        elif 'c'==usrin1:
            print('c')





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
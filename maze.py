# Note to Mr.Schattman, using os.system("clear") to clear the terminal because CodeHS and VScode uses Linux, so theres no reason to check handling for windows, solaris or other systems
# Using Level1 as function names because I would like to add to this game later :)

import os, sys
from time import sleep
import numpy as np
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
                        "teal":36,
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
    
    def itxt(self, txt:str) -> str:
        return f"\033[3m{txt}\033[0m"


#Class Calls
ctext = coltxt()  

def term_size() -> tuple:
    x = os.get_terminal_size()
    return x.columns, x.lines # width, length


class GameState:
    def __init__(self):
        self.door = "🚪"
        self.path = "_"
        self.character = "🧍"
        self.crab = "🦀"
        self.doorchoice = ""
        self.rc, self.gch = self.updatedoorchoice() # Tells which door has a darkness (second worst choice), good choice
        self.usrin = ""

    def binomial_expansion(self, number:int) -> tuple:
        # Number will be the number an binomial expression that looks like this: (a+<number>)^2
        A = 1
        B = 2 * number
        C = number ** 2
        return (A, B, C)

    def updatedoorchoice(self) -> tuple: #Door count to a max of 3 doors so only a,b,c required
        choices = ['a', 'b', 'c']
        n = random.randint(0, 2) # Pick a random number between 0,2 and map that to a letter\
        x = random.randint(0,1) # Which door is bad after ghosts?
        self.doorchoice = choices[n]
        choices.remove(choices[n])
        badch = str(choices[x]) # Bad choice (second worst)
        choices.remove(badch)
        return badch, ''.join(choices)

    
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
        

    def level1_scene1(self):
        self.ancient_characters(ctext.itxt("You are trapped inside of a cave and have to escape! One wrong move and you DIE! "), 0.05)
        self.ancient_characters(ctext.itxt("Escape the cave without getting hurt "), 0.05)
        time.sleep(2)
        os.system("clear")

    def level1_scene2(self):
        a = time.perf_counter() # Start timer
        os.system("clear")
        self.ancient_characters(f"{self.path*20}{self.character}{self.path*20}{self.door} {self.door} {self.door}", 0.01)
        self.ancient_characters(f"{' '*17}  You{' '*20}A  B  C", 0.01)

        print("\n\n\n\n") # Spaces :)

        self.ancient_characters(ctext.ctxt("red", "(Creepy Angel): Which door will it be? Be careful, you don't want ghosts to get you... "), 0.05)


        print(self.doorchoice)
        print(self.rc)
        while True:
            self.usrin = input(ctext.btxt("Your choice? (A, B, C): ")).lower()
            if self.usrin not in ["a", "b", "c"]:
                continue
            else:
                break

        if self.doorchoice == self.usrin:
            os.system("clear")
            self.ancient_characters((ctext.ctxt("yellow",(f"Door {self.usrin.upper()} had ghosts! You have died. "))), 0.01)
            sys.exit()
        elif self.rc == self.usrin: # Second worst choice
            os.system("clear")
            self.ancient_characters(ctext.itxt("You enter the door, theres darkness everywhere. The door closes behind you. "),0.05)
            self.ancient_characters(ctext.itxt("There is a light, you walk to the light and see a weary traveler "),0.05)
            print("\n\n\n") # Spam new lines for spaces
            self.ancient_characters(ctext.ctxt("yellow","(Weary Traveler): Hello sir. Would you like to donate $5? In return I will give you some intel "),0.05)
            print("\n\n\n") # Spam new lines for spaces

            while True:
                self.usrin = input(ctext.btxt("Your choice? (Yes/No): ")).lower()
                if self.usrin not in ["yes", "no"]:
                    continue
                else:
                    os.system("clear")
                    if self.usrin == "yes":
                        if random.randint(0,1) == 1:
                            binomial_number = random.randint(0,5)
                            self.ancient_characters(ctext.ctxt("yellow","(Weary Traveler): Hehehehe, Thanks knucklehead :), Runs away "),0.03)
                            time.sleep(2)
                            os.system("clear")
                            print(ctext.itxt("A random little boy appears"))
                            self.ancient_characters(ctext.ctxt("yellow", "(Little Boy): I apologize for my dad. What did he do to you? "), 0.03)
                            self.ancient_characters(ctext.ctxt("green", "(You): He rob- That doesn't matter. Can you send me back? "), 0.03)
                            self.ancient_characters(ctext.ctxt("yellow", "(Little Boy): Yes, BUT you must solve a math problem for me. I must do this for my school "), 0.03)
                            self.ancient_characters(ctext.ctxt("yellow", f"(Little Boy): Tell me. If I am told to expand the binomial expression (a+{binomial_number})^2, "), 0.03)
                            self.ancient_characters(ctext.ctxt("yellow", "(Little Boy): What would be the values for a, b, c? (Hint: ax^2+bx+c=0, for a,b,c, looking for the coefficient) "), 0.03)

                            print("\n\n\n")

                            while True:
                                a1,b1,c1 = self.binomial_expansion(binomial_number)
                                print(a1, b1, c1)
                                valuea = int(input(ctext.btxt("(Little Boy) So whats the answer for a?: ")))
                                valueb = int(input(ctext.btxt("(Little Boy) So whats the answer for b?: ")))
                                valuec = int(input(ctext.btxt("(Little Boy) So whats the answer for c?: ")))

                                if valuea == a1 and valueb == b1 and valuec == c1:
                                    self.ancient_characters(ctext.ctxt("yellow", f"(Little Boy): YES ! That's it! I will send you back now !"), 0.03)
                                    break
                                else:
                                    self.ancient_characters(ctext.ctxt("yellow", f"(Little Boy): Hmmm! Lies! Try again if you want to go back "), 0.03)
                        else:
                            self.ancient_characters(ctext.ctxt("yellow",f"(Weary Traveler): Okay so listen. I will send you back, this time pick option {self.gch.upper()}. Vanishes "), 0.05)
                            time.sleep(2)

                        os.system("clear")
                        b = time.perf_counter() # End Timer
                        self.ancient_characters(ctext.itxt(f"You go {round(b-a,0)} seconds back "),0.05)
                        sleep(2)
                        os.system("clear")
                    else:
                        self.ancient_characters(ctext.ctxt("yellow","(Weary Traveler): Hmm? No? I don't think you buddy "),0.05)
                        print(ctext.itxt("The weary traveler stabs and robs you."))
                        self.ancient_characters(ctext.itxt("You wake up to the same 3 doors. What? Was this a dream? "), 0.03)
                        time.sleep(2)



                    break
            self.level1_scene2()
        else:
            os.system("clear")
            self.ancient_characters(ctext.itxt("teal","You enter the door, You see a playground, with crabs playing on the swings, slides, and seesaw. "),0.05)

    def level1_scene3_updte_mtrx(self, matrix:np.ndarray) -> np.ndarray: # Force np.ndarray--Ensure unwanted input not provided
        # 3 is crab, 2 is door, 1 is person, 0 is blank


        # Find where the human is currently located (if present)
        person_pos = np.argwhere(matrix == 1)
        person_row = -1
        person_col = -1
        if person_pos.size > 0:
            person_row, person_col = person_pos[0]



        # Example state [_ _ 2] -> [3 _ 2] -> [_ 3 2] -> [1 3 2] -> [3 1 2]
        uprow0 = matrix[0] # Simple swap crabs if wanted, initial state should be [3,0,2]
        if uprow0[0] == 1:
            uprow0[1] = 3
            uprow0[0] = 1
        elif uprow0[1] == 1:
            uprow0[0] = 3
            uprow0[1] = 1
        elif random.randint(0,1) == 1 and uprow0[0] == 3 and uprow0[1] == 0:
            uprow0[0] = 0
            uprow0[1] = 3
        elif random.randint(0,1) == 1 and uprow0[0] == 0 and uprow0[1] == 3:
            uprow0[0] = 3
            uprow0[1] = 0
        # elif is required because the random can be 0 or 1


        uprow1 = matrix[1] #Stands for Update Row - According to initial state this should be [0,3,0]

        uprow2 = matrix[2] #Stands for Update Row - According to initial state this should be [3,0,0]

        # Example state [ _ 1 _ ]
        freeze_row1 = False
        freeze_row2 = False
        if person_row == 1 and person_col == 1:
            freeze_row1 = True 
        if person_row == 2 and person_col == 1:
            freeze_row2 = True 
        if freeze_row1 and freeze_row2:
            return matrix
        # Handle if the player is in the middle of the matrix (position 1); If character (1) in the middle, no crab can move


        # Example states [ 1 0 0 ] -> [ 1 3 0 ] -> [ 1 0 3 ] -> [0 0 3]
        if not freeze_row1:
            crab_pos1 = np.where(uprow1 == 3)[0]
            if crab_pos1.size > 0:
                crab_col1 = int(crab_pos1[0])

                if person_row == 1 and person_col == 0:
                    if crab_col1 == 1 and random.randint(0,1) == 1 and uprow1[2] == 0:
                        uprow1[1] = 0
                        uprow1[2] = 3
                    elif crab_col1 == 2 and random.randint(0,1) == 1 and uprow1[1] == 0:
                        uprow1[2] = 0
                        uprow1[1] = 3
                elif person_row == 1 and person_col == 2:
                    if crab_col1 == 1 and random.randint(0,1) == 1 and uprow1[0] == 0:
                        uprow1[1] = 0
                        uprow1[0] = 3
                    elif crab_col1 == 0 and random.randint(0,1) == 1 and uprow1[1] == 0:
                        uprow1[0] = 0
                        uprow1[1] = 3
                else:
                    if crab_col1 == 0 and random.randint(0,1) == 1 and uprow1[1] == 0:
                        uprow1[0] = 0
                        uprow1[1] = 3
                    elif crab_col1 == 2 and random.randint(0,1) == 1 and uprow1[1] == 0:
                        uprow1[2] = 0
                        uprow1[1] = 3
                    elif crab_col1 == 1 and random.randint(0,1) == 1:
                        if random.randint(0,1) == 1 and uprow1[0] == 0:
                            uprow1[1] = 0
                            uprow1[0] = 3
                        elif uprow1[2] == 0:
                            uprow1[1] = 0
                            uprow1[2] = 3
        # Handle for the 2nd array (from the top)

        if not freeze_row2:
            crab_pos2 = np.where(uprow2 == 3)[0]
            if crab_pos2.size > 0:
                crab_col2 = int(crab_pos2[0])

                if person_row == 2 and person_col == 0:
                    if crab_col2 == 1 and random.randint(0,1) == 1 and uprow2[2] == 0:
                        uprow2[1] = 0
                        uprow2[2] = 3
                    elif crab_col2 == 2 and random.randint(0,1) == 1 and uprow2[1] == 0:
                        uprow2[2] = 0
                        uprow2[1] = 3
                elif person_row == 2 and person_col == 2:
                    if crab_col2 == 1 and random.randint(0,1) == 1 and uprow2[0] == 0:
                        uprow2[1] = 0
                        uprow2[0] = 3
                    elif crab_col2 == 0 and random.randint(0,1) == 1 and uprow2[1] == 0:
                        uprow2[0] = 0
                        uprow2[1] = 3
                else:
                    if crab_col2 == 0 and random.randint(0,1) == 1 and uprow2[1] == 0:
                        uprow2[0] = 0
                        uprow2[1] = 3
                    elif crab_col2 == 2 and random.randint(0,1) == 1 and uprow2[1] == 0:
                        uprow2[2] = 0
                        uprow2[1] = 3
                    elif crab_col2 == 1 and random.randint(0,1) == 1:
                        if random.randint(0,1) == 1 and uprow2[0] == 0:
                            uprow2[1] = 0
                            uprow2[0] = 3
                        elif uprow2[2] == 0:
                            uprow2[1] = 0
                            uprow2[2] = 3
        # Handle for the 3rd array (from the top)

        # Example states [ _ _ 1 ] -> [ _ 3 1 ] -> [ 3 _ 1 ]
        if not freeze_row1 and person_row == 1 and person_col == 2:
            if uprow1[1] == 3 and random.randint(0,1) == 1 and uprow1[0] == 0:
                uprow1[0] = 3
                uprow1[1] = 0
            elif uprow1[0] == 3 and random.randint(0,1) == 1 and uprow1[1] == 0:
                uprow1[0] = 0
                uprow1[1] = 3

        return matrix
    
    def upd_move(self, move:str, matrix:np.ndarray) -> np.ndarray: # Move error handling done by default when passed in `move`; valid inputs are l, r, u, d
        plyr_pos = np.argwhere(matrix == 1)[0] # Find location similar to [3 0] where 3 is row and 0 is coloumn number
        matrix_row_max = np.shape(matrix)[0]-1
        if move == "d":
            if plyr_pos[0] == matrix_row_max: # Bottom most row
                return matrix
            d_plyr_pos = np.argwhere(matrix == 1)[0]
            if d_plyr_pos[0] == 3:
                self.ancient_characters(ctext.itxt("There is a crab under this ! You cannot go there ! Try again "), 0.04)
                return matrix
            elif d_plyr_pos[0] != 3 and d_plyr_pos[0]




        return matrix

    
    def level1_scene3_prnt(self, matrix:np.ndarray) -> None:
        row_str = ""
        for row in matrix:  
            row_str = ""
            for v in row:
                v = int(v)
                if v == 0:   
                    row_str += f" {self.path} "
                elif v == 1: 
                    row_str += f" {self.character} "
                elif v == 2: 
                    row_str += f" {self.door} "
                else:        
                    row_str += f" {self.crab} "
            print(row_str)
            print()


    def level1_end(self):
        os.system("clear")
        self.ancient_characters(ctext.itxt("You have escaped the cave! Good Job! More Levels coming soon :) "), 0.05)




    def level1_scene3(self): 
        # 3 is crab, 2 is door, 1 is person, 0 is blank
        mtrx = np.array([[3,0,2],
                         [0,3,0],
                         [3,0,0],
                         [1,0,0]
                         ])
        # This Matrix defines the game board and the state/position of crab, door, person, and blank . Its not put in the __init__ function on purpose.

        # self.ancient_characters(ctext.itxt("INSTRUCTIONS: "), 0.03)
        # self.ancient_characters(ctext.itxt("1. Enter l (left), r (right), u (up), d (down) when asked to move character "), 0.03)
        # self.ancient_characters(ctext.itxt("2. The crabs move so you must be careful to not hit a crab! "), 0.03)
        # print("\n\n")
        # input("Press ENTER to begin")
        # os.system("clear")

        self.upd_move("d", mtrx)



        # self.level1_end()


    def level1(self):
        self.resize(100)

        # self.level1_scene1()

        # self.level1_scene2()

        self.level1_scene3()

# w,_ = term_size()
# l1= "Welcome to Airarret by Ayan"
# print(ctext.btxt("#"*w))
# print(f"{ctext.btxt('# ')}{ctext.ctxt('bred',l1)}{' '*(w-(4+len(l1)))}{ctext.btxt(' #')}") # Compute spaces, #, and text to make sure it works with the print line before and after
# print(ctext.btxt("#"*w))

# while True:
#     print(ctext.btxt("\r Start Game? (yes/no): "), end='')
#     x = input("").lower()

#     if x in ['y', "yes", "ya"]:
#         print(ctext.ctxt("green","Okay lets go :)"))
#         break
#     elif x in ['n', 'no', 'nah']:
#         os.system("clear")
#         print(ctext.btxt("Awh >:("))
#         sys.exit()
#     else:
#         os.system("clear")
#         print(ctext.ctxt("red", "Gibberish ? I asked yes or no question :) "))
#         sleep(1)

g = GameState()
g.level1()
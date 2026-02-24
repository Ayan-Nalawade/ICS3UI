# Note to Mr.Schattman, using os.system("clear") to clear the terminal because CodeHS and VScode uses Linux, so theres no reason to check handling for windows, solaris or other systems
# Using Level1 as function names because I would like to add to this game later :)

import os, sys
from time import sleep
import numpy as np
import time
import random

class coltxt:
    def __init__(self):
        self.colours = {"red":31, 
                        "green":32, 
                        "yellow":33, 
                        "blue":34, 
                        "magenta":35, 
                        "teal":36,
                        "cyan":36,
                        "bred": 91,
                        }
        # Define colours for ANSII text. for example for bred (bright red) the code is 91 (this is defined by the OS)
        

    
    def ctxt(self, colour:str, txt:str) -> str:
        """
        This function colours the text printed on the terminal (the print command must be done on its own it just returns the format required to colour)

        args:
        `colour`: This is the colour that the user wants based on the self.colours dictionary
        `txt`: The text the user WANTS to colour
        """
        colour = colour.lower() # LOWER REMEMBER FOR DICT!
        if colour in self.colours:
            return f"\033[{self.colours.get(colour)}m{txt}\033[0m" #Return required ANSI format to colour text 
        return txt
    
    def btxt(self, txt:str) -> str:
        """
        This function bolds the text printed on the terminal; DOESN'T print it BUT returns the format required to bold text

        args:
        `txt`: This text the user WANTS to colour
        """
        return f"\033[1m{txt}\033[0m"
    
    def itxt(self, txt:str) -> str:
        return f"\033[3m{txt}\033[0m"


#Class Calls
ctext = coltxt()  

def term_size() -> tuple:
    """
    This function will crab the terminal size from the function `os.get_terminal_size()`
    Will return a tuple in the format (width, length)
    """
    x = os.get_terminal_size()
    return x.columns, x.lines # width, length


class GameState:
    def __init__(self):
        self.door = "🚪"         # Define door
        self.path = "_"          # Define path (empty spots)
        self.character = "🧍"    # Define Character 
        self.crab = "🦀"         # Define Crab
        self.doorchoice = ""  # Define Door choice with the ghosts!
        self.rc, self.gch = self.updatedoorchoice()      # Tells which door has a darkness (second worst choice), good choice
        self.usrin = ""       # Define what door choice the user picks
        self.level1_complete:bool = False                # Is the level 1 complete?
        self.cnt = 0          # Count how mnay times the user picked ghost door
        

    def binomial_expansion(self, number:int) -> tuple:
        """
        Takes in a number for the function: (a+number)^2. Using the formula a^2 + b^2 + 2ab. The value of a must be 1 always, b is 2ab or 2(number)
        and c is c^2 or number^2
        returns the tuple with values for A B and C 
        """
        # Number will be the number an binomial expression that looks like this: (a+<number>)^2
        A = 1
        B = 2 * number
        C = number ** 2
        return (A, B, C)

    def updatedoorchoice(self) -> tuple: #Door count to a max of 3 doors so only a,b,c required
        """
        This function checks which choice is good, bad, and which choice cuts to scene 2 (or is the best choice)

        Returns the bad choice and then the best choice
        """
        choices = ['a', 'b', 'c']              # Possible choices
        n = random.randint(0, 2)               # Pick a random number between 0,2 and map that to a letter\
        x = random.randint(0,1)                # Which door is bad after ghosts?
        self.doorchoice = choices[n]
        choices.remove(choices[n])
        badch = str(choices[x])                # Bad choice (second worst)
        choices.remove(badch)
        return badch, ''.join(choices)

    
    def resize(self, size:int) -> None: # Ask the user to resize their terminal so game works properly
        """
        This function handles the resizing processes where the user must resize the terminal in order for the game to work properly.

        args:
        `size`: Integer value that tells what the size of the terminal (horizontally) must be
        """
        while True:                 # Repeat until the user resizes the terminal so it fits the `size` requirement
            os.system("clear")      # Keep clearing the terminal so its not spamming lines
            w,l = term_size()       # split into w,l as term_size() returns tuple. l is not required right now HOWEVER its there incase its required in the future
            if w < size:            # Repeat until the terminal isn't resized enough
                _ = input(ctext.btxt("Please resize window (horizontally), press enter once DONE"))
            else:
                break


    def ancient_characters(self, text: str, time:float) -> None:
        """
        The main function to print the text. It works by overwriting the text 1 character at a time at a time interval to make it look realistic

        args:
        `text`: This is the text that must be printed one character at a time
        `time`: This is the time interval for each character (before its printed)
        """
        # The function works by having a variable `newtxt`. theres a for loop that iterates over each character of 'text' and adds the character
        # to `newtxt` which then gets printed and the cursor is returned to the front and the line is overwritten over and over until the text is done
        newtxt: str = ""
        for e in text:
            newtxt = newtxt+e
            print(f"\r {newtxt}", end='')
            sleep(time)
        print()
        

    def level1_scene1(self):
        """
        This is one of the scenes in level1. This is at the start
        """
        # Introduction; Talks about what the goal of the game is and what must NOT be done (dying)
        self.ancient_characters(ctext.itxt("You are trapped inside of a cave and have to escape! One wrong move and you DIE! "), 0.05)
        self.ancient_characters(ctext.itxt("Escape the cave without getting hurt "), 0.05)
        sleep(2)                  # Sleep to let the user read
        os.system("clear")        # Clear the screen

    def level1_scene2(self):
        """
        This is the second scene of level 1. This has the door level where it prints out the door and the introduction for little boy,
        weary traveler, and little angel. This is a solid chunk of the game right now
        """
        a = time.perf_counter() # Start timer (starts counter to see how long it takes)
        os.system("clear")      # Clear the terminal
        self.ancient_characters(f"{self.path*20}{self.character}{self.path*20}{self.door} {self.door} {self.door}", 0.01) # Print the board 
        self.ancient_characters(f"{' '*17}  You{' '*20}A  B  C", 0.01) # Print the door choice (A, B, C)

        print("\n\n\n\n") # Spaces :)

        # Introduction to the creepy angel. 
        self.ancient_characters(ctext.ctxt("red", "(Creepy Angel): Which door will it be? Be careful, you don't want ghosts to get you... "), 0.05)


        # print(f"Ghost door {self.doorchoice}")                            # DEBUG TO FIND DOOR WITH GHOSTS
        # print(f"Door with darkness room {self.rc}")                       # DEBUG TO FIND DOOR WITH SECOND BEST CHOICE/ DARKNESS ROOM

        while True: # Keep asking for user input until they respond with a, b, or c
            self.usrin = input(ctext.btxt("Your choice? (A, B, C): ")).lower()
            if self.usrin not in ["a", "b", "c"]:
                continue
            else:
                break

        
        if self.doorchoice == self.usrin: # If the user picks the door with ghosts
            os.system("clear")
            # We let the user pick the door 2 times in total before the ghosts kill them. 
            if self.cnt >= 2: # Check how many times the user picked the door
                # The ghosts killed the user
                self.ancient_characters((ctext.ctxt("yellow",(f"Door {self.usrin.upper()} had ghosts! You were unable to escape this time and died "))), 0.01)
                sys.exit() # Call safe program exit
            else:
                # Ghosts but you escaped somehow :)
                self.ancient_characters((ctext.ctxt("yellow",(f"Door {self.usrin.upper()} had ghosts! You run out! "))), 0.01)
    
            sleep(2) # Sleep to let the user read
            self.cnt += 1 # Progress the count by one
            self.level1_scene2() # Recall this function to let the user retry picking the doors
            
        elif self.rc == self.usrin: # Second worst choice (darkness room)
            os.system("clear")

            # Explaination of where the user is
            self.ancient_characters(ctext.itxt("You enter the door, theres darkness everywhere. The door closes behind you. "),0.05)
            self.ancient_characters(ctext.itxt("There is a light, you walk to the light and see a weary traveler "),0.05)

            print("\n\n\n") # Spam new lines for spaces

            # Introduction of "weary traveler"
            self.ancient_characters(ctext.ctxt("yellow","(Weary Traveler): Hello sir. Would you like to donate $5? In return I will give you some intel "),0.05)
            
            print("\n\n\n") # Spam new lines for spaces


            while True: # Check if user is giving what is wanted
                self.usrin = input(ctext.btxt("Your choice? (Yes/No): ")).lower() # Does the user want to donate $5?
                if self.usrin not in ["yes", "no"]: # If the user says anything BUT yes or no
                    continue
                else:
                    os.system("clear") # Clear up the terminal

                    if self.usrin == "yes":  # If the user picks yes
                        bgate = False                                  # DEBUG: Allow this section to run regardless 
                        if random.randint(0,1) == 1 or bgate == True: # Check if DEBUG is wanted or if random number is 1

                            binomial_number = random.randint(0,5) # IN the format (a+b)^2, what should be b value?

                            # Weary traveller robs us
                            self.ancient_characters(ctext.ctxt("yellow","(Weary Traveler): Hehehehe, Thanks knucklehead :), Runs away "),0.03)
                            sleep(2)
                            os.system("clear") # Clear the terminal

                            # Introduction of the little boy; with character and little boy conversation. 
                            print(ctext.itxt("A random little boy appears"))
                            self.ancient_characters(ctext.ctxt("yellow", "(Little Boy): I apologize for my dad. What did he do to you? "), 0.03)
                            self.ancient_characters(ctext.ctxt("green", "(You): He rob- That doesn't matter. Can you send me back? "), 0.03)
                            self.ancient_characters(ctext.ctxt("yellow", "(Little Boy): Yes, BUT you must solve a math problem for me. I must do this for my school "), 0.03)
                            self.ancient_characters(ctext.ctxt("yellow", f"(Little Boy): Tell me. If I am told to expand the binomial expression (a+{binomial_number})^2, "), 0.03)
                            self.ancient_characters(ctext.ctxt("yellow", "(Little Boy): What would be the values for a, b, c? (Hint: ax^2+bx+c=0, for a,b,c, looking for the coefficient) "), 0.03)

                            print("\n\n\n")  # Add new lines

                            while True: # We want the user to give out the correct values, will iterate until correct values given
                                a1,b1,c1 = self.binomial_expansion(binomial_number)  # Do the polynomial expansion
                                # print(a1, b1, c1)                                      # DEBUG TO FIND VALUES

                                try: # Ask for values and make sure they aren't random values and just integers
                                    valuea = int(input(ctext.btxt("(Little Boy) So whats the answer for a?: ")))
                                    valueb = int(input(ctext.btxt("(Little Boy) So whats the answer for b?: ")))
                                    valuec = int(input(ctext.btxt("(Little Boy) So whats the answer for c?: ")))
                                except ValueError:
                                    continue

                                if valuea == a1 and valueb == b1 and valuec == c1: # If all values match the little boy sends character back
                                    self.ancient_characters(ctext.ctxt("yellow", f"(Little Boy): YES ! That's it! I will send you back now ! Oh yeah also the correct door is {self.gch.upper()} "), 0.03)
                                    sleep(2)
                                    break
                                else: # If values don't match, the little boy will give you another chance (unlimited chances)
                                    self.ancient_characters(ctext.ctxt("yellow", f"(Little Boy): Hmmm! Lies! Try again if you want to go back "), 0.03)
 
                        else: # If the random function doesn't say 1, then the character gets the correct door value
                            self.ancient_characters(ctext.ctxt("yellow",f"(Weary Traveler): Okay so listen. I will send you back, this time pick option {self.gch.upper()}. Vanishes "), 0.05)
                            sleep(2)

                        os.system("clear")
                        b = time.perf_counter() # End Timer (a being start timer. It will count how long it took for the user to get here)
                        self.ancient_characters(ctext.itxt(f"You go {round(b-a,0)} seconds back "),0.05) # Print out "going back x seconds" where x is the time it took for the user to get here
                        sleep(2)
                        os.system("clear")
                    
                    else: # If the user responds "no" to when weary traveller asks for money; he will stab and run away
                        self.ancient_characters(ctext.ctxt("yellow","(Weary Traveler): Hmm? No? I don't think you buddy "),0.05)
                        print(ctext.itxt("The weary traveler stabs and robs you."))
                        self.ancient_characters(ctext.itxt("You wake up to the same 3 doors. What? Was this a dream? "), 0.03)
                        sleep(2)



                    break

            # Regardless of what happenes we want to rerun the function to give the user another try (if the user dies, we call safe os exit to quit program)
            self.level1_scene2() 
        
        else: # If the user picks the best possible door `gch`
            # We introduce--CRABS!
            os.system("clear")
            self.ancient_characters(ctext.itxt("You enter the door, You see a playground, with crabs playing on the swings, slides, and seesaw. ") ,0.05)
            self.ancient_characters(ctext.itxt("The crabs spotted you! Now they scurry over to block the exit! Try to escape quickly! ") ,0.05)
            sleep(2)
            os.system("clear")

    def level1_scene3_updte_mtrx(self, matrix:np.ndarray) -> np.ndarray: # Force np.ndarray--Ensure unwanted input not provided
        """
        Update the crab positions each time; this function accounts for blank spaces, and characters being in the way

        args:
        `matrix`: This is the board itself
        """
        # 3 is crab, 2 is door, 1 is person, 0 is blank (matrix value)


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
    
    def level1_end(self):
        """
        Level end. Currently it says the game was completed. But adding levels, level1_end would print something else
        """
        os.system("clear")
        self.ancient_characters(ctext.itxt("You have escaped the cave! Good Job! "), 0.05)
        sys.exit()
    
    def upd_move(self, move:str, matrix:np.ndarray) -> np.ndarray: # Move error handling done by default when passed in `move`; valid inputs are l, r, u, d
        """
        This function updates the move. It accounts for if the character wants to move where a crab is, if its a legal move, and if the move touches the door
        
        args:
        `move`: This is the move (correct moves from the user must be filtered before this function), takes l,r,u, or d values
        `matrix`: This is the game board itself
        
        It returns the matrix itself.
        """
        

        plyr_pos = np.argwhere(matrix == 1)[0] # Find location similar to [3 0] where 3 is row and 0 is coloumn number
        matrix_row_max = np.shape(matrix)[0]-1 # Find the shape of the matrix the "-1" because its index 1 (starts from 1)
        matrix_col_max = np.shape(matrix)[1]-1
        if move == "d":
            if plyr_pos[0] == matrix_row_max: # Bottom most row
                return matrix
            

            d_plyr_pos = np.array([plyr_pos[0]+1, plyr_pos[1]]) # Position directly under player
            if matrix[d_plyr_pos[0]][d_plyr_pos[1]] == 3:
                os.system("clear")
                self.ancient_characters(ctext.itxt("There is a crab under this ! You cannot go there ! Try again "), 0.04)
                sleep(2)
                return matrix
            
            elif matrix[d_plyr_pos[0]][d_plyr_pos[1]] != 3 and matrix[d_plyr_pos[0]][d_plyr_pos[1]] != 2:
                matrix[plyr_pos[0]][plyr_pos[1]] = 0
                matrix[d_plyr_pos[0]][d_plyr_pos[1]] = 1

            elif matrix[d_plyr_pos[0]][d_plyr_pos[1]] == 2:
                matrix[plyr_pos[0]][plyr_pos[1]] = 0
                matrix[d_plyr_pos[0]][d_plyr_pos[1]] = 1

            else:
                os.system("clear")
                self.ancient_characters(ctext.btxt("There is a critical error with logic of matrix. Please restart code :) or ask dev for help with 'logic of matrix'"), 0.03)
                sys.exit()

        elif move == "u":
            if plyr_pos[0] == 0: # Top most row
                return matrix
            u_plyr_pos = np.array([plyr_pos[0]-1, plyr_pos[1]]) # Position directly above player
            if matrix[u_plyr_pos[0]][u_plyr_pos[1]] == 3:
                os.system("clear")
                self.ancient_characters(ctext.itxt("There is a crab above this ! You cannot go there ! Try again "), 0.04)
                sleep(2)
                return matrix
            
            elif matrix[u_plyr_pos[0]][u_plyr_pos[1]] != 3 and matrix[u_plyr_pos[0]][u_plyr_pos[1]] != 2:
                matrix[plyr_pos[0]][plyr_pos[1]] = 0
                matrix[u_plyr_pos[0]][u_plyr_pos[1]] = 1

            elif matrix[u_plyr_pos[0]][u_plyr_pos[1]] == 2:
                matrix[plyr_pos[0]][plyr_pos[1]] = 0
                matrix[u_plyr_pos[0]][u_plyr_pos[1]] = 1
                self.level1_end()
                self.level1_complete = True

            else:
                os.system("clear")
                self.ancient_characters(ctext.btxt("There is a critical error with logic of matrix. Please restart code :) or ask dev for help with 'logic of matrix'"), 0.03)
                sys.exit()

        elif move == "l":
            if plyr_pos[1] == 0: # Left most column
                return matrix
            
            l_plyr_pos = np.array([plyr_pos[0], plyr_pos[1]-1]) # Position directly left of player
            if matrix[l_plyr_pos[0]][l_plyr_pos[1]] == 3:
                os.system("clear")
                self.ancient_characters(ctext.itxt("There is a crab on the left ! You cannot go there ! Try again "), 0.04)
                sleep(2)
                return matrix
            
            elif matrix[l_plyr_pos[0]][l_plyr_pos[1]] != 3 and matrix[l_plyr_pos[0]][l_plyr_pos[1]] != 2:
                matrix[plyr_pos[0]][plyr_pos[1]] = 0
                matrix[l_plyr_pos[0]][l_plyr_pos[1]] = 1

            elif matrix[l_plyr_pos[0]][l_plyr_pos[1]] == 2:
                matrix[plyr_pos[0]][plyr_pos[1]] = 0
                matrix[l_plyr_pos[0]][l_plyr_pos[1]] = 1
                self.level1_end()
                self.level1_complete = True

            else:
                os.system("clear")
                self.ancient_characters(ctext.btxt("There is a critical error with logic of matrix. Please restart code :) or ask dev for help with 'logic of matrix'"), 0.03)
                sys.exit()

        elif move == "r":
            if plyr_pos[1] == matrix_col_max: # Right most column
                return matrix
            
            r_plyr_pos = np.array([plyr_pos[0], plyr_pos[1]+1]) # Position directly right of player
            if matrix[r_plyr_pos[0]][r_plyr_pos[1]] == 3:
                os.system("clear")
                self.ancient_characters(ctext.itxt("There is a crab on the right ! You cannot go there ! Try again "), 0.04)
                sleep(2)
                return matrix
            
            elif matrix[r_plyr_pos[0]][r_plyr_pos[1]] != 3 and matrix[r_plyr_pos[0]][r_plyr_pos[1]] != 2:
                matrix[plyr_pos[0]][plyr_pos[1]] = 0
                matrix[r_plyr_pos[0]][r_plyr_pos[1]] = 1

            elif matrix[r_plyr_pos[0]][r_plyr_pos[1]] == 2:
                matrix[plyr_pos[0]][plyr_pos[1]] = 0
                matrix[r_plyr_pos[0]][r_plyr_pos[1]] = 1
                self.level1_end()
                self.level1_complete = True

            else:
                os.system("clear")
                self.ancient_characters(ctext.btxt("There is a critical error with logic of matrix. Please restart code :) or ask dev for help with 'logic of matrix' "), 0.03)
                sys.exit()
        else:
                os.system("clear")
                self.ancient_characters(ctext.btxt("The programmer made an oopsie with upd_move :) Please ask them to fix it :) "), 0.03)
                sys.exit()

        return matrix

    
    def level1_scene3_prnt(self, matrix:np.ndarray) -> None:
        """
        This prints out the board based on the matrix

        args:
        `matrix`: The matrix for the board that gets converted to emojies and printed out
        """
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


    def level1_scene3(self): 
        """
        The 3rd scene. In this scene the crab game is played AND instructions
        """
        # 3 is crab, 2 is door, 1 is person, 0 is blank
        mtrx = np.array([[3,0,2],
                         [0,3,0],
                         [3,0,0],
                         [1,0,0]
                         ])
        # This Matrix defines the game board and the state/position of crab, door, person, and blank . Its not put in the __init__ function on purpose.

        self.ancient_characters(ctext.itxt("INSTRUCTIONS: "), 0.03)
        self.ancient_characters(ctext.itxt("1. Enter l (left), r (right), u (up), d (down) when asked to move character "), 0.03)
        self.ancient_characters(ctext.itxt("2. The crabs move so you must be careful to not hit a crab! "), 0.03)
        print("\n\n")
        input("Press ENTER to begin")
        os.system("clear")

        while self.level1_complete != True:
            os.system("clear")
            self.level1_scene3_prnt(mtrx)
            self.level1_scene3_updte_mtrx(mtrx)
            while True:
                a = input("Where to move? Enter l (left), r (right), u (up) or d (down) : ")
                a = a.lower()
                a = a.strip(" ")
                if a not in ["left", "right", "up", "down", "l", "r", "u", "d"]: # Check if the input from the user is in the list
                    continue
                elif a == "left":
                    a = "l"
                elif a == "right":
                    a = "r"
                elif a == "up":
                    a = "u"
                elif a == "down":
                    a = "d"
                # If neither, then it must be a one of l, r, u, d
                break
            self.upd_move(a, mtrx)




    def level1(self):
        """
        Calls all the functions in the function
        """
        self.resize(100)

        self.level1_scene1()

        self.level1_scene2()

        self.level1_scene3()

# Print out the "#" and the text
w,_ = term_size()
l1= "Welcome to Airarret by Ayan"
print(ctext.btxt("#"*w))
print(f"{ctext.btxt('# ')}{ctext.ctxt('bred',l1)}{' '*(w-(4+len(l1)))}{ctext.btxt(' #')}") # Compute spaces, #, and text to make sure it works with the print line before and after
print(ctext.btxt("#"*w))

# The game 
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
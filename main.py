import tkinter as tk
from time import sleep
from random import *
from math import *

from PIL import Image, ImageTk


r = tk.Tk()

WIDTH = r.winfo_screenwidth() # x
HEIGHT = r.winfo_screenheight() # y
if WIDTH > 1000: 
    WIDTH = 1000
if HEIGHT > 1000:
    HEIGHT = 1000
# Check if the HEIGHT or WIDTH is greater than 1000, if so make it 1000 so it doesn't take up the entire screen
if WIDTH < 500:
    WIDTH = 600
if HEIGHT < 500:
    HEIGHT = 600
# Account for minimum 500, so the board isn't drawn in a 1x1 pixel box if the user wants to be fancy
f = tk.Canvas(r, width=WIDTH, height=HEIGHT, background="#FFFFFF")
f.pack()

class Board:
    def __init__(self):
        self.sqh = HEIGHT//6 # Get the square height required for each square of the board
        self.sqw = WIDTH//6 # Get the square width required for each square of the board
        self.board_data = {} # x,y,piece (None=Nothing, True=Player, False, Bot)
    
    def __progression(self, character) -> str:
        if character == "None":  # Guard
            return "None"
        one, two = character[0], character[1]
        one = ord(one)
        if one == 70:
            if two == '1': 
                return "None"
            return f"A{int(two)-1}"
        return f"{chr(one+1)}{two}"
    
    def draw_player(self, pl:bool, current:str, target:str): # If player is true, draw blue, else draw red as its a bot
        r = 20
        x,y,_ = self.board_data.get(target)
        if pl:
            f.delete("pl")
            f.create_oval(x-r,y-r,x+r, y+r, outline=None, fill="Blue", tags="pl")
        else:
            f.delete("bot")
            f.create_oval(x-r,y-r,x+r, y+r, outline=None, fill="Red", tags="bot")
        
        self.board_data[current] = (x,y,None) 
        self.board_data[target] = (x,y,True)
        
    
    def show_notation(self):
        start = "A6"
        for _ in range(0,6):
            for _ in range(0,6):
                x,y,_ = self.board_data.get(start)
                _ = f.create_text(
                        x, 
                        y, 
                        text=start, 
                        fill="blue", 
                        font=("Helvetica", 20,"bold"),
                        tags="notation"
                        )
                start = self.__progression(start)


    def draw_board(self):
        current = "A6"
        for i in range(0,6): # Each row
            for x in range(0,6): # Each coloumn
                colour = "#E2E2E2"
                
                f.create_rectangle(x * self.sqw, i * self.sqh, (x+1) * self.sqw, (i+1) * self.sqh, fill=colour, tags="square")
            

                centrex = x * self.sqw + self.sqw // 2  # center x of square
                centrey = i * self.sqh + self.sqh // 2  # center y of square
                self.board_data[current] = (centrex, centrey, None)
                current = self.__progression(current)
                # Centre will be used to actually move the pieces
        print(self.board_data)

    def validate_move(self, command:str):
        if command.lower() == "up":
            print(self.board_data)
    
    def onplayerclick(self, event):

        if event.keysym.lower() == "up":
            self.validate_move("up")
            return


c = Board()
c.draw_board()
c.show_notation()
c.draw_player(True, "A7", "C1")
c.draw_player(False, "A7", "D6")
r.bind("<Key>", c.onplayerclick)
f.focus_set()
r.mainloop()
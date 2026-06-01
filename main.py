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
        self.sqh = HEIGHT//8 # Get the square height required for each square of the board
        self.sqw = WIDTH//8 # Get the square width required for each square of the board
        self.board_data = {} # "board location":(x,y,piece_info) is the format data is stored in
    

    def __progression(self, character) -> str:
        one, two = list(character)
        one = ord(one) # Convert to ASCII
        if one == 72: # If H
            if two == 8 or f"A{int(two)+1}" == "A9": # Check if the second value is a 8 AND make sure its not A9. A9 is possible since the +1 for two is done AFTER the check
                return "None"
            
            return f"A{int(two)+1}"
        return f"{chr(one+1)}{two}"
        
    def progression_test(self):
        start = "A1"
        for i in range(64):
            x = self.__progression(start)
            start = x
            print(x)

    def draw_board(self):
        current = "A1"
        for i in range(0,8): # Each row
            for x in range(0,8): # Each coloumn
                f.create_rectangle(x * self.sqw, i * self.sqh, (x+1) * self.sqw, (i+1) * self.sqh)
                centrex = x * self.sqw + self.sqw // 2  # center x of square
                centrey = i * self.sqh + self.sqh // 2  # center y of square
                self.board_data[current] = (centrex, centrey, "None")
                # Centre will be used to actually move the pieces
                current = self.__progression(current)
        print(self.board_data)




c = Board()
c.draw_board()
c.progression_test()
f.mainloop()
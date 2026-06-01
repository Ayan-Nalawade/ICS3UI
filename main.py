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

    def draw_board(self):
        for i in range(0,8): # Each row
            for x in range(0,8): # Each coloumn
                f.create_rectangle(x * self.sqw, i * self.sqh, (x+1) * self.sqw, (i+1) * self.sqh)


c = Board()
c.draw_board()

f.mainloop()
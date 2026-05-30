import tkinter as tk
from time import sleep
from random import *
from math import *

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
        self.cubeWC = WIDTH // 8
        self.cubeHC = HEIGHT // 8
    

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                x1 = col * self.cubeWC
                y1 = row * self.cubeHC
                x2 = x1 + self.cubeWC
                y2 = y1 + self.cubeHC
                if (row + col) % 2 == 0: # Every alternate square we need to change the colour
                    color = "#FFFFFF"
                else:
                    color = "#8B5A2B"
                f.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)


board = Board()
board.draw_board()

f.mainloop()
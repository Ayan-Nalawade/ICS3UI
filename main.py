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
        self.cubeWC = (WIDTH // 8)
        self.cubeHC = HEIGHT // 8
        self.piece_size = max(1, int(min(self.cubeWC, self.cubeHC) * 0.98))
        # load piece images and keep references
        files = {
            'r': 'r.png', 'n': 'n.png', 'b': 'b.png', 'q': 'q.png', 'k': 'k.png', 'p': 'p.png'
        }
        self.images = {}
        for color in ('b', 'w'):
            for key, fname in files.items():
                self.images[color+key] = self._load_piece_image(f"{color}{key}.png")

    def _load_piece_image(self, path):
        img = Image.open(path).convert("RGBA")
        img = img.resize((self.piece_size, self.piece_size), Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    

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
    
    def draw_pieces(self):
        # standard chess starting positions
        # using lowercase keys: r,n,b,q,k,p with prefix b or w
        start = [
            ['br','bn','bb','bq','bk','bb','bn','br'],
            ['bp']*8,
            [None]*8,
            [None]*8,
            [None]*8,
            [None]*8,
            ['wp']*8,
            ['wr','wn','wb','wq','wk','wb','wn','wr']
        ]
        for row in range(8):
            for col in range(8):
                piece = start[row][col]
                if piece:
                    img = self.images.get(piece)
                    if img:
                        x = col * self.cubeWC + self.cubeWC//2
                        y = row * self.cubeHC + self.cubeHC//2
                        f.create_image(x, y, image=img)
        # ensure images are not garbage collected
        self._keep_refs = list(self.images.values())

board = Board()
board.draw_board()
board.draw_pieces()

f.mainloop()
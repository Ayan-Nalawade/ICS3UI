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
        self.selected = None
        # load piece images and keep references
        files = {
            'r': 'r.png', 'n': 'n.png', 'b': 'b.png', 'q': 'q.png', 'k': 'k.png', 'p': 'p.png'
        }
        self.images = {}
        for color in ('b', 'w'):
            for key, fname in files.items():
                self.images[color+key] = self._load_piece_image(f"{color}{key}.png")

        self.state = [
            ['br','bn','bb','bq','bk','bb','bn','br'],
            ['bp']*8,
            [None]*8,
            [None]*8,
            [None]*8,
            [None]*8,
            ['wp']*8,
            ['wr','wn','wb','wq','wk','wb','wn','wr']
        ]

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

        # labels: ranks on left, files along bottom
        for row in range(8):
            rank = 8 - row
            x = self.cubeWC * 0.15
            y = row * self.cubeHC + self.cubeHC * 0.5
            f.create_text(x, y, text=str(rank), fill="#111111")

        for col in range(8):
            file_letter = chr(ord('A') + col)
            x = col * self.cubeWC + self.cubeWC * 0.5
            y = 7 * self.cubeHC + self.cubeHC * 0.85
            f.create_text(x, y, text=file_letter, fill="#111111")
    
    def draw_pieces(self):
        f.delete("piece")
        for row in range(8):
            for col in range(8):
                piece = self.state[row][col]
                if piece:
                    img = self.images.get(piece)
                    if img:
                        x = col * self.cubeWC + self.cubeWC//2
                        y = row * self.cubeHC + self.cubeHC//2
                        f.create_image(x, y, image=img, tags="piece")
        # ensure images are not garbage collected
        self._keep_refs = list(self.images.values())

    def _coords_to_index(self, x, y):
        col = int(x // self.cubeWC)
        row = int(y // self.cubeHC)
        if 0 <= row < 8 and 0 <= col < 8:
            return row, col
        return None

    def _algebraic_to_index(self, square):
        if not square or len(square) < 2:
            return None
        file_char = square[0].upper()
        rank_char = square[1]
        if file_char < 'A' or file_char > 'H':
            return None
        if rank_char < '1' or rank_char > '8':
            return None
        col = ord(file_char) - ord('A')
        row = 8 - int(rank_char)
        return row, col

    def move_piece(self, src, dst):
        src_idx = self._algebraic_to_index(src)
        dst_idx = self._algebraic_to_index(dst)
        if not src_idx or not dst_idx:
            return False
        sr, sc = src_idx
        dr, dc = dst_idx
        piece = self.state[sr][sc]
        if piece is None:
            return False
        self.state[sr][sc] = None
        self.state[dr][dc] = piece
        self.draw_pieces()
        return True

    def _draw_selection(self):
        f.delete("selection")
        if self.selected is None:
            return
        row, col = self.selected
        x1 = col * self.cubeWC
        y1 = row * self.cubeHC
        x2 = x1 + self.cubeWC
        y2 = y1 + self.cubeHC
        f.create_rectangle(x1, y1, x2, y2, outline="#1E90FF", width=3, tags="selection")

    def on_click(self, event):
        idx = self._coords_to_index(event.x, event.y)
        if not idx:
            return
        row, col = idx
        if self.selected is None:
            if self.state[row][col] is None:
                return
            self.selected = (row, col)
            self._draw_selection()
            return

        sr, sc = self.selected
        if (row, col) == (sr, sc):
            self.selected = None
            self._draw_selection()
            return
        self.state[row][col] = self.state[sr][sc]
        self.state[sr][sc] = None
        self.selected = None
        self._draw_selection()
        self.draw_pieces()

board = Board()
board.draw_board()
board.draw_pieces()
f.bind("<Button-1>", board.on_click)

f.mainloop()
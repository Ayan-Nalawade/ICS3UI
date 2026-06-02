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
        self.piece_size = max(1, int(min(self.sqw, self.sqh) * 0.98))
        self._img_refs = {}
        self.BlackPlaying = False
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
        self.tomove = ""
    

    def __progression(self, character) -> str:
        if character == "None":  # Guard
            return "None"
        one, two = character[0], character[1]
        one = ord(one)
        if one == 72:
            if two == '1': 
                return "None"
            return f"A{int(two)-1}"
        return f"{chr(one+1)}{two}"

        
    def progression_test(self): # Test if the Blocks are correctly replying with the correct progression
        start = "A8"
        for i in range(64):
            x = self.__progression(start)
            start = x
            print(start)

    def draw_board(self):
        current = "A8"
        for i in range(0,8): # Each row
            for x in range(0,8): # Each coloumn
                if (i + x) % 2 == 0:
                    colour = "#949494"
                else:
                    colour = "#925300"
                
                f.create_rectangle(x * self.sqw, i * self.sqh, (x+1) * self.sqw, (i+1) * self.sqh, fill=colour, tags="square")
            

                centrex = x * self.sqw + self.sqw // 2  # center x of square
                centrey = i * self.sqh + self.sqh // 2  # center y of square
                self.board_data[current] = (centrex, centrey, "None")
                # Centre will be used to actually move the pieces
                current = self.__progression(current)
        # print(self.board_data)

    def redraw_pieces(self):
        f.delete("piece")

        for square, (x, y, piece) in self.board_data.items():
            if piece is not None:
                img = self._img_refs[piece]
                f.create_image(x, y, image=img, tags="piece")
    
    
    def update_piece(self, tomove, target):
        f.delete("highlight")

        x1, y1, piece = self.board_data[tomove]
        x2, y2, _ = self.board_data[target]

        if piece is None:
            return

        self.board_data[tomove] = (x1, y1, None)

        img = self._img_refs[piece]

        moving_piece = f.create_image(x1, y1, image=img, tags="piece")

        steps = 10
        dx = (x2 - x1) / steps
        dy = (y2 - y1) / steps

        def animate(step):
            if step >= steps:
                f.delete(moving_piece)
                self.board_data[target] = (x2, y2, piece)
                self.redraw_pieces()
                return

            f.move(moving_piece, dx, dy)
            f.after(15, animate, step + 1)

        animate(0)

        
    
    def draw_pieces(self):
        f.delete("piece")
        files = {'r','n','b','q','k','p'}

        if not self._img_refs:
            for color in ('b', 'w'):
                for key in files:
                    img = Image.open(f"{color}{key}.png").convert("RGBA")
                    img = img.resize((self.piece_size, self.piece_size), Image.LANCZOS)
                    self._img_refs[color+key] = ImageTk.PhotoImage(img)

        start = "A8"
        for row in range(0,8):
            for col in range(0,8):
                piece = self.state[row][col]
                x, y, _ = self.board_data.get(start)
                self.board_data[start] = (x, y, piece)
                if piece:  # Only draw if there's actually a piece
                    img = self._img_refs.get(piece)
                    if img:
                        f.create_image(x, y, image=img, tags="piece")
                start = self.__progression(start)

    def _get_square(self, event): # This function now maps the square to the coordinates
        col = event.x // self.sqw
        row = event.y // self.sqh

        file = chr(ord('A') + col)
        rank = 8 - row

        return f"{file}{rank}"
    
    def highlight_square(self, square):
        f.delete("highlight")

        x, y, _ = self.board_data[square]

        f.create_rectangle(
            x - self.sqw//2,
            y - self.sqh//2,
            x + self.sqw//2,
            y + self.sqh//2,
            outline="blue",
            width=4,
            tags="highlight"
        )
    
    def validate_move(self, square):
        _, _, piece = self.board_data.get(self.tomove)

        if piece is None:
            return  # nothing to move

        color = piece[0]  # 'b' or 'w'

        # check turn
        if color == 'b' and not self.BlackPlaying:
            return
        if color == 'w' and self.BlackPlaying:
            return

        # move is valid -> execute
        self.update_piece(self.tomove, square)

        # switch turn ONLY once
        self.BlackPlaying = not self.BlackPlaying
    

    def on_click(self, event):
        
        self.highlight_square(self._get_square(event))
        if self.tomove == "":
            self.tomove = self._get_square(event)
        else:
            self.validate_move(self._get_square(event))
            self.tomove = ""

        print(f"{self.board_data} \n")





c = Board()
# c.progression_test()
c.draw_board()
c.draw_pieces()
f.bind("<Button-1>", c.on_click)
f.mainloop()
import tkinter as tk
from random import randint
from PIL import Image, ImageTk

r = tk.Tk()

WIDTH = r.winfo_screenwidth()
HEIGHT = r.winfo_screenheight()
if WIDTH > 1000: 
    WIDTH = 1000
if HEIGHT > 1000: 
    HEIGHT = 1000
if WIDTH < 500: 
    WIDTH = 600
    print("Please resize WIDTH")
if HEIGHT < 500: 
    HEIGHT = 600
    print("Please resize HEIGHT")


f = tk.Canvas(r, width=WIDTH, height=HEIGHT, background="#FFFFFF")
f.pack()

WIDTH -= 200

SPRITE_SIZE = 64

class Board:
    def __init__(self):
        self.sqh = HEIGHT // 6
        self.sqw = WIDTH // 6
        self.board_data = {}
        self.check_who = True
        self.won = False
        self.pl_last_dir = "down"
        self.bot_last_dir = "down"

        def load_sprite(path):
            img = Image.open(path).convert("RGBA")
            img = img.resize((SPRITE_SIZE, SPRITE_SIZE), Image.LANCZOS)
            return ImageTk.PhotoImage(img)

        self.pl_sprites = {
            "up":    load_sprite("Back.png"),
            "down":  load_sprite("Front.png"),
            "left":  load_sprite("Left.png"),
            "right": load_sprite("Right.png"),
        }
        self.bot_sprites = {
            "up":    load_sprite("BackBot.png"),
            "down":  load_sprite("FrontBot.png"),
            "left":  load_sprite("LeftBot.png"),
            "right": load_sprite("RightBot.png"),
        }
        
    def rightside(self): 
        HEIGHTy = 0
        HEIGHTy2 = HEIGHT
        WIDTHx = WIDTH
        WIDTHx2 = WIDTH + 200
        txtsize = 20
        
        ptxtx = (WIDTHx2+WIDTHx)//2
        ptxty = HEIGHTy+25
        f.create_text(ptxtx, ptxty, text="Power-Ups", font=("Helvetica", 20, "underline", "bold"), tags="powerup")
        
        f.create_text(ptxtx, ptxty+100, text="Bot:", font=("Helvetica", 20, "italic underline"), tags="bottxt")
        f.create_rectangle(ptxtx+20, ptxty+20,ptxtx+20, ptxtx+20)

        
        
        
        

    def __piece_location(self, pl: bool):
        for square, (_, _, occupant) in self.board_data.items():
            if occupant == pl:
                return square
        return None

    def __progression(self, character) -> str:
        if character == "None":
            return "None"
        one, two = character[0], character[1]
        one = ord(one)
        if one == 70:
            if two == "1":
                return "None"
            return f"A{int(two)-1}"
        return f"{chr(one+1)}{two}"

    def draw_player(self, pl: bool, current: str, target: str, direction: str = None):
        x, y, _ = self.board_data[current]
        x2, y2, _ = self.board_data[target]

        if pl:
            if direction:
                self.pl_last_dir = direction
            sprite = self.pl_sprites[self.pl_last_dir]
            f.delete("pl")
            f.create_image(x2, y2, image=sprite, anchor="center", tags="pl")
        else:
            if direction:
                self.bot_last_dir = direction
            sprite = self.bot_sprites[self.bot_last_dir]
            f.delete("bot")
            f.create_image(x2, y2, image=sprite, anchor="center", tags="bot")

        self.board_data[current] = (x, y, None)
        self.board_data[target] = (x2, y2, pl)

    def show_notation(self):
        start = "A6"
        for _ in range(6):
            for _ in range(6):
                x, y, _ = self.board_data.get(start)
                f.create_text(x, y, text=start, fill="blue",
                              font=("Helvetica", 20, "bold"), tags="notation")
                start = self.__progression(start)

    def draw_board(self):
        current = "A6"
        for i in range(6):
            for x in range(6):
                f.create_rectangle(
                    x * self.sqw, i * self.sqh,
                    (x+1) * self.sqw, (i+1) * self.sqh,
                    fill="#E2E2E2", tags="square"
                )
                centrex = x * self.sqw + self.sqw // 2
                centrey = i * self.sqh + self.sqh // 2
                self.board_data[current] = (centrex, centrey, None)
                current = self.__progression(current)

    def validate_move(self, command: str, pl: bool):
        location = self.__piece_location(pl)
        if location is None or self.won:
            return 1

        col = location[0]
        row = int(location[1])
        direction = command.lower()
        target = None

        if direction == "up":
            if row == 6: return 1
            target = f"{col}{row+1}"
        elif direction == "down":
            if row == 1: return 1
            target = f"{col}{row-1}"
        elif direction == "left":
            if col == "A": return 1
            target = f"{chr(ord(col)-1)}{row}"
        elif direction == "right":
            if col == "F": return 1
            target = f"{chr(ord(col)+1)}{row}"
        else:
            return 1

        x, y, piece = self.board_data[target]
        if piece is not None:
            return 1

        self.draw_player(pl, location, target, direction)
        print(f"DEBUG: Moving {'player' if pl else 'bot'} from {location} to {target}")
        return 0

    def check_win(self):
        location = self.__piece_location(self.check_who)
        one, two = location[0], location[1]
        if self.check_who:
            self.check_who = False
            if two == "6":
                f.delete("all")
                f.create_text((WIDTH+200)//2, HEIGHT//2, text="You Won!",
                              font=("Helvetica", 48, "bold"), fill="green")
                self.won = True
        else:
            self.check_who = True
            if two == "1":
                f.delete("all")
                f.create_text((WIDTH+200)//2, HEIGHT//2, text="Bot Won!",
                              font=("Helvetica", 48, "bold"), fill="red")
                self.won = True

        if not self.won:
            r.after(200, self.check_win)

    def bot(self):
        if self.won:
            return
        r.after(5000, self.bot)
        k = self.validate_move("down", False)
        if k == 1:
            m = randint(0, 1)
            if m == 0:
                x = self.validate_move("left", False)
                if x == 1:
                    self.validate_move("right", False)
            else:
                x = self.validate_move("right", False)
                if x == 1:
                    self.validate_move("left", False)

    def onplayerclick(self, event):
        key = event.keysym.lower()
        if key in ("up", "down", "left", "right"):
            self.validate_move(key, True)


c = Board()
c.draw_board()
c.show_notation()
c.draw_player(True, "C1", "C1", "down")
c.draw_player(False, "D6", "D6", "down")
c.rightside()
c.bot()
c.check_win()
r.bind("<Key>", c.onplayerclick)
f.focus_set()
r.mainloop()
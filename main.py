import tkinter as tk
from random import randint
import math
from PIL import Image, ImageTk

r = tk.Tk()

WIDTH = r.winfo_screenwidth()
HEIGHT = r.winfo_screenheight()
if WIDTH > 1000: 
    WIDTH = 1000
if HEIGHT > 1000: 
    HEIGHT = 1000
if WIDTH < 300: 
    WIDTH = 600
    print("Please resize WIDTH")
if HEIGHT < 300: 
    HEIGHT = 600
    print("Please resize HEIGHT")


f = tk.Canvas(r, width=WIDTH, height=HEIGHT, background="#0B1F05")
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
        self.sticks_left = 4
        self.bot_sticks_left = 4
        self.stick_orientation = "horizontal"
        self.horizontal_walls = set()
        self.vertical_walls = set()
        self.tick = 0
        self.snakes = []
        snake_colors = ["#FF5252", "#FFEB3B", "#00BCD4", "#E040FB"]
        for i in range(2):
            self.snakes.append({
                "x": randint(0, WIDTH + 100),
                "y": randint(0, HEIGHT),
                "x_speed": randint(-3, 3) or 2,
                "y_speed": randint(-3, 3) or -2,
                "length": randint(15, 25),
                "color": snake_colors[i],
                "tags": f"snake_{i}",
                "history": []
            })

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
        HEIGHTy = 50
        WIDTHx = WIDTH
        WIDTHx2 = WIDTH + 200
        
        ptxtx = WIDTHx + 100
        ptxty = HEIGHTy + 25
        f.create_text(ptxtx, ptxty, text="Power-Ups", font=("Helvetica", 20, "underline", "bold"), tags="powerup", fill="#4CAF50")
        
        f.create_text(ptxtx, ptxty + 80, text="Bot:", font=("Helvetica", 16, "bold"), tags="bottxt", fill="white")
        rect_size = 30
        rect_spacing = 15
        for i in range(3):
            x_offset = ptxtx - 45 + i * (rect_size + rect_spacing)
            f.create_rectangle(x_offset, ptxty + 100, x_offset + rect_size, ptxty + 130, outline="#111", fill="#795548", tags=f"bot_rect{i}")
        
        f.create_text(ptxtx, ptxty + 170, text="Player:", font=("Helvetica", 16, "bold"), tags="playertxt", fill="white")
        for i in range(3):
            x_offset = ptxtx - 45 + i * (rect_size + rect_spacing)
            f.create_rectangle(x_offset, ptxty + 200, x_offset + rect_size, ptxty + 230, outline="#111", fill="#795548", tags=f"player_rect{i}")

        f.create_text(ptxtx - 45, ptxty + 270, text="Sticks Left:", font=("Helvetica", 16, "bold"), anchor="w", tags="stickstxt", fill="white")
        f.create_text(ptxtx + 75, ptxty + 270, text=str(self.sticks_left), font=("Helvetica", 16, "bold"), anchor="w", tags="sticksval", fill="#FFEB3B")
        f.create_text(ptxtx - 45, ptxty + 300, text="Stick Dir:", font=("Helvetica", 16, "bold"), anchor="w", tags="dirtxt", fill="white")
        f.create_text(ptxtx + 55, ptxty + 300, text=self.stick_orientation.capitalize(), font=("Helvetica", 16, "bold"), anchor="w", tags="dirval", fill="#FFEB3B")
        f.create_text(ptxtx, ptxty + 340, text="(Right-click or press 'Space'\nto flip)", font=("Helvetica", 10, "italic"), justify="center", tags="dirhint", fill="#BDBDBD")

    def toggle_orientation(self, event=None):
        if self.stick_orientation == "horizontal":
            self.stick_orientation = "vertical"
        else:
            self.stick_orientation = "horizontal"
        f.itemconfigure("dirval", text=self.stick_orientation.capitalize())

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
                f.create_text(x, y, text=start, fill="#8BC34A",
                              font=("Helvetica", 20, "bold"), tags="notation")
                start = self.__progression(start)

    def draw_board(self):
        current = "A6"
        for i in range(6):
            for x in range(6):
                color = "#2E4A1E" if (x + i) % 2 == 0 else "#233D14"
                f.create_rectangle(
                    x * self.sqw, i * self.sqh,
                    (x+1) * self.sqw, (i+1) * self.sqh,
                    fill=color, outline="#1A2E0C", tags="square"
                )
                centrex = x * self.sqw + self.sqw // 2
                centrey = i * self.sqh + self.sqh // 2
                self.board_data[current] = (centrex, centrey, None)
                current = self.__progression(current)

    def animate_jungle(self):
        if self.won:
            return
        
        self.tick += 1

        for snake in self.snakes:
            # Introduce random wandering variation
            if randint(0, 15) == 0:
                angle = math.atan2(snake["y_speed"], snake["x_speed"]) + (randint(-1, 1) * 0.5)
                speed = math.hypot(snake["x_speed"], snake["y_speed"])
                snake["x_speed"] = math.cos(angle) * speed
                snake["y_speed"] = math.sin(angle) * speed
            
            snake["x"] += snake["x_speed"]
            snake["y"] += snake["y_speed"]
            
            # Screen edge wrap-around (clears history to avoid streaking a line across screen)
            if snake["x"] < -20: snake["x"] = WIDTH + 220; snake["history"].clear()
            if snake["x"] > WIDTH + 220: snake["x"] = -20; snake["history"].clear()
            if snake["y"] < -20: snake["y"] = HEIGHT + 20; snake["history"].clear()
            if snake["y"] > HEIGHT + 20: snake["y"] = -20; snake["history"].clear()
            
            # Mathematical slithering effect!
            angle = math.atan2(snake["y_speed"], snake["x_speed"])
            perp_angle = angle + math.pi / 2
            slither = math.sin(self.tick * 0.5) * 6
            
            draw_x = snake["x"] + math.cos(perp_angle) * slither
            draw_y = snake["y"] + math.sin(perp_angle) * slither
            
            snake["history"].insert(0, (draw_x, draw_y))
            if len(snake["history"]) > snake["length"]:
                snake["history"].pop()
                
            f.delete(snake["tags"])
            
            if len(snake["history"]) > 1:
                # Draw the full segmented snake history tapering at the end
                for i in range(len(snake["history"]) - 1):
                    x1, y1 = snake["history"][i]
                    x2, y2 = snake["history"][i+1]
                    w = max(1, 6 - int((i / snake["length"]) * 6))
                    f.create_line(x1, y1, x2, y2, fill=snake["color"], width=w, tags=snake["tags"], capstyle="round")
                    
            # Render snake layers strategically so they travel over tiles but beneath characters and walls
            if f.find_withtag("square"):
                f.tag_raise(snake["tags"], "square")
            if f.find_withtag("pl"):
                f.tag_lower(snake["tags"], "pl")
            if f.find_withtag("bot"):
                f.tag_lower(snake["tags"], "bot")
            if f.find_withtag("wall"):
                f.tag_lower(snake["tags"], "wall")
            
        r.after(50, self.animate_jungle)

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
            if (col, row) in self.horizontal_walls: 
                return 1
            
            target = f"{col}{row+1}"
        elif direction == "down":
            if row == 1: return 1
            if (col, row-1) in self.horizontal_walls: 
                return 1
            
            target = f"{col}{row-1}"
        elif direction == "left":
            if col == "A": return 1
            prev_col = chr(ord(col)-1)
            if (prev_col, row) in self.vertical_walls:
                return 1
            
            target = f"{prev_col}{row}"
        elif direction == "right":
            if col == "F": 
                return 1
            if (col, row) in self.vertical_walls: 
                return 1
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
            r.after(50, self.check_win)

    def bot(self):
        if self.won:
            return
        r.after(1000, self.bot)
        
        # 1 in 3 chance the bot decides to place a stick instead of moving (if it has any left)
        if self.bot_sticks_left > 0 and randint(0, 2) == 0:
            placed = False
            for _ in range(20): # Try up to 20 random spots
                if randint(0, 1) == 0: # Try horizontal
                    x2 = randint(0, 5)
                    wall_row = randint(1, 5)
                    wall = (chr(ord('A') + x2), wall_row)
                    if wall not in self.horizontal_walls:
                        self.horizontal_walls.add(wall)
                        y2 = 6 - wall_row
                        line_y = y2 * self.sqh
                        f.create_line(x2 * self.sqw, line_y, (x2 + 1) * self.sqw, line_y, width=5, fill="brown", tags="wall")
                        placed = True
                        break
                else: # Try vertical
                    x2 = randint(0, 4)
                    wall_row = randint(1, 6)
                    wall = (chr(ord('A') + x2), wall_row)
                    if wall not in self.vertical_walls:
                        self.vertical_walls.add(wall)
                        y2 = 6 - wall_row
                        line_x = (x2 + 1) * self.sqw
                        f.create_line(line_x, y2 * self.sqh, line_x, (y2 + 1) * self.sqh, width=5, fill="brown", tags="wall")
                        placed = True
                        break
            
            if placed:
                self.bot_sticks_left -= 1
                return # Skip movement since the bot spent its turn placing a stick

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

    def on_mouse_click(self, event):
        if self.won or self.sticks_left <= 0:
            return
        
        x2 = event.x // self.sqw
        y2 = event.y // self.sqh
        
        if x2 >= 6 or y2 >= 6 or x2 < 0 or y2 < 0: # Basically if the user clicks outside
            return
        
        placed = False
        if self.stick_orientation == "horizontal":
            center_y = y2 * self.sqh + self.sqh // 2
            if event.y < center_y:
                wall_row = 6 - y2
                if wall_row < 6:
                    wall = (chr(ord('A') + x2), wall_row)
                    if wall not in self.horizontal_walls:
                        self.horizontal_walls.add(wall)
                        line_y = y2 * self.sqh
                        f.create_line(x2 * self.sqw, line_y, (x2 + 1) * self.sqw, line_y, width=5, fill="blue", tags="wall")
                        placed = True
            else:
                wall_row = 5 - y2
                if wall_row >= 1:
                    wall = (chr(ord('A') + x2), wall_row)
                    if wall not in self.horizontal_walls:
                        self.horizontal_walls.add(wall)
                        line_y = (y2 + 1) * self.sqh
                        f.create_line(x2 * self.sqw, line_y, (x2 + 1) * self.sqw, line_y, width=5, fill="blue", tags="wall")
                        placed = True
        else:
            center_x = x2 * self.sqw + self.sqw // 2
            row_str = 6 - y2
            if event.x < center_x:
                if x2 > 0:
                    wall = (chr(ord('A') + x2 - 1), row_str)
                    if wall not in self.vertical_walls:
                        self.vertical_walls.add(wall)
                        line_x = x2 * self.sqw
                        f.create_line(line_x, y2 * self.sqh, line_x, (y2 + 1) * self.sqh, width=5, fill="brown", tags="wall")
                        placed = True
            else:
                if x2 < 5:
                    wall = (chr(ord('A') + x2), row_str)
                    if wall not in self.vertical_walls:
                        self.vertical_walls.add(wall)
                        line_x = (x2 + 1) * self.sqw
                        f.create_line(line_x, y2 * self.sqh, line_x, (y2 + 1) * self.sqh, width=5, fill="brown", tags="wall")
                        placed = True

        if placed:
            self.sticks_left -= 1
            f.itemconfigure("sticksval", text=str(self.sticks_left))

    def onplayerclick(self, event):
        key = event.keysym.lower()
        if key == "space":
            self.toggle_orientation()
        elif key in ("up", "down", "left", "right"):
            self.validate_move(key, True)


c = Board()
c.draw_board()
c.show_notation()
c.draw_player(True, "C1", "C1", "down")
c.draw_player(False, "D6", "D6", "down")
c.rightside()
c.bot()
c.animate_jungle()
c.check_win()
r.bind("<Key>", c.onplayerclick)
r.bind("<Button-3>", c.toggle_orientation)
r.bind("<Button-2>", c.toggle_orientation)
f.bind("<Button-1>", c.on_mouse_click)
f.focus_set()
r.mainloop()
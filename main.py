import tkinter as tk
from random import randint, choice, uniform
import math
from PIL import Image, ImageTk
import bot_ml

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
        self.horizontal_walls = set()
        self.vertical_walls = set()
        self.tick = 0
        self.snakes = []
        snake_colors = ["#2E5A3A", "#3D4A2A", "#1A4A4A", "#3A2A4A"]
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
        self.fireflies = []
        for _ in range(18):
            self.fireflies.append({
                "x": uniform(0, WIDTH),
                "y": uniform(0, HEIGHT),
                "speed_x": uniform(-0.4, 0.4),
                "speed_y": uniform(-0.4, 0.4),
                "phase": uniform(0, math.pi * 2),
                "tag": f"ff_{randint(0, 99999)}"
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
        self.chest_sprites = {
            "closed": load_sprite("chest.png"),
            "open":   load_sprite("chest-open.png"),
        }
        self.chests = {}
        self.vanishing_chests = []
        self._place_chests()
        self.player_powerups = []
        self.bot_powerups = []
        self.win_frame = 0
        self.win_type = None
        self.win_particles = []
        self.bot_move_log = ""  # latest move description shown on screen
        
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

        f.create_text(ptxtx - 90, ptxty + 270, text="Sticks Left:", font=("Helvetica", 16, "bold"), anchor="w", tags="stickstxt", fill="white")
        f.create_text(ptxtx + 75, ptxty + 270, text=str(self.sticks_left), font=("Helvetica", 16, "bold"), anchor="w", tags="sticksval", fill="#FFEB3B")

        f.create_text(ptxtx - 90, ptxty + 310, text="Bot Sticks:", font=("Helvetica", 16, "bold"), anchor="w", tags="botstickstxt", fill="white")
        f.create_text(ptxtx + 75, ptxty + 310, text=str(self.bot_sticks_left), font=("Helvetica", 16, "bold"), anchor="w", tags="botsticksval", fill="#FF9800")

        # Instructions
        f.create_text(ptxtx, ptxty + 370, text="Instructions", font=("Helvetica", 18, "underline", "bold"), tags="instructions", fill="#4CAF50")
        f.create_text(ptxtx, ptxty + 440, text="Get to the other side before the bot, click on the squares to place vines and block the bot",
                      font=("Helvetica", 12), tags="instructions", fill="#CCE5CC", width=170)

        self._draw_powerups()

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

    def _place_chests(self):
        """Randomly place closed chests on the board, avoiding starting squares."""
        available = []
        for col in ["A", "B", "C", "D", "E", "F"]:
            for row in range(1, 7):
                available.append(f"{col}{row}")
        available.remove("C1")
        available.remove("D6")
        for _ in range(randint(3, 4)):
            square = choice(available)
            available.remove(square)
            self.chests[square] = "closed"

    def draw_chests(self):
        """Draw all chests on the board, behind players."""
        f.delete("chest")
        for square, state in self.chests.items():
            data = self.board_data.get(square)
            if data:
                x, y, _ = data
                sprite = self.chest_sprites[state]
                f.create_image(x, y, image=sprite, anchor="center", tags="chest")
        if f.find_withtag("pl"):
            f.tag_lower("chest", "pl")
        if f.find_withtag("bot"):
            f.tag_lower("chest", "bot")

    def _draw_powerups(self):
        """Draw power-up indicators in the right panel slots."""
        f.delete("pu_indicator")
        ptxtx = WIDTH + 100
        ptxty = 75
        rect_size = 30
        rect_spacing = 15

        # Bot power-ups
        for i, pu in enumerate(self.bot_powerups[:3]):
            x_offset = ptxtx - 45 + i * (rect_size + rect_spacing)
            center_x = x_offset + rect_size // 2
            center_y = ptxty + 100 + rect_size // 2
            if pu == "extra_stick":
                f.create_oval(center_x - 8, center_y - 8, center_x + 8, center_y + 8,
                             fill="#4CAF50", outline="", tags="pu_indicator")
                f.create_text(center_x, center_y, text="+", font=("Helvetica", 16, "bold"),
                             fill="white", tags="pu_indicator")
            elif pu == "erase_stick":
                f.create_oval(center_x - 8, center_y - 8, center_x + 8, center_y + 8,
                             fill="#F44336", outline="", tags="pu_indicator")
                f.create_text(center_x, center_y, text="-", font=("Helvetica", 16, "bold"),
                             fill="white", tags="pu_indicator")

        # Player power-ups
        for i, pu in enumerate(self.player_powerups[:3]):
            x_offset = ptxtx - 45 + i * (rect_size + rect_spacing)
            center_x = x_offset + rect_size // 2
            center_y = ptxty + 200 + rect_size // 2
            if pu == "extra_stick":
                f.create_oval(center_x - 8, center_y - 8, center_x + 8, center_y + 8,
                             fill="#4CAF50", outline="", tags="pu_indicator")
                f.create_text(center_x, center_y, text="+", font=("Helvetica", 16, "bold"),
                             fill="white", tags="pu_indicator")
            elif pu == "erase_stick":
                f.create_oval(center_x - 8, center_y - 8, center_x + 8, center_y + 8,
                             fill="#F44336", outline="", tags="pu_indicator")
                f.create_text(center_x, center_y, text="-", font=("Helvetica", 16, "bold"),
                             fill="white", tags="pu_indicator")

    def _award_powerup(self, is_player):
        """Award a random power-up when a chest is touched."""
        powerup = choice(["extra_stick", "erase_stick"])

        if is_player:
            self.player_powerups.append(powerup)
            if powerup == "extra_stick":
                self.sticks_left += 1
            elif powerup == "erase_stick":
                self.horizontal_walls.clear()
                self.vertical_walls.clear()
                f.delete("wall")
        else:
            self.bot_powerups.append(powerup)
            if powerup == "extra_stick":
                self.bot_sticks_left += 1
            elif powerup == "erase_stick":
                self.horizontal_walls.clear()
                self.vertical_walls.clear()
                f.delete("wall")

        self._draw_powerups()
        f.itemconfigure("sticksval", text=str(self.sticks_left))
        f.itemconfigure("botsticksval", text=str(self.bot_sticks_left))

    def _draw_leaf_shape(self, x1, y1, angle, size, color, outline_color, tag="wall"):
        """Draw a realistic leaf shape polygon."""
        angle_rad = math.radians(angle)
        half_width = size * 0.35
        pts = []
        for t_rel in range(0, 181, 12):
            t = t_rel / 180
            along = -size + t * size * 2
            width = half_width * math.sin(t * math.pi)
            x = x1 + along * math.cos(angle_rad) - width * math.sin(angle_rad)
            y = y1 + along * math.sin(angle_rad) + width * math.cos(angle_rad)
            pts.append(x)
            pts.append(y)
        f.create_polygon(*pts, fill=color, outline=outline_color, width=1,
                        smooth=True, tags=tag)
        # Center vein
        x2 = x1 + size * 0.7 * math.cos(angle_rad)
        y2 = y1 + size * 0.7 * math.sin(angle_rad)
        f.create_line(x1, y1, x2, y2, fill=outline_color, width=1, tags=tag)

    def _draw_leaf_cluster(self, x1, y1, vine_angle):
        """Draw leaves sprouting from a vine node."""
        colors = ["#1B5E20", "#2E7D32", "#388E3C", "#43A047"]
        for i in range(randint(2, 4)):
            off = randint(-50, 50)
            sz = randint(7, 13)
            self._draw_leaf_shape(
                x1 + randint(-3, 3), y1 + randint(-3, 3),
                vine_angle + off, sz, choice(colors), "#0B3D0B"
            )

    def _draw_tendril(self, x1, y1, angle, length):
        """Draw a curly vine tendril."""
        pts = []
        x, y = x1, y1
        for i in range(24):
            t = i / 24
            angle2 = angle + math.sin(t * math.pi * 5) * 40
            x += math.cos(math.radians(angle2)) * length / 24
            y += math.sin(math.radians(angle2)) * length / 24
            pts.extend([x, y])
        f.create_line(*pts, fill="#4CAF50", width=1, smooth=True, tags="wall")

    def draw_vine(self, x1, y1, x2, y2, color):
        """Draw a realistic organic vine with leaves and tendrils."""
        segments = 14
        horiz = y1 == y2

        pts = []
        for i in range(segments + 1):
            t = i / segments
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t
            if 0 < i < segments:
                wiggle = math.sin(t * math.pi * 3 + self.tick * 0.03) * (5 + 3 * math.sin(t * math.pi))
                if horiz:
                    y += wiggle
                else:
                    x += wiggle
            pts.extend([x, y])

        # Three layers for depth: dark shadow, main body, highlight
        f.create_line(*pts, fill="#0B3D0B", width=7, smooth=True, tags="wall", capstyle="round")
        f.create_line(*pts, fill=color, width=5, smooth=True, tags="wall", capstyle="round")
        f.create_line(*pts, fill="#66BB6A", width=2, smooth=True, tags="wall", capstyle="round")

        # Leaves along the vine
        if horiz:
            vine_angle = 0
        else:
            vine_angle = 90
        for i in range(2, segments, 3):
            x, y = pts[i * 2], pts[i * 2 + 1]
            if i % 2 == 0:
                side = 90
            else:
                side = -90
            self._draw_leaf_cluster(x, y, vine_angle + side)

        # Occasional tendril
        if randint(0, 2) == 0:
            idx = randint(2, segments - 2)
            x, y = pts[idx * 2], pts[idx * 2 + 1]
            self._draw_tendril(x, y, vine_angle + choice([-60, 60]), randint(15, 25))

    def _draw_grass_blade(self, x, y, height, lean):
        """Draw a single curved grass blade."""
        f.create_line(
            x, y,
            x + lean * 0.3, y - height * 0.6,
            x + lean, y - height,
            fill=choice(["#4CAF50", "#66BB6A", "#388E3C", "#2E7D32"]),
            width=1, smooth=True, tags="tile_detail"
        )

    def _draw_tile_texture(self, x, y, sqw, sqh, dark_shade):
        """Add grass, dirt, and moss detail to a single tile."""
        # Random dirt/moss patches
        for _ in range(randint(2, 4)):
            x1 = x + randint(6, sqw - 6)
            y1 = y + randint(6, sqh - 6)
            r2 = randint(3, 7)
            f.create_oval(x1 - r2, y1 - r2, x1 + r2, y1 + r2,
                         fill=dark_shade, outline="", tags="tile_detail")

        # Grass blades
        for _ in range(randint(4, 7)):
            x1 = x + randint(4, sqw - 4)
            y1 = y + sqh - randint(2, 5)
            h = randint(5, 12)
            lean = randint(-4, 4)
            self._draw_grass_blade(x1, y1, h, lean)

        # Tiny lighter speckles (decomposition highlights)
        for _ in range(randint(1, 3)):
            x1 = x + randint(8, sqw - 8)
            y1 = y + randint(8, sqh - 8)
            f.create_oval(x1 - 1, y1 - 1, x1 + 1, y1 + 1,
                         fill="#8BC34A", outline="", tags="tile_detail")

    def draw_board(self):
        """Draw the board with realistic jungle floor tiles."""
        # Dark mossy border around the whole board
        pad = 5
        f.create_rectangle(-pad, -pad, WIDTH + pad, HEIGHT + pad,
                          fill="#0B3D0B", outline="#071F05", tags="board_border")
        # Inner shadow edge
        f.create_rectangle(0, 0, WIDTH, HEIGHT,
                          fill="", outline="#1A5C1A", width=2, tags="board_border")

        current = "A6"
        for i in range(6):
            for x in range(6):
                is_dark = (x + i) % 2 == 0
                base = "#2E4A1E" if is_dark else "#233D14"
                dark = "#1A3A0E" if is_dark else "#152B0B"

                x1 = x * self.sqw
                y1 = i * self.sqh

                f.create_rectangle(
                    x1, y1, x1 + self.sqw, y1 + self.sqh,
                    fill=base, outline="#1A2E0C", tags="square"
                )

                self._draw_tile_texture(x1, y1, self.sqw, self.sqh, dark)

                x_center = x1 + self.sqw // 2
                y_center = y1 + self.sqh // 2
                self.board_data[current] = (x_center, y_center, None)
                current = self.__progression(current)

    def draw_jungle_ambient(self):
        """Draw static jungle foliage around the board edges."""
        # Hanging vines from top of canvas
        for i in range(10):
            x = randint(10, WIDTH - 10)
            vine_len = randint(50, 140)
            pts = []
            for j in range(12):
                t = j / 12
                sway = math.sin(t * math.pi * 2.5) * 10 * t
                pts.extend([x + sway, -5 + vine_len * t])
            f.create_line(*pts, fill="#1B5E20", width=3, smooth=True, tags="bg_foliage")
            # Small leaf at end (ambient, not a wall)
            self._draw_leaf_shape(
                pts[-2], pts[-1] - 5, 90 + randint(-20, 20),
                randint(8, 13), choice(["#2E7D32", "#388E3C"]), "#0B3D0B",
                tag="bg_foliage"
            )

        # Dense corner foliage
        corners = [
            (15, 15, 135),
            (WIDTH - 15, 15, 45),
            (15, HEIGHT - 15, 225),
            (WIDTH - 15, HEIGHT - 15, -45)
        ]
        for x, y, angle in corners:
            for _ in range(5):
                self._draw_leaf_shape(
                    x + randint(-20, 20), y + randint(-20, 20),
                    angle + randint(-50, 50), randint(14, 24),
                    choice(["#1B5E20", "#2E7D32", "#1A4A1A"]), "#0B3D0B",
                    tag="bg_foliage"
                )

        # Low bushes along the bottom
        for i in range(8):
            x = i * (WIDTH // 7) + randint(5, 25)
            y = HEIGHT - randint(3, 12)
            for _ in range(6):
                x_offset = randint(-18, 18)
                y_offset = randint(-12, 4)
                size = randint(7, 15)
                f.create_oval(x + x_offset - size, y + y_offset - size, x + x_offset + size, y + y_offset + size,
                             fill="#1B5E20", outline="#0B3D0B", tags="bg_foliage")

        # Push ambient behind everything
        f.tag_lower("bg_foliage")
        f.tag_lower("board_border")

    def animate_jungle(self):
        if self.won:
            self._animate_win()
            f.after(50, self.animate_jungle)
            return
        
        self.tick += 1

        # Animate fireflies
        for firefly in self.fireflies:
            firefly["x"] += firefly["speed_x"]
            firefly["y"] += firefly["speed_y"]

            # Bounce off edges
            if firefly["x"] < 0 or firefly["x"] > WIDTH:
                firefly["speed_x"] *= -1
            if firefly["y"] < 0 or firefly["y"] > HEIGHT:
                firefly["speed_y"] *= -1

            # Random direction change
            if randint(0, 40) == 0:
                firefly["speed_x"] += uniform(-0.3, 0.3)
                firefly["speed_y"] += uniform(-0.3, 0.3)
                speed = math.hypot(firefly["speed_x"], firefly["speed_y"])
                if speed > 1:
                    firefly["speed_x"] /= speed
                    firefly["speed_y"] /= speed

            glow = abs(math.sin(self.tick * 0.04 + firefly["phase"]))
            r = int(40 + 30 * glow)
            g = int(100 + 40 * glow)
            b = int(30 + 20 * glow)
            color = f"#{r:02x}{g:02x}{b:02x}"

            f.delete(firefly["tag"])

            # Outer glow ring
            glow_size = 2 + int(3 * glow)
            f.create_oval(
                firefly["x"] - glow_size, firefly["y"] - glow_size,
                firefly["x"] + glow_size, firefly["y"] + glow_size,
                fill=color, outline="", tags=firefly["tag"]
            )
            # Core
            core_size = 1 + int(1 * glow)
            f.create_oval(
                firefly["x"] - core_size, firefly["y"] - core_size,
                firefly["x"] + core_size, firefly["y"] + core_size,
                fill="#CCDDAA", outline="", tags=firefly["tag"]
            )

            f.tag_raise(firefly["tag"])

        # Animate vanishing chests
        for vc in self.vanishing_chests[:]:
            vc["frame"] += 1
            tag = f"vanish_{vc['square']}"
            f.delete(tag)

            if vc["frame"] >= vc["max_frames"]:
                self.vanishing_chests.remove(vc)
                continue

            t = vc["frame"] / vc["max_frames"]
            x1, y1 = vc["x"], vc["y"]

            # Expanding golden glow that fades out
            radius = 5 + t * 28
            r = int(255 * (1 - t))
            g = int(220 * (1 - t))
            b = int(50 * (1 - t))
            glow_color = f"#{r:02x}{g:02x}{b:02x}"
            f.create_oval(x1 - radius, y1 - radius, x1 + radius, y1 + radius,
                          fill=glow_color, outline="", tags=tag)

            # Sparkle particles flying outward
            for i in range(10):
                angle = i * math.pi / 5 + t * 3
                dist = 5 + t * 35
                x2 = x1 + math.cos(angle) * dist
                y2 = y1 + math.sin(angle) * dist
                size = max(1, 5 - int(t * 5))
                r = int(255 * (1 - t))
                g = int(255 * (1 - t))
                b = int(200 * (1 - t))
                color = f"#{r:02x}{g:02x}{b:02x}"
                f.create_oval(x2 - size, y2 - size, x2 + size, y2 + size,
                              fill=color, outline="", tags=tag)

            f.tag_raise(tag)

        # Animate snakes (original logic preserved)
        for snake in self.snakes:
            if randint(0, 15) == 0:
                angle = math.atan2(snake["y_speed"], snake["x_speed"]) + (randint(-1, 1) * 0.5)
                speed = math.hypot(snake["x_speed"], snake["y_speed"])
                snake["x_speed"] = math.cos(angle) * speed
                snake["y_speed"] = math.sin(angle) * speed

            snake["x"] += snake["x_speed"]
            snake["y"] += snake["y_speed"]

            if snake["x"] < -20:
                snake["x"] = WIDTH + 220
                snake["history"].clear()
            if snake["x"] > WIDTH + 220:
                snake["x"] = -20
                snake["history"].clear()
            if snake["y"] < -20:
                snake["y"] = HEIGHT + 20
                snake["history"].clear()
            if snake["y"] > HEIGHT + 20:
                snake["y"] = -20
                snake["history"].clear()

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
                for i in range(len(snake["history"]) - 1):
                    x1, y1 = snake["history"][i]
                    x2, y2 = snake["history"][i + 1]
                    w = max(1, 3 - int((i / snake["length"]) * 2))
                    f.create_line(x1, y1, x2, y2, fill=snake["color"], width=w,
                                 tags=snake["tags"], capstyle="round")

            if f.find_withtag("square"):
                f.tag_raise(snake["tags"], "square")
            if f.find_withtag("pl"):
                f.tag_lower(snake["tags"], "pl")
            if f.find_withtag("bot"):
                f.tag_lower(snake["tags"], "bot")
            if f.find_withtag("wall"):
                f.tag_lower(snake["tags"], "wall")

        f.after(50, self.animate_jungle)

    def validate_move(self, command: str, pl: bool):
        location = self.__piece_location(pl)
        if location is None or self.won:
            return 1

        col = location[0]
        row = int(location[1])
        direction = command.lower()
        target = None

        if direction == "up":
            if row == 6:
                return 1
            if (col, row) in self.horizontal_walls: 
                return 1
            
            target = f"{col}{row+1}"
        elif direction == "down":
            if row == 1:
                return 1
            if (col, row-1) in self.horizontal_walls: 
                return 1
            
            target = f"{col}{row-1}"
        elif direction == "left":
            if col == "A":
                return 1
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
        # Vanishing chest if stepping onto one
        if target in self.chests and self.chests[target] == "closed":
            data = self.board_data.get(target)
            if data:
                x, y, _ = data
                self.vanishing_chests.append({
                    "x": x, "y": y,
                    "square": target,
                    "frame": 0,
                    "max_frames": 10
                })
            del self.chests[target]
            self.draw_chests()
            if pl:
                print("Player touches chest")
            else:
                print("Bot touches chest")
            self._award_powerup(pl)
        # if pl:
        #     who = "player"
        # else:
        #     who = "bot"
        #print(f"DEBUG: Moving {who} from {location} to {target}")
        return 0

    def check_win(self):
        location = self.__piece_location(self.check_who)
        if location is None:
            if not self.won:
                r.after(50, self.check_win)
            return

        one, two = location[0], location[1]
        if self.check_who:
            self.check_who = False
            if two == "6":
                self.won = True
                self.win_frame = 0
                self.win_type = "player"
                self._draw_win_screen()
        else:
            self.check_who = True
            if two == "1":
                self.won = True
                self.win_frame = 0
                self.win_type = "bot"
                self._draw_win_screen()

        if not self.won:
            r.after(50, self.check_win)

    def _draw_win_screen(self):
        """Draw the win/lose overlay and start particles."""
        is_win = self.win_type == "player"
        canvas_width = WIDTH + 200

        # Dark overlay
        if is_win:
            overlay = "#0A1F05"
        else:
            overlay = "#1F0505"
        f.create_rectangle(0, 0, canvas_width, HEIGHT, fill=overlay, tags="win_overlay")

        # Large title with shadow
        if is_win:
            title = "VICTORY"
            title_color = "#FFD700"
            shadow_color = "#5C3A00"
        else:
            title = "DEFEAT"
            title_color = "#FF3333"
            shadow_color = "#5C0000"
        x1 = canvas_width // 2
        y1 = HEIGHT // 2 - 30

        f.create_text(x1 + 3, y1 + 3, text=title,
                      font=("Helvetica", 64, "bold"), fill=shadow_color, tags="win_title_shadow")
        f.create_text(x1, y1, text=title,
                      font=("Helvetica", 64, "bold"), fill=title_color, tags="win_title")

        # Subtitle
        if is_win:
            subtitle = "You reached the other side!"
        else:
            subtitle = "The bot beat you!"
        f.create_text(x1, y1 + 60, text=subtitle,
                      font=("Helvetica", 20), fill="#CCCCCC", tags="win_subtitle")

        # Particles differ by outcome
        self.win_particles = []
        if is_win:
            count = 50
        else:
            count = 30
        for _ in range(count):
            if is_win:
                colors = ["#FF5252", "#FFEB3B", "#00BCD4", "#E040FB", "#FFD700", "#4CAF50", "#FF9800"]
                y_start = randint(-HEIGHT, 0)
                speed_x = uniform(-2, 2)
                speed_y = uniform(2, 5)
                size = randint(3, 7)
            else:
                colors = ["#8B0000", "#660000", "#CC3333", "#440000", "#992222"]
                y_start = randint(0, HEIGHT)
                speed_x = uniform(-0.5, 0.5)
                speed_y = uniform(-1, -0.3)
                size = randint(2, 5)
            self.win_particles.append({
                "x": randint(0, canvas_width),
                "y": y_start,
                "speed_x": speed_x,
                "speed_y": speed_y,
                "size": size,
                "color": choice(colors),
                "phase": uniform(0, math.pi * 2),
                "tag": f"win_p_{randint(0, 99999)}"
            })

    def _animate_win(self):
        """Animate the win/lose screen — pulsing text and particles."""
        self.win_frame += 1
        is_win = self.win_type == "player"
        canvas_width = WIDTH + 200
        x1 = canvas_width // 2
        y1 = HEIGHT // 2 - 30

        # Pulsing title glow
        f.delete("win_glow")
        pulse = abs(math.sin(self.win_frame * 0.06))
        glow_radius = 40 + int(30 * pulse)
        intensity = int(60 * pulse)
        if is_win:
            glow_color = f"#{intensity:02x}{int(intensity*0.85):02x}00"
        else:
            glow_color = f"#{intensity:02x}0000"
        f.create_oval(x1 - glow_radius, y1 - glow_radius,
                      x1 + glow_radius, y1 + glow_radius,
                      fill=glow_color, outline="", tags="win_glow")
        f.tag_lower("win_glow", "win_title_shadow")

        # Subtle title bounce
        bounce = int(math.sin(self.win_frame * 0.08) * 3)
        f.coords("win_title", x1, y1 + bounce)
        f.coords("win_title_shadow", x1 + 3, y1 + bounce + 3)

        # Animate particles
        for p in self.win_particles[:]:
            f.delete(p["tag"])
            p["x"] += p["speed_x"] + math.sin(self.win_frame * 0.04 + p["phase"]) * 0.3
            p["y"] += p["speed_y"]

            if p["y"] < -30 or p["y"] > HEIGHT + 30:
                p["x"] = randint(0, canvas_width)
                if is_win:
                    p["y"] = randint(-30, -5)
                else:
                    p["y"] = HEIGHT + randint(5, 30)

            if 0 <= p["y"] <= HEIGHT:
                f.create_oval(p["x"] - p["size"], p["y"] - p["size"],
                              p["x"] + p["size"], p["y"] + p["size"],
                              fill=p["color"], outline="", tags=p["tag"])

    def _build_ml_state(self):
        """Build a GameState from the current board for bot decision-making."""
        s = bot_ml.GameState()
        # Player position (1-indexed -> 0-indexed)
        ploc = self.__piece_location(True)
        if ploc:
            s.p_col = ord(ploc[0]) - ord("A")
            s.p_row = int(ploc[1]) - 1
        # Bot position
        bloc = self.__piece_location(False)
        if bloc:
            s.b_col = ord(bloc[0]) - ord("A")
            s.b_row = int(bloc[1]) - 1
        # Walls (1-indexed -> 0-indexed)
        for col_l, row_1 in self.horizontal_walls:
            s.h_walls.add((ord(col_l) - ord("A"), row_1 - 1))
        for col_l, row_1 in self.vertical_walls:
            s.v_walls.add((ord(col_l) - ord("A"), row_1 - 1))
        s.p_sticks = self.sticks_left
        s.b_sticks = self.bot_sticks_left
        s.to_move = True  # always bot's turn when this is called
        return s

    def _blocker_pick_action(self):
        """Use the deterministic blocker strategy to pick the bot's move."""
        state = self._build_ml_state()
        move = bot_ml.pick_action_blocker(state, verbose=True)
        if move is None:
            print("  blocker: no move returned")
            return False

        kind = move[0]
        if kind in ("up", "down", "left", "right"):
            ok = self.validate_move(kind, False) == 0
            if not ok:
                print(f"  blocker: invalid move {kind}")
            return ok
        elif kind == "h_wall":
            wcol, wrow = move[1], move[2]
            col_l = chr(ord("A") + wcol)
            row_1 = wrow + 1
            wall = (col_l, row_1)
            if wall not in self.horizontal_walls and self.bot_sticks_left > 0:
                self.horizontal_walls.add(wall)
                y = 6 - row_1
                line_y = y * self.sqh
                self.draw_vine(wcol * self.sqw, line_y, (wcol + 1) * self.sqw, line_y, "#2E7D32")
                self.bot_sticks_left -= 1
                f.itemconfigure("botsticksval", text=str(self.bot_sticks_left))
                return True
            return False
        elif kind == "v_wall":
            wcol, wrow = move[1], move[2]
            col_l = chr(ord("A") + wcol)
            row_1 = wrow + 1
            wall = (col_l, row_1)
            if wall not in self.vertical_walls and self.bot_sticks_left > 0:
                self.vertical_walls.add(wall)
                y = 6 - row_1
                line_x = (wcol + 1) * self.sqw
                self.draw_vine(line_x, y * self.sqh, line_x, (y + 1) * self.sqh, "#2E7D32")
                self.bot_sticks_left -= 1
                f.itemconfigure("botsticksval", text=str(self.bot_sticks_left))
                return True
            return False
        return False

    def bot(self):
        if self.won:
            return
        r.after(1000, self.bot)

        self.bot_move_log = ""
        self._blocker_pick_action()

    def on_mouse_click(self, event):
        if self.won or self.sticks_left <= 0:
            return
        
        x2 = event.x // self.sqw
        y2 = event.y // self.sqh
        
        if x2 >= 6 or y2 >= 6 or x2 < 0 or y2 < 0: # Basically if the user clicks outside
            return
        
        # Calculate distance to all 4 edges of the clicked cell to determine stick orientation
        dist_left = event.x - (x2 * self.sqw)
        dist_right = ((x2 + 1) * self.sqw) - event.x
        dist_top = event.y - (y2 * self.sqh)
        dist_bottom = ((y2 + 1) * self.sqh) - event.y
        min_dist = min(dist_left, dist_right, dist_top, dist_bottom)

        placed = False
        if min_dist in (dist_top, dist_bottom):
            center_y = y2 * self.sqh + self.sqh // 2
            if event.y < center_y:
                wall_row = 6 - y2
                if wall_row < 6:
                    wall = (chr(ord('A') + x2), wall_row)
                    if wall not in self.horizontal_walls:
                        self.horizontal_walls.add(wall)
                        line_y = y2 * self.sqh
                        self.draw_vine(x2 * self.sqw, line_y, (x2 + 1) * self.sqw, line_y, "#4CAF50")
                        placed = True
            else:
                wall_row = 5 - y2
                if wall_row >= 1:
                    wall = (chr(ord('A') + x2), wall_row)
                    if wall not in self.horizontal_walls:
                        self.horizontal_walls.add(wall)
                        line_y = (y2 + 1) * self.sqh
                        self.draw_vine(x2 * self.sqw, line_y, (x2 + 1) * self.sqw, line_y, "#4CAF50")
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
                        self.draw_vine(line_x, y2 * self.sqh, line_x, (y2 + 1) * self.sqh, "#4CAF50")
                        placed = True
            else:
                if x2 < 5:
                    wall = (chr(ord('A') + x2), row_str)
                    if wall not in self.vertical_walls:
                        self.vertical_walls.add(wall)
                        line_x = (x2 + 1) * self.sqw
                        self.draw_vine(line_x, y2 * self.sqh, line_x, (y2 + 1) * self.sqh, "#4CAF50")
                        placed = True

        if placed:
            self.sticks_left -= 1
            f.itemconfigure("sticksval", text=str(self.sticks_left))

    def onplayerclick(self, event):
        key = event.keysym.lower()
        if key in ("up", "down", "left", "right"):
            self.validate_move(key, True)


c = Board()
c.draw_board()
c.draw_jungle_ambient()
c.show_notation()
c.draw_player(True, "C1", "C1", "down")
c.draw_player(False, "D6", "D6", "down")
c.draw_chests()
c.rightside()
c.bot()
c.animate_jungle()
c.check_win()
r.bind("<Key>", c.onplayerclick)
f.bind("<Button-1>", c.on_mouse_click)
f.focus_set()
r.mainloop()

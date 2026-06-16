import tkinter as tk
import random
import sys
import math
from random import randint, choice, uniform, shuffle
from PIL import Image, ImageTk
import numpy as np
from collections import deque


class GameState:
    """Minimal game state for simulation."""

    __slots__ = (
        "p_col", "p_row", "b_col", "b_row",
        "h_walls", "v_walls", "p_sticks", "b_sticks", "to_move",
        "p_destroys", "b_destroys",
    )

    def __init__(self):
        self.p_col = 2
        self.p_row = 0
        self.b_col = 3
        self.b_row = 5
        self.h_walls = set()
        self.v_walls = set()
        self.p_sticks = 4
        self.b_sticks = 4
        self.to_move = True
        self.p_destroys = 2
        self.b_destroys = 2

    def copy(self):
        s = GameState()
        s.p_col, s.p_row = self.p_col, self.p_row
        s.b_col, s.b_row = self.b_col, self.b_row
        s.h_walls = set(self.h_walls)
        s.v_walls = set(self.v_walls)
        s.p_sticks, s.b_sticks = self.p_sticks, self.b_sticks
        s.p_destroys, s.b_destroys = self.p_destroys, self.b_destroys
        s.to_move = self.to_move
        return s

    def is_terminal(self):
        if self.p_row == 5 or self.b_row == 0:
            return True
        return len(self.legal_moves(nearby_only=True)) == 0

    def result(self):
        if self.b_row == 0:
            return 1.0
        if self.p_row == 5:
            return -1.0
        if not self.legal_moves(nearby_only=True):
            if self.to_move:
                return -1.0
            else:
                return 1.0
        return 0.0

    def _occupied(self, col, row):
        return (col == self.p_col and row == self.p_row) or (
            col == self.b_col and row == self.b_row
        )

    def legal_moves(self, nearby_only=False):
        moves = []
        is_bot = self.to_move
        if is_bot:
            col = self.b_col
            row = self.b_row
            sticks = self.b_sticks
        else:
            col = self.p_col
            row = self.p_row
            sticks = self.p_sticks

        if (
            row < 5
            and (col, row) not in self.h_walls
            and not self._occupied(col, row + 1)
        ):
            moves.append(("up",))
        if (
            row > 0
            and (col, row - 1) not in self.h_walls
            and not self._occupied(col, row - 1)
        ):
            moves.append(("down",))
        if (
            col > 0
            and (col - 1, row) not in self.v_walls
            and not self._occupied(col - 1, row)
        ):
            moves.append(("left",))
        if (
            col < 5
            and (col, row) not in self.v_walls
            and not self._occupied(col + 1, row)
        ):
            moves.append(("right",))

        if sticks > 0:
            if nearby_only:
                player_row, player_col = self.p_row, self.p_col
                bot_row, bot_col = self.b_row, self.b_col
                seen = set()
                for row, col in [(player_row, player_col), (bot_row, bot_col)]:
                    for drow in range(-2, 3):
                        for dcol in range(-2, 3):
                            wall_row = row + drow
                            wall_col = col + dcol
                            if 0 <= wall_col < 6 and 0 <= wall_row < 5:
                                key = ("h", wall_col, wall_row)
                                if key not in seen and (wall_col, wall_row) not in self.h_walls:
                                    seen.add(key)
                                    moves.append(("h_wall", wall_col, wall_row))
                            if 0 <= wall_col < 5 and 0 <= wall_row < 6:
                                key = ("v", wall_col, wall_row)
                                if key not in seen and (wall_col, wall_row) not in self.v_walls:
                                    seen.add(key)
                                    moves.append(("v_wall", wall_col, wall_row))
            else:
                for wall_col in range(6):
                    for wall_row in range(5):
                        if (wall_col, wall_row) not in self.h_walls:
                            moves.append(("h_wall", wall_col, wall_row))
                for wall_col in range(5):
                    for wall_row in range(6):
                        if (wall_col, wall_row) not in self.v_walls:
                            moves.append(("v_wall", wall_col, wall_row))

        destroys = self.b_destroys if is_bot else self.p_destroys
        if destroys > 0:
            seen_destroy = set()
            if nearby_only:
                for drow in range(-2, 3):
                    for dcol in range(-2, 3):
                        wall_row = row + drow
                        wall_col = col + dcol
                        if 0 <= wall_col < 6 and 0 <= wall_row < 5:
                            key = ("dh", wall_col, wall_row)
                            if key not in seen_destroy and (wall_col, wall_row) in self.h_walls:
                                seen_destroy.add(key)
                                moves.append(("destroy_h", wall_col, wall_row))
                        if 0 <= wall_col < 5 and 0 <= wall_row < 6:
                            key = ("dv", wall_col, wall_row)
                            if key not in seen_destroy and (wall_col, wall_row) in self.v_walls:
                                seen_destroy.add(key)
                                moves.append(("destroy_v", wall_col, wall_row))
            else:
                for wall_col in range(6):
                    for wall_row in range(5):
                        if (wall_col, wall_row) in self.h_walls:
                            moves.append(("destroy_h", wall_col, wall_row))
                for wall_col in range(5):
                    for wall_row in range(6):
                        if (wall_col, wall_row) in self.v_walls:
                            moves.append(("destroy_v", wall_col, wall_row))

        random.shuffle(moves)
        return moves

    def apply(self, move):
        s = self.copy()
        kind = move[0]

        if kind == "up":
            if s.to_move:
                s.b_row += 1
            else:
                s.p_row += 1
        elif kind == "down":
            if s.to_move:
                s.b_row -= 1
            else:
                s.p_row -= 1
        elif kind == "left":
            if s.to_move:
                s.b_col -= 1
            else:
                s.p_col -= 1
        elif kind == "right":
            if s.to_move:
                s.b_col += 1
            else:
                s.p_col += 1
        elif kind == "h_wall":
            _, wall_col, wall_row = move
            s.h_walls.add((wall_col, wall_row))
            if s.to_move:
                s.b_sticks -= 1
            else:
                s.p_sticks -= 1
        elif kind == "v_wall":
            _, wall_col, wall_row = move
            s.v_walls.add((wall_col, wall_row))
            if s.to_move:
                s.b_sticks -= 1
            else:
                s.p_sticks -= 1
        elif kind == "destroy_h":
            _, wall_col, wall_row = move
            s.h_walls.discard((wall_col, wall_row))
            if s.to_move:
                s.b_destroys -= 1
            else:
                s.p_destroys -= 1
        elif kind == "destroy_v":
            _, wall_col, wall_row = move
            s.v_walls.discard((wall_col, wall_row))
            if s.to_move:
                s.b_destroys -= 1
            else:
                s.p_destroys -= 1

        s.to_move = not s.to_move
        return s

    def encode(self):
        f = np.zeros(134, dtype=np.float32)
        idx = 0
        f[self.p_col * 6 + self.p_row] = 1.0
        idx += 36
        f[idx + self.b_col * 6 + self.b_row] = 1.0
        idx += 36
        for wall_col in range(6):
            for wall_row in range(5):
                if (wall_col, wall_row) in self.h_walls:
                    f[idx] = 1.0
                idx += 1
        for wall_col in range(5):
            for wall_row in range(6):
                if (wall_col, wall_row) in self.v_walls:
                    f[idx] = 1.0
                idx += 1
        f[idx] = self.p_sticks / 4.0
        idx += 1
        f[idx] = self.b_sticks / 4.0
        return f


def _bfs_path(state, is_bot):
    if is_bot:
        start = (state.b_col, state.b_row)
        goal_row = 0
    else:
        start = (state.p_col, state.p_row)
        goal_row = 5

    visited = {start}
    queue = deque()
    queue.append((start, [start]))

    while queue:
        (col, row), path = queue.popleft()
        if row == goal_row:
            return path

        for drow, dcol in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
            next_col, next_row = col + dcol, row + drow
            if next_col < 0 or next_col > 5 or next_row < 0 or next_row > 5:
                continue
            if (next_col, next_row) in visited:
                continue
            if state._occupied(next_col, next_row):
                continue
            if drow == 1 and (col, row) in state.h_walls:
                continue
            if drow == -1 and (col, row - 1) in state.h_walls:
                continue
            if dcol == -1 and (col - 1, row) in state.v_walls:
                continue
            if dcol == 1 and (col, row) in state.v_walls:
                continue
            visited.add((next_col, next_row))
            queue.append(((next_col, next_row), path + [(next_col, next_row)]))

    return None


def _format_move(move):
    kind = move[0]
    if kind in ("up", "down", "left", "right"):
        return kind
    if kind == "h_wall":
        col = chr(ord("A") + move[1])
        row = move[2] + 1
        return f"h_wall {col}{row}-{col}{row+1}"
    if kind == "v_wall":
        col = chr(ord("A") + move[1])
        col2 = chr(ord("A") + move[1] + 1)
        row = move[2] + 1
        return f"v_wall {col}{row}-{col2}{row}"
    if kind == "destroy_h":
        col = chr(ord("A") + move[1])
        row = move[2] + 1
        return f"destroy_h {col}{row}-{col}{row+1}"
    if kind == "destroy_v":
        col = chr(ord("A") + move[1])
        col2 = chr(ord("A") + move[1] + 1)
        row = move[2] + 1
        return f"destroy_v {col}{row}-{col2}{row}"
    return str(move)


def _format_position(col, row):
    return f"{chr(ord('A') + col)}{row + 1}"


def _evaluate_state(state):
    """Score a game state from the bot's perspective. Higher is better."""
    score = 0

    bot_path = _bfs_path(state, is_bot=True)
    player_path = _bfs_path(state, is_bot=False)

    if bot_path and player_path:
        score += (len(player_path) - len(bot_path)) * 15

    if not player_path:
        score += 200

    if not bot_path:
        score -= 300

    if player_path and len(player_path) > 1:
        next_col, next_row = player_path[1]
        if next_col != state.p_col or next_row != state.p_row:
            if (state.p_col, state.p_row) in state.h_walls:
                score += 10
            if (next_col, next_row) in state.h_walls and next_row == state.p_row + 1:
                score += 10
            dcol = next_col - state.p_col
            if dcol == 1 and (state.p_col, state.p_row) in state.v_walls:
                score += 10
            if dcol == -1 and (next_col, state.p_row) in state.v_walls:
                score += 10

    return score


def pick_action_blocker(state, verbose=True):
    moves = state.legal_moves(nearby_only=True)
    if not moves:
        return None

    best_move = None
    best_score = -999999

    for move in moves:
        after_bot = state.apply(move)
        player_moves = after_bot.legal_moves(nearby_only=True)

        if not player_moves:
            score = _evaluate_state(after_bot) + 500
        else:
            worst_for_bot = 999999
            for pmove in player_moves:
                after_player = after_bot.apply(pmove)
                s = _evaluate_state(after_player)
                if s < worst_for_bot:
                    worst_for_bot = s
            score = worst_for_bot

        if score > best_score:
            best_score = score
            best_move = move

    if verbose:
        print(f"DEBUG:  blocker from {_format_position(state.b_col, state.b_row)}: "
              f"best is {_format_move(best_move)} (score={best_score})")

    return best_move


root = tk.Tk()

WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()
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


canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, background="#0B1F05")
canvas.pack()

WIDTH -= 200

SPRITE_SIZE = 64

class Board:
    def __init__(self):
        self.square_height = HEIGHT // 6
        self.square_width = WIDTH // 6
        self.board_data = {}
        self.check_who = True
        self.won = False
        self.player_last_dir = "down"
        self.bot_last_dir = "down"
        self.sticks_left = 4
        self.bot_sticks_left = 4
        self.horizontal_walls = set()
        self.vertical_walls = set()
        self.tick = 0
        self.snakes = []
        snake_colors = ["#2E5A3A", "#3D4A2A", "#1A4A4A", "#3A2A4A"]
        for i in range(2):
            speed_x = randint(-3, 3)
            if speed_x == 0:
                speed_x = 2
            speed_y = randint(-3, 3)
            if speed_y == 0:
                speed_y = -2
            self.snakes.append({
                "x": randint(0, WIDTH + 100),
                "y": randint(0, HEIGHT),
                "x_speed": speed_x,
                "y_speed": speed_y,
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

        self.player_sprites = {
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
        self.wall_colors = {}
        self.player_destroys = 2
        self.bot_destroys = 2
        self._instr_shown = False
        self.player_turn = True
        self.win_frame = 0
        self.win_type = None
        self.win_particles = []
        self.bot_move_log = ""
        
    def rightside(self): 
        panel_top = 50
        panel_left = WIDTH
        panel_right = WIDTH + 200
        
        panel_center_x = panel_left + 100
        panel_center_y = panel_top + 25
        canvas.create_text(panel_center_x, panel_center_y, text="Power-Ups", font=("Helvetica", 20, "underline", "bold"), tags="powerup", fill="#4CAF50")
        
        canvas.create_text(panel_center_x, panel_center_y + 80, text="Bot:", font=("Helvetica", 16, "bold"), tags="bottxt", fill="white")
        rect_size = 30
        rect_spacing = 15
        for i in range(3):
            x_offset = panel_center_x - 45 + i * (rect_size + rect_spacing)
            canvas.create_rectangle(x_offset, panel_center_y + 100, x_offset + rect_size, panel_center_y + 130, outline="#111", fill="#795548", tags=f"bot_rect{i}")
        
        canvas.create_text(panel_center_x, panel_center_y + 170, text="Player:", font=("Helvetica", 16, "bold"), tags="playertxt", fill="white")
        for i in range(3):
            x_offset = panel_center_x - 45 + i * (rect_size + rect_spacing)
            canvas.create_rectangle(x_offset, panel_center_y + 200, x_offset + rect_size, panel_center_y + 230, outline="#111", fill="#795548", tags=f"player_rect{i}")

        canvas.create_text(panel_center_x - 90, panel_center_y + 270, text="Sticks Left:", font=("Helvetica", 16, "bold"), anchor="w", tags="stickstxt", fill="white")
        canvas.create_text(panel_center_x + 75, panel_center_y + 270, text=str(self.sticks_left), font=("Helvetica", 16, "bold"), anchor="w", tags="sticksval", fill="#FFEB3B")

        canvas.create_text(panel_center_x - 90, panel_center_y + 310, text="Bot Sticks:", font=("Helvetica", 16, "bold"), anchor="w", tags="botstickstxt", fill="white")
        canvas.create_text(panel_center_x + 75, panel_center_y + 310, text=str(self.bot_sticks_left), font=("Helvetica", 16, "bold"), anchor="w", tags="botsticksval", fill="#FF9800")

        canvas.create_text(panel_center_x - 90, panel_center_y + 350, text="Destroys:", font=("Helvetica", 16, "bold"), anchor="w", tags="destroytxt", fill="white")
        canvas.create_text(panel_center_x + 75, panel_center_y + 350, text=str(self.player_destroys), font=("Helvetica", 16, "bold"), anchor="w", tags="destroysval", fill="#FF5722")

        self._draw_powerups()

    def __piece_location(self, is_player: bool):
        for square, (_, _, occupant) in self.board_data.items():
            if occupant == is_player:
                return square
        return None

    def __progression(self, character) -> str:
        if character == "None":
            return "None"
        column_letter, row_digit = character[0], character[1]
        column_letter = ord(column_letter)
        if column_letter == 70:
            if row_digit == "1":
                return "None"
            return f"A{int(row_digit)-1}"
        return f"{chr(column_letter+1)}{row_digit}"

    def draw_player(self, is_player: bool, current: str, target: str, direction: str = None):
        x, y, _ = self.board_data[current]
        x2, y2, _ = self.board_data[target]

        if is_player:
            if direction:
                self.player_last_dir = direction
            sprite = self.player_sprites[self.player_last_dir]
            canvas.delete("pl")
            canvas.create_image(x2, y2, image=sprite, anchor="center", tags="pl")
        else:
            if direction:
                self.bot_last_dir = direction
            sprite = self.bot_sprites[self.bot_last_dir]
            canvas.delete("bot")
            canvas.create_image(x2, y2, image=sprite, anchor="center", tags="bot")

        self.board_data[current] = (x, y, None)
        self.board_data[target] = (x2, y2, is_player)

    def show_notation(self):
        start = "A6"
        for _ in range(6):
            for _ in range(6):
                x, y, _ = self.board_data.get(start)
                canvas.create_text(x, y, text=start, fill="#8BC34A",
                              font=("Helvetica", 20, "bold"), tags="notation")
                start = self.__progression(start)

    def _place_chests(self):
        available = []
        for col in ["A", "B", "C", "D", "E", "F"]:
            for row in range(2, 6):
                available.append(f"{col}{row}")
        for _ in range(randint(3, 4)):
            square = choice(available)
            available.remove(square)
            self.chests[square] = "closed"

    def draw_chests(self):
        canvas.delete("chest")
        for square, state in self.chests.items():
            data = self.board_data.get(square)
            if data:
                x, y, _ = data
                sprite = self.chest_sprites[state]
                canvas.create_image(x, y, image=sprite, anchor="center", tags="chest")
        if canvas.find_withtag("pl"):
            canvas.tag_lower("chest", "pl")
        if canvas.find_withtag("bot"):
            canvas.tag_lower("chest", "bot")

    def _draw_powerups(self):
        canvas.delete("pu_indicator")
        panel_center_x = WIDTH + 100
        panel_center_y = 75
        rect_size = 30
        rect_spacing = 15

        for i, powerup in enumerate(self.bot_powerups[:3]):
            x_offset = panel_center_x - 45 + i * (rect_size + rect_spacing)
            center_x = x_offset + rect_size // 2
            center_y = panel_center_y + 100 + rect_size // 2
            if powerup == "extra_stick":
                canvas.create_oval(center_x - 8, center_y - 8, center_x + 8, center_y + 8,
                             fill="#4CAF50", outline="", tags="pu_indicator")
                canvas.create_text(center_x, center_y, text="+", font=("Helvetica", 16, "bold"),
                             fill="white", tags="pu_indicator")
            elif powerup == "erase_stick":
                canvas.create_oval(center_x - 8, center_y - 8, center_x + 8, center_y + 8,
                             fill="#F44336", outline="", tags="pu_indicator")
                canvas.create_text(center_x, center_y, text="-", font=("Helvetica", 16, "bold"),
                             fill="white", tags="pu_indicator")
            elif powerup == "split":
                canvas.create_oval(center_x - 8, center_y - 8, center_x + 8, center_y + 8,
                             fill="#9C27B0", outline="", tags="pu_indicator")
                canvas.create_text(center_x, center_y, text="=", font=("Helvetica", 14, "bold"),
                             fill="white", tags="pu_indicator")
            elif powerup == "maze":
                canvas.create_rectangle(center_x - 8, center_y - 8, center_x + 8, center_y + 8,
                                  fill="#FF5722", outline="", tags="pu_indicator")
                canvas.create_text(center_x, center_y, text="#", font=("Helvetica", 14, "bold"),
                             fill="white", tags="pu_indicator")

        for i, powerup in enumerate(self.player_powerups[:3]):
            x_offset = panel_center_x - 45 + i * (rect_size + rect_spacing)
            center_x = x_offset + rect_size // 2
            center_y = panel_center_y + 200 + rect_size // 2
            if powerup == "extra_stick":
                canvas.create_oval(center_x - 8, center_y - 8, center_x + 8, center_y + 8,
                             fill="#4CAF50", outline="", tags="pu_indicator")
                canvas.create_text(center_x, center_y, text="+", font=("Helvetica", 16, "bold"),
                             fill="white", tags="pu_indicator")
            elif powerup == "erase_stick":
                canvas.create_oval(center_x - 8, center_y - 8, center_x + 8, center_y + 8,
                             fill="#F44336", outline="", tags="pu_indicator")
                canvas.create_text(center_x, center_y, text="-", font=("Helvetica", 16, "bold"),
                             fill="white", tags="pu_indicator")
            elif powerup == "split":
                canvas.create_oval(center_x - 8, center_y - 8, center_x + 8, center_y + 8,
                             fill="#9C27B0", outline="", tags="pu_indicator")
                canvas.create_text(center_x, center_y, text="=", font=("Helvetica", 14, "bold"),
                             fill="white", tags="pu_indicator")
            elif powerup == "maze":
                canvas.create_rectangle(center_x - 8, center_y - 8, center_x + 8, center_y + 8,
                                  fill="#FF5722", outline="", tags="pu_indicator")
                canvas.create_text(center_x, center_y, text="#", font=("Helvetica", 14, "bold"),
                             fill="white", tags="pu_indicator")

    def _award_powerup(self, is_player):
        powerup = choice(["extra_stick", "erase_stick", "split", "maze"])
        print(f"DEBUG: awarded powerup '{powerup}' to {'player' if is_player else 'bot'}")

        if is_player:
            self.player_powerups.append(powerup)
            if powerup == "extra_stick":
                self.sticks_left += 1
            elif powerup == "erase_stick":
                self.horizontal_walls.clear()
                self.vertical_walls.clear()
                self.wall_colors.clear()
                canvas.delete("wall")
            elif powerup == "split":
                self._activate_split()
            elif powerup == "maze":
                self._activate_maze()
        else:
            self.bot_powerups.append(powerup)
            if powerup == "extra_stick":
                self.bot_sticks_left += 1
            elif powerup == "erase_stick":
                self.horizontal_walls.clear()
                self.vertical_walls.clear()
                self.wall_colors.clear()
                canvas.delete("wall")
            elif powerup == "split":
                self._activate_split()
            elif powerup == "maze":
                self._activate_maze()

        self._draw_powerups()
        canvas.itemconfigure("sticksval", text=str(self.sticks_left))
        canvas.itemconfigure("botsticksval", text=str(self.bot_sticks_left))

    def _activate_split(self):
        self.horizontal_walls.clear()
        self.vertical_walls.clear()
        self.wall_colors.clear()
        canvas.delete("wall")

        split_row = 3
        left_bridge_col = 1
        right_bridge_col = 4
        for col_idx in range(6):
            if col_idx == left_bridge_col or col_idx == right_bridge_col:
                continue
            col_letter = chr(ord("A") + col_idx)
            self.horizontal_walls.add((col_letter, split_row))
            self.wall_colors[("h", col_letter, split_row)] = "#9C27B0"
            grid_y = 6 - split_row
            line_y = grid_y * self.square_height
            x1 = col_idx * self.square_width
            x2 = (col_idx + 1) * self.square_width
            self.draw_vine(x1, line_y, x2, line_y, "#9C27B0")

        player_pos = self.__piece_location(True)
        if player_pos:
            self.draw_player(True, player_pos, "C1", "down")
        bot_pos = self.__piece_location(False)
        if bot_pos:
            self.draw_player(False, bot_pos, "D6", "down")

    def _activate_maze(self):
        state = GameState()
        player_pos = self.__piece_location(True)
        bot_pos = self.__piece_location(False)
        if player_pos:
            state.p_col = ord(player_pos[0]) - ord("A")
            state.p_row = int(player_pos[1]) - 1
        if bot_pos:
            state.b_col = ord(bot_pos[0]) - ord("A")
            state.b_row = int(bot_pos[1]) - 1

        self.horizontal_walls.clear()
        self.vertical_walls.clear()
        self.wall_colors.clear()
        canvas.delete("wall")

        candidates = []
        for col in range(6):
            for row in range(5):
                candidates.append(("h", col, row))
        for col in range(5):
            for row in range(6):
                candidates.append(("v", col, row))
        shuffle(candidates)

        placed = 0
        maze_color = "#FF5722"

        for kind, col, row in candidates:
            if kind == "h":
                if (col, row) in state.h_walls:
                    continue
                state.h_walls.add((col, row))
            else:
                if (col, row) in state.v_walls:
                    continue
                state.v_walls.add((col, row))

            bot_path = _bfs_path(state, is_bot=True)
            player_path = _bfs_path(state, is_bot=False)

            if bot_path and player_path:
                placed += 1
                col_letter = chr(ord("A") + col)
                if kind == "h":
                    self.horizontal_walls.add((col_letter, row + 1))
                    self.wall_colors[("h", col_letter, row + 1)] = maze_color
                    grid_y = 6 - (row + 1)
                    line_y = grid_y * self.square_height
                    x1 = col * self.square_width
                    x2 = (col + 1) * self.square_width
                    self.draw_vine(x1, line_y, x2, line_y, maze_color)
                else:
                    self.vertical_walls.add((col_letter, row + 1))
                    self.wall_colors[("v", col_letter, row + 1)] = maze_color
                    y_grid = 6 - (row + 1)
                    line_x = (col + 1) * self.square_width
                    self.draw_vine(line_x, y_grid * self.square_height,
                                   line_x, (y_grid + 1) * self.square_height, maze_color)
            else:
                if kind == "h":
                    state.h_walls.remove((col, row))
                else:
                    state.v_walls.remove((col, row))

        print(f"DEBUG: maze activated — {placed} walls placed out of {len(candidates)} candidates")

    def _redraw_all_walls(self):
        canvas.delete("wall")
        for col_letter, row_number in self.horizontal_walls:
            col_idx = ord(col_letter) - ord("A")
            grid_y = 6 - row_number
            line_y = grid_y * self.square_height
            x1 = col_idx * self.square_width
            x2 = (col_idx + 1) * self.square_width
            color = self.wall_colors.get(("h", col_letter, row_number), "#4CAF50")
            self.draw_vine(x1, line_y, x2, line_y, color)
        for col_letter, row_number in self.vertical_walls:
            col_idx = ord(col_letter) - ord("A")
            y_grid = 6 - row_number
            line_x = (col_idx + 1) * self.square_width
            color = self.wall_colors.get(("v", col_letter, row_number), "#2E7D32")
            self.draw_vine(line_x, y_grid * self.square_height,
                           line_x, (y_grid + 1) * self.square_height, color)

    def _destroy_wall(self, event):
        if not self.player_turn:
            return
        grid_x = event.x // self.square_width
        grid_y = event.y // self.square_height
        if grid_x >= 6 or grid_y >= 6 or grid_x < 0 or grid_y < 0 or self.won:
            return
        if self.player_destroys <= 0:
            return

        dist_left = event.x - (grid_x * self.square_width)
        dist_right = ((grid_x + 1) * self.square_width) - event.x
        dist_top = event.y - (grid_y * self.square_height)
        dist_bottom = ((grid_y + 1) * self.square_height) - event.y
        min_dist = min(dist_left, dist_right, dist_top, dist_bottom)

        removed = False
        if min_dist in (dist_top, dist_bottom):
            center_y = grid_y * self.square_height + self.square_height // 2
            if event.y < center_y:
                wall_row = 6 - grid_y
            else:
                wall_row = 5 - grid_y
            wall = (chr(ord("A") + grid_x), wall_row)
            if wall in self.horizontal_walls:
                self.horizontal_walls.remove(wall)
                self.wall_colors.pop(("h", wall[0], wall[1]), None)
                removed = True
        else:
            row_str = 6 - grid_y
            if event.x < grid_x * self.square_width + self.square_width // 2:
                if grid_x > 0:
                    wall = (chr(ord("A") + grid_x - 1), row_str)
                else:
                    return
            else:
                if grid_x < 5:
                    wall = (chr(ord("A") + grid_x), row_str)
                else:
                    return
            if wall in self.vertical_walls:
                self.vertical_walls.remove(wall)
                self.wall_colors.pop(("v", wall[0], wall[1]), None)
                removed = True

        if removed:
            self.player_destroys -= 1
            self._redraw_all_walls()
            canvas.itemconfigure("destroysval", text=str(self.player_destroys))
            self.player_turn = False

    def _draw_leaf_shape(self, x1, y1, angle, size, color, outline_color, tag="wall"):
        angle_rad = math.radians(angle)
        half_width = size * 0.35
        points = []
        for t_rel in range(0, 181, 12):
            t = t_rel / 180
            along = -size + t * size * 2
            width = half_width * math.sin(t * math.pi)
            x = x1 + along * math.cos(angle_rad) - width * math.sin(angle_rad)
            y = y1 + along * math.sin(angle_rad) + width * math.cos(angle_rad)
            points.append(x)
            points.append(y)
        canvas.create_polygon(*points, fill=color, outline=outline_color, width=1,
                        smooth=True, tags=tag)
        x2 = x1 + size * 0.7 * math.cos(angle_rad)
        y2 = y1 + size * 0.7 * math.sin(angle_rad)
        canvas.create_line(x1, y1, x2, y2, fill=outline_color, width=1, tags=tag)

    def _draw_leaf_cluster(self, x1, y1, vine_angle):
        colors = ["#1B5E20", "#2E7D32", "#388E3C", "#43A047"]
        for i in range(randint(2, 4)):
            offset = randint(-50, 50)
            size = randint(7, 13)
            self._draw_leaf_shape(
                x1 + randint(-3, 3), y1 + randint(-3, 3),
                vine_angle + offset, size, choice(colors), "#0B3D0B"
            )

    def _draw_tendril(self, x1, y1, angle, length):
        points = []
        x, y = x1, y1
        for i in range(24):
            t = i / 24
            angle2 = angle + math.sin(t * math.pi * 5) * 40
            x += math.cos(math.radians(angle2)) * length / 24
            y += math.sin(math.radians(angle2)) * length / 24
            points.extend([x, y])
        canvas.create_line(*points, fill="#4CAF50", width=1, smooth=True, tags="wall")

    def draw_vine(self, x1, y1, x2, y2, color):
        segments = 14
        horiz = y1 == y2

        points = []
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
            points.extend([x, y])

        canvas.create_line(*points, fill="#0B3D0B", width=7, smooth=True, tags="wall", capstyle="round")
        canvas.create_line(*points, fill=color, width=5, smooth=True, tags="wall", capstyle="round")
        canvas.create_line(*points, fill="#66BB6A", width=2, smooth=True, tags="wall", capstyle="round")

        if horiz:
            vine_angle = 0
        else:
            vine_angle = 90
        for i in range(2, segments, 3):
            x, y = points[i * 2], points[i * 2 + 1]
            if i % 2 == 0:
                side = 90
            else:
                side = -90
            self._draw_leaf_cluster(x, y, vine_angle + side)

        if randint(0, 2) == 0:
            idx = randint(2, segments - 2)
            x, y = points[idx * 2], points[idx * 2 + 1]
            self._draw_tendril(x, y, vine_angle + choice([-60, 60]), randint(15, 25))

    def _draw_grass_blade(self, x, y, height, lean):
        canvas.create_line(
            x, y,
            x + lean * 0.3, y - height * 0.6,
            x + lean, y - height,
            fill=choice(["#4CAF50", "#66BB6A", "#388E3C", "#2E7D32"]),
            width=1, smooth=True, tags="tile_detail"
        )

    def _draw_tile_texture(self, x, y, square_width, square_height, dark_shade):
        for _ in range(randint(2, 4)):
            x1 = x + randint(6, square_width - 6)
            y1 = y + randint(6, square_height - 6)
            radius = randint(3, 7)
            canvas.create_oval(x1 - radius, y1 - radius, x1 + radius, y1 + radius,
                         fill=dark_shade, outline="", tags="tile_detail")

        for _ in range(randint(4, 7)):
            x1 = x + randint(4, square_width - 4)
            y1 = y + square_height - randint(2, 5)
            h = randint(5, 12)
            lean = randint(-4, 4)
            self._draw_grass_blade(x1, y1, h, lean)

        for _ in range(randint(1, 3)):
            x1 = x + randint(8, square_width - 8)
            y1 = y + randint(8, square_height - 8)
            canvas.create_oval(x1 - 1, y1 - 1, x1 + 1, y1 + 1,
                         fill="#8BC34A", outline="", tags="tile_detail")

    def draw_board(self):
        pad = 5
        canvas.create_rectangle(-pad, -pad, WIDTH + pad, HEIGHT + pad,
                          fill="#0B3D0B", outline="#071F05", tags="board_border")
        canvas.create_rectangle(0, 0, WIDTH, HEIGHT,
                          fill="", outline="#1A5C1A", width=2, tags="board_border")

        current = "A6"
        for i in range(6):
            for x in range(6):
                is_dark = (x + i) % 2 == 0
                if is_dark:
                    base = "#2E4A1E"
                    dark = "#1A3A0E"
                else:
                    base = "#233D14"
                    dark = "#152B0B"

                x1 = x * self.square_width
                y1 = i * self.square_height

                canvas.create_rectangle(
                    x1, y1, x1 + self.square_width, y1 + self.square_height,
                    fill=base, outline="#1A2E0C", tags="square"
                )

                self._draw_tile_texture(x1, y1, self.square_width, self.square_height, dark)

                x_center = x1 + self.square_width // 2
                y_center = y1 + self.square_height // 2
                self.board_data[current] = (x_center, y_center, None)
                current = self.__progression(current)

    def draw_jungle_ambient(self):
        for i in range(10):
            x = randint(10, WIDTH - 10)
            vine_len = randint(50, 140)
            points = []
            for j in range(12):
                t = j / 12
                sway = math.sin(t * math.pi * 2.5) * 10 * t
                points.extend([x + sway, -5 + vine_len * t])
            canvas.create_line(*points, fill="#1B5E20", width=3, smooth=True, tags="bg_foliage")
            self._draw_leaf_shape(
                points[-2], points[-1] - 5, 90 + randint(-20, 20),
                randint(8, 13), choice(["#2E7D32", "#388E3C"]), "#0B3D0B",
                tag="bg_foliage"
            )

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

        for i in range(8):
            x = i * (WIDTH // 7) + randint(5, 25)
            y = HEIGHT - randint(3, 12)
            for _ in range(6):
                x_offset = randint(-18, 18)
                y_offset = randint(-12, 4)
                size = randint(7, 15)
                canvas.create_oval(x + x_offset - size, y + y_offset - size, x + x_offset + size, y + y_offset + size,
                             fill="#1B5E20", outline="#0B3D0B", tags="bg_foliage")

        canvas.tag_lower("bg_foliage")
        canvas.tag_lower("board_border")

    def animate_jungle(self):
        if self.won:
            self._animate_win()
            canvas.after(50, self.animate_jungle)
            return
        
        self.tick += 1

        for firefly in self.fireflies:
            firefly["x"] += firefly["speed_x"]
            firefly["y"] += firefly["speed_y"]

            if firefly["x"] < 0 or firefly["x"] > WIDTH:
                firefly["speed_x"] *= -1
            if firefly["y"] < 0 or firefly["y"] > HEIGHT:
                firefly["speed_y"] *= -1

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

            canvas.delete(firefly["tag"])

            glow_size = 2 + int(3 * glow)
            canvas.create_oval(
                firefly["x"] - glow_size, firefly["y"] - glow_size,
                firefly["x"] + glow_size, firefly["y"] + glow_size,
                fill=color, outline="", tags=firefly["tag"]
            )
            core_size = 1 + int(1 * glow)
            canvas.create_oval(
                firefly["x"] - core_size, firefly["y"] - core_size,
                firefly["x"] + core_size, firefly["y"] + core_size,
                fill="#CCDDAA", outline="", tags=firefly["tag"]
            )

            canvas.tag_raise(firefly["tag"])

        for chest in self.vanishing_chests[:]:
            chest["frame"] += 1
            tag = f"vanish_{chest['square']}"
            canvas.delete(tag)

            if chest["frame"] >= chest["max_frames"]:
                self.vanishing_chests.remove(chest)
                continue

            progress = chest["frame"] / chest["max_frames"]
            x1, y1 = chest["x"], chest["y"]

            radius = 5 + progress * 28
            r = int(255 * (1 - progress))
            g = int(220 * (1 - progress))
            b = int(50 * (1 - progress))
            glow_color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_oval(x1 - radius, y1 - radius, x1 + radius, y1 + radius,
                          fill=glow_color, outline="", tags=tag)

            for i in range(10):
                angle = i * math.pi / 5 + progress * 3
                dist = 5 + progress * 35
                x2 = x1 + math.cos(angle) * dist
                y2 = y1 + math.sin(angle) * dist
                size = max(1, 5 - int(progress * 5))
                r = int(255 * (1 - progress))
                g = int(255 * (1 - progress))
                b = int(200 * (1 - progress))
                color = f"#{r:02x}{g:02x}{b:02x}"
                canvas.create_oval(x2 - size, y2 - size, x2 + size, y2 + size,
                              fill=color, outline="", tags=tag)

            canvas.tag_raise(tag)

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

            canvas.delete(snake["tags"])

            if len(snake["history"]) > 1:
                for i in range(len(snake["history"]) - 1):
                    x1, y1 = snake["history"][i]
                    x2, y2 = snake["history"][i + 1]
                    w = max(1, 3 - int((i / snake["length"]) * 2))
                    canvas.create_line(x1, y1, x2, y2, fill=snake["color"], width=w,
                                 tags=snake["tags"], capstyle="round")

            if canvas.find_withtag("square"):
                canvas.tag_raise(snake["tags"], "square")
            if canvas.find_withtag("pl"):
                canvas.tag_lower(snake["tags"], "pl")
            if canvas.find_withtag("bot"):
                canvas.tag_lower(snake["tags"], "bot")
            if canvas.find_withtag("wall"):
                canvas.tag_lower(snake["tags"], "wall")

        canvas.after(50, self.animate_jungle)

    def validate_move(self, command: str, is_player: bool):
        location = self.__piece_location(is_player)
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

        self.draw_player(is_player, location, target, direction)
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
            if is_player:
                print("DEBUG: Player touches chest")
            else:
                print("DEBUG: Bot touches chest")
            self._award_powerup(is_player)
        return 0

    def check_win(self):
        location = self.__piece_location(self.check_who)
        if location is None:
            if not self.won:
                root.after(50, self.check_win)
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
            root.after(50, self.check_win)

    def _draw_win_screen(self):
        is_win = self.win_type == "player"
        canvas_width = WIDTH + 200

        if is_win:
            overlay = "#0A1F05"
        else:
            overlay = "#1F0505"
        canvas.create_rectangle(0, 0, canvas_width, HEIGHT, fill=overlay, tags="win_overlay")

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

        canvas.create_text(x1 + 3, y1 + 3, text=title,
                      font=("Helvetica", 64, "bold"), fill=shadow_color, tags="win_title_shadow")
        canvas.create_text(x1, y1, text=title,
                      font=("Helvetica", 64, "bold"), fill=title_color, tags="win_title")

        if is_win:
            subtitle = "You reached the other side!"
        else:
            subtitle = "The bot beat you!"
        canvas.create_text(x1, y1 + 60, text=subtitle,
                      font=("Helvetica", 20), fill="#CCCCCC", tags="win_subtitle")

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
        self.win_frame += 1
        is_win = self.win_type == "player"
        canvas_width = WIDTH + 200
        x1 = canvas_width // 2
        y1 = HEIGHT // 2 - 30

        canvas.delete("win_glow")
        pulse = abs(math.sin(self.win_frame * 0.06))
        glow_radius = 40 + int(30 * pulse)
        intensity = int(60 * pulse)
        if is_win:
            glow_color = f"#{intensity:02x}{int(intensity*0.85):02x}00"
        else:
            glow_color = f"#{intensity:02x}0000"
        canvas.create_oval(x1 - glow_radius, y1 - glow_radius,
                      x1 + glow_radius, y1 + glow_radius,
                      fill=glow_color, outline="", tags="win_glow")
        canvas.tag_lower("win_glow", "win_title_shadow")

        bounce = int(math.sin(self.win_frame * 0.08) * 3)
        canvas.coords("win_title", x1, y1 + bounce)
        canvas.coords("win_title_shadow", x1 + 3, y1 + bounce + 3)

        for p in self.win_particles[:]:
            canvas.delete(p["tag"])
            p["x"] += p["speed_x"] + math.sin(self.win_frame * 0.04 + p["phase"]) * 0.3
            p["y"] += p["speed_y"]

            if p["y"] < -30 or p["y"] > HEIGHT + 30:
                p["x"] = randint(0, canvas_width)
                if is_win:
                    p["y"] = randint(-30, -5)
                else:
                    p["y"] = HEIGHT + randint(5, 30)

            if 0 <= p["y"] <= HEIGHT:
                canvas.create_oval(p["x"] - p["size"], p["y"] - p["size"],
                              p["x"] + p["size"], p["y"] + p["size"],
                              fill=p["color"], outline="", tags=p["tag"])

    def _build_ml_state(self):
        state = GameState()
        player_location = self.__piece_location(True)
        if player_location:
            state.p_col = ord(player_location[0]) - ord("A")
            state.p_row = int(player_location[1]) - 1
        bot_location = self.__piece_location(False)
        if bot_location:
            state.b_col = ord(bot_location[0]) - ord("A")
            state.b_row = int(bot_location[1]) - 1
        for column_letter, row_number in self.horizontal_walls:
            state.h_walls.add((ord(column_letter) - ord("A"), row_number - 1))
        for column_letter, row_number in self.vertical_walls:
            state.v_walls.add((ord(column_letter) - ord("A"), row_number - 1))
        state.p_sticks = self.sticks_left
        state.b_sticks = self.bot_sticks_left
        state.p_destroys = self.player_destroys
        state.b_destroys = self.bot_destroys
        state.to_move = True
        return state

    def _blocker_pick_action(self):
        state = self._build_ml_state()
        move = pick_action_blocker(state, verbose=True)
        if move is None:
            print("DEBUG:  blocker: no move returned")
            return False

        kind = move[0]
        if kind in ("up", "down", "left", "right"):
            ok = self.validate_move(kind, False) == 0
            if not ok:
                print(f"DEBUG:  blocker: invalid move {kind}")
            return ok
        elif kind == "h_wall":
            wall_column, wall_row = move[1], move[2]
            column_letter = chr(ord("A") + wall_column)
            row_number = wall_row + 1
            wall = (column_letter, row_number)
            if wall not in self.horizontal_walls and self.bot_sticks_left > 0:
                self.horizontal_walls.add(wall)
                self.wall_colors[("h", wall[0], wall[1])] = "#2E7D32"
                y = 6 - row_number
                line_y = y * self.square_height
                self.draw_vine(wall_column * self.square_width, line_y, (wall_column + 1) * self.square_width, line_y, "#2E7D32")
                self.bot_sticks_left -= 1
                canvas.itemconfigure("botsticksval", text=str(self.bot_sticks_left))
                return True
            return False
        elif kind == "v_wall":
            wall_column, wall_row = move[1], move[2]
            column_letter = chr(ord("A") + wall_column)
            row_number = wall_row + 1
            wall = (column_letter, row_number)
            if wall not in self.vertical_walls and self.bot_sticks_left > 0:
                self.vertical_walls.add(wall)
                self.wall_colors[("v", wall[0], wall[1])] = "#2E7D32"
                y = 6 - row_number
                line_x = (wall_column + 1) * self.square_width
                self.draw_vine(line_x, y * self.square_height, line_x, (y + 1) * self.square_height, "#2E7D32")
                self.bot_sticks_left -= 1
                canvas.itemconfigure("botsticksval", text=str(self.bot_sticks_left))
                return True
            return False
        elif kind == "destroy_h":
            wall_column, wall_row = move[1], move[2]
            col_letter = chr(ord("A") + wall_column)
            row_number = wall_row + 1
            wall = (col_letter, row_number)
            if wall in self.horizontal_walls and self.bot_destroys > 0:
                self.horizontal_walls.remove(wall)
                self.wall_colors.pop(("h", wall[0], wall[1]), None)
                self.bot_destroys -= 1
                self._redraw_all_walls()
                return True
            return False
        elif kind == "destroy_v":
            wall_column, wall_row = move[1], move[2]
            col_letter = chr(ord("A") + wall_column)
            row_number = wall_row + 1
            wall = (col_letter, row_number)
            if wall in self.vertical_walls and self.bot_destroys > 0:
                self.vertical_walls.remove(wall)
                self.wall_colors.pop(("v", wall[0], wall[1]), None)
                self.bot_destroys -= 1
                self._redraw_all_walls()
                return True
            return False
        return False

    def bot(self):
        if self.won:
            return
        root.after(1000, self.bot)

        self.bot_move_log = ""
        self._blocker_pick_action()
        self.player_turn = True

    def on_mouse_click(self, event):
        if self.won or self.sticks_left <= 0 or not self.player_turn:
            return
        
        grid_x = event.x // self.square_width
        grid_y = event.y // self.square_height
        
        if grid_x >= 6 or grid_y >= 6 or grid_x < 0 or grid_y < 0:
            return
        
        dist_left = event.x - (grid_x * self.square_width)
        dist_right = ((grid_x + 1) * self.square_width) - event.x
        dist_top = event.y - (grid_y * self.square_height)
        dist_bottom = ((grid_y + 1) * self.square_height) - event.y
        min_dist = min(dist_left, dist_right, dist_top, dist_bottom)

        placed = False
        if min_dist in (dist_top, dist_bottom):
            center_y = grid_y * self.square_height + self.square_height // 2
            if event.y < center_y:
                wall_row = 6 - grid_y
                if wall_row < 6:
                    wall = (chr(ord('A') + grid_x), wall_row)
                    if wall not in self.horizontal_walls:
                        self.horizontal_walls.add(wall)
                        self.wall_colors[("h", wall[0], wall[1])] = "#4CAF50"
                        line_y = grid_y * self.square_height
                        self.draw_vine(grid_x * self.square_width, line_y, (grid_x + 1) * self.square_width, line_y, "#4CAF50")
                        placed = True
            else:
                wall_row = 5 - grid_y
                if wall_row >= 1:
                    wall = (chr(ord('A') + grid_x), wall_row)
                    if wall not in self.horizontal_walls:
                        self.horizontal_walls.add(wall)
                        self.wall_colors[("h", wall[0], wall[1])] = "#4CAF50"
                        line_y = (grid_y + 1) * self.square_height
                        self.draw_vine(grid_x * self.square_width, line_y, (grid_x + 1) * self.square_width, line_y, "#4CAF50")
                        placed = True
        else:
            center_x = grid_x * self.square_width + self.square_width // 2
            row_str = 6 - grid_y
            if event.x < center_x:
                if grid_x > 0:
                    wall = (chr(ord('A') + grid_x - 1), row_str)
                    if wall not in self.vertical_walls:
                        self.vertical_walls.add(wall)
                        self.wall_colors[("v", wall[0], wall[1])] = "#4CAF50"
                        line_x = grid_x * self.square_width
                        self.draw_vine(line_x, grid_y * self.square_height, line_x, (grid_y + 1) * self.square_height, "#4CAF50")
                        placed = True
            else:
                if grid_x < 5:
                    wall = (chr(ord('A') + grid_x), row_str)
                    if wall not in self.vertical_walls:
                        self.vertical_walls.add(wall)
                        self.wall_colors[("v", wall[0], wall[1])] = "#4CAF50"
                        line_x = (grid_x + 1) * self.square_width
                        self.draw_vine(line_x, grid_y * self.square_height, line_x, (grid_y + 1) * self.square_height, "#4CAF50")
                        placed = True

        if placed:
            self.sticks_left -= 1
            canvas.itemconfigure("sticksval", text=str(self.sticks_left))
            self.player_turn = False

    def onplayerclick(self, event):
        if not self.player_turn:
            return
        key = event.keysym.lower()
        if key in ("up", "down", "left", "right"):
            if self.validate_move(key, True) == 0:
                self.player_turn = False

    def _draw_start_screen(self):
        canvas.delete("menu")
        canvas.delete("instructions_overlay")

        c1 = WIDTH + 200
        c2 = c1 // 2
        canvas.create_rectangle(0, 0, c1, HEIGHT,
                               fill="#0A1A08", tags="menu")

        for i in range(6):
            x = randint(20, c1 - 20)
            vine_len = randint(80, 160)
            l1 = []
            for j in range(14):
                t = j / 14
                sway = math.sin(t * math.pi * 3) * 15 * t
                l1.extend([x + sway, -10 + vine_len * t])
            canvas.create_line(*l1, fill="#1B5E20", width=3, smooth=True, tags="menu")
            l2, l3 = l1[-2], l1[-1]
            for _ in range(2):
                self._draw_leaf_shape(
                    l2 + randint(-8, 8), l3 - 5,
                    90 + randint(-30, 30), randint(10, 16),
                    choice(["#2E7D32", "#388E3C"]), "#0B3D0B", tag="menu"
                )

        title_y = HEIGHT // 3 - 20
        canvas.create_text(c2 + 3, title_y + 3, text="JUNGLE RUSH",
                          font=("Helvetica", 52, "bold"), fill="#0B3D0B", tags="menu")
        canvas.create_text(c2, title_y, text="JUNGLE RUSH",
                          font=("Helvetica", 52, "bold"), fill="#4CAF50", tags="menu")

        self._draw_leaf_shape(c2 - 210, title_y - 6, 0, 18, "#2E7D32", "#0B3D0B", tag="menu")
        self._draw_leaf_shape(c2 + 210, title_y - 6, 180, 18, "#2E7D32", "#0B3D0B", tag="menu")

        canvas.create_text(c2, title_y + 55, text="Outrun the Bot",
                          font=("Helvetica", 18), fill="#8BC34A", tags="menu")

        btn_w, btn_h = 240, 56
        start_y = title_y + 120
        self.start_btn = (c2 - btn_w // 2, start_y, c2 + btn_w // 2, start_y + btn_h)
        canvas.create_rectangle(*self.start_btn, fill="#1B5E20", outline="#4CAF50",
                               width=3, tags="menu")
        for side in [-1, 1]:
            b1 = c2 + side * (btn_w // 2 + 4)
            b2 = start_y + btn_h // 2
            self._draw_leaf_shape(b1, b2, 90 if side < 0 else -90, 14, "#388E3C", "#0B3D0B", tag="menu")
        canvas.create_text(c2, start_y + btn_h // 2, text="Start Game",
                          font=("Helvetica", 22, "bold"), fill="white", tags="menu")

        instr_y = start_y + 75
        self.instr_btn = (c2 - btn_w // 2, instr_y, c2 + btn_w // 2, instr_y + btn_h)
        canvas.create_rectangle(*self.instr_btn, fill="#0F3D0F", outline="#4CAF50",
                               width=3, tags="menu")
        for side in [-1, 1]:
            b1 = c2 + side * (btn_w // 2 + 4)
            b2 = instr_y + btn_h // 2
            self._draw_leaf_shape(b1, b2, 90 if side < 0 else -90, 14, "#2E7D32", "#0B3D0B", tag="menu")
        canvas.create_text(c2, instr_y + btn_h // 2, text="How to Play",
                          font=("Helvetica", 22, "bold"), fill="#A5D6A7", tags="menu")

        for _ in range(4):
            x = randint(30, c1 - 30)
            y = HEIGHT - randint(10, 30)
            for _ in range(5):
                o1 = randint(-20, 20)
                o2 = randint(-10, 6)
                s1 = randint(8, 16)
                canvas.create_oval(x + o1 - s1, y + o2 - s1, x + o1 + s1, y + o2 + s1,
                             fill="#1B5E20", outline="#0B3D0B", tags="menu")

    def _on_menu_click(self, event):
        if self._instr_shown:
            self._toggle_instructions()
            return
        x, y = event.x, event.y
        x1, y1, x2, y2 = self.start_btn
        if x1 <= x <= x2 and y1 <= y <= y2:
            self._start_game()
            return
        x1, y1, x2, y2 = self.instr_btn
        if x1 <= x <= x2 and y1 <= y <= y2:
            self._toggle_instructions()

    def _toggle_instructions(self):
        if self._instr_shown:
            canvas.delete("instructions_overlay")
            self._instr_shown = False
            return
        self._instr_shown = True
        c1 = WIDTH // 2
        c2 = WIDTH + 200

        canvas.create_rectangle(10, 10, c2 - 10, HEIGHT - 10,
                               fill="#0A1A08", outline="#2E7D32", width=4,
                               tags="instructions_overlay")

        for i in range(4):
            x = randint(30, c2 - 30)
            vine_len = randint(100, 180)
            l1 = []
            for j in range(12):
                t = j / 12
                sway = math.sin(t * math.pi * 4) * 12 * t
                l1.extend([x + sway, -5 + vine_len * t])
            canvas.create_line(*l1, fill="#1B5E20", width=2, smooth=True,
                              tags="instructions_overlay")
            l2, l3 = l1[-2], l1[-1]
            self._draw_leaf_shape(l2 + randint(-5, 5), l3 - 5,
                                 90 + randint(-20, 20), randint(8, 14),
                                 choice(["#2E7D32", "#388E3C"]), "#0B3D0B",
                                 tag="instructions_overlay")

        for i in range(3):
            b1 = 20 + i * 60
            y = 20 + i * 40
            self._draw_leaf_shape(b1, y, 135 + i * 20, 12,
                                 choice(["#1B5E20", "#2E7D32"]), "#0B3D0B",
                                 tag="instructions_overlay")
            self._draw_leaf_shape(c2 - b1, y, -45 - i * 20, 12,
                                 choice(["#1B5E20", "#2E7D32"]), "#0B3D0B",
                                 tag="instructions_overlay")

        lines = [
            "HOW TO PLAY",
            "",
            "Use ARROW KEYS to move your character.",
            "Click on grid EDGES to place vines (walls).",
            "Right-click a vine to DESTROY it.",
            "",
            "Reach the BOTTOM before the bot reaches the TOP.",
            "Block the bot's path with vines.",
            "",
            "Collect CHESTS for power-ups:",
            '  + = Extra vine         - = Erase all vines',
            '  = = Split the map      # = Generate a maze',
            "",
            "Click anywhere to close."
        ]
        text = "\n".join(lines)
        canvas.create_rectangle(60, 60, c2 - 60, HEIGHT - 60,
                               fill="#0D1F0A", outline="#1B5E20", width=2,
                               tags="instructions_overlay")
        canvas.create_text(c1, HEIGHT // 2 - 10, text=text,
                          font=("Helvetica", 15), fill="#CCE5CC",
                          justify="center", tags="instructions_overlay")

    def _start_game(self):
        canvas.delete("menu")
        canvas.delete("instructions_overlay")
        self.show_notation()
        self.draw_player(True, "C1", "C1", "down")
        self.draw_player(False, "D6", "D6", "down")
        self.draw_chests()
        self.rightside()
        self.bot()
        self.check_win()
        root.bind("<Key>", self.onplayerclick)
        canvas.bind("<Button-1>", self.on_mouse_click)
        canvas.bind("<Button-3>", self._destroy_wall)
        canvas.focus_set()


def RunGame():
    board = Board()
    board.draw_board()
    board.draw_jungle_ambient()
    board._draw_start_screen()
    board.animate_jungle()
    canvas.bind("<Button-1>", board._on_menu_click)
    root.mainloop()


RunGame()
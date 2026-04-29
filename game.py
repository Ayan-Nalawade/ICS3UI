import tkinter as tk
from random import randint as rand
from random import shuffle
from time import sleep

pick = ""
fi = input("Easy or Hard mode?: ")

def pick_word(fi):
    global pick
    while True:
    
        if fi.lower() == "easy":
            with open("Easy combinations.txt", "r") as x:
                data = x.readlines()
                pick = data[rand(0,len(data)-1)].strip()
                
            break
        elif fi.lower() == "hard":
            with open("Hard combinations.txt", "r") as x:
                data = x.readlines()
                pick = data[rand(0,len(data)-1)].strip()
                
            break
        else:
            print("Enter Easy or Hard!")
            continue
    
    print(f"Debug: {pick}")
pick_word(fi)

print("Terminal not required! Click on the coloured balls")
pick = list(pick)
# Pick a random word based on the user decision to play easy or hard mode
r = tk.Tk()
r.title("Mastermind")
WIDTH = 600
HEIGHT = 600
r.geometry(f"{WIDTH}x{HEIGHT}")
f = tk.Canvas(r, background="#8b8378")
f.pack(fill="both", expand=True) # Only after the user picks we want to create the screen

class Gameboard:
    def __init__(self):
        self.game_over = False
        self.confetti_array = []
        self.revealed_clues = []
        self.level_max = 10
        self.gamestate = {"level":0, "column":0, "col":"white", "guess":"", "guesseval":""} # For guesseval 0=null, 1=black, 2=yellow
        self.colors = ["blue", "green", "red", "purple", "orange", "yellow"]
    
    def draw_instructions(self):
        f.create_rectangle(20, 20, WIDTH-350, HEIGHT-20, fill="#3B3737")
        f.create_text(135, 50, text="Click on the colored ball \nto place into the row", fill="white")
    
    def trigger_explosion(self):
        self.game_over = True
        
        f.create_text(WIDTH//2, HEIGHT//2, text="BOOM!", fill="red", font=("Arial", 80, "bold"))
        
        self.explosion_items = []
        all_items = f.find_all()
        
        for item in all_items:

            vx = rand(-25, 25)
            vy = rand(-35, -10) 
            self.explosion_items.append({"id": item, "vx": vx, "vy": vy})
            
        self.animate_explosion()

    def animate_explosion(self):
        for p in self.explosion_items:

            f.move(p["id"], p["vx"], p["vy"])

            p["vy"] += 2 
            

        r.after(30, self.animate_explosion)
    
    def __buy_clue(self):
        if self.game_over:
            return
            

        if self.gamestate["level"] + 2 >= self.level_max:
            print("Not enough rows left to buy a clue!")
            return
            

        unrevealed = [i for i in range(4) if i not in self.revealed_clues]
        if not unrevealed: # All clues already revealed
            return
            

        clue_index = unrevealed[rand(0, len(unrevealed)-1)]
        self.revealed_clues.append(clue_index)
        

        e = pick[clue_index]
        color_map = {"r": "red", "o": "orange", "y": "yellow", "g": "green", "p": "purple", "b": "blue"}
        f.itemconfig(f"s{clue_index}", fill=color_map.get(e, "black"))
        

        self.gamestate["level"] += 2
        

        self.gamestate["column"] = 0
        self.gamestate["guess"] = ""
        self.gamestate["col"] = "white"
        
        self.__update()

        if len(self.revealed_clues) == 4:
            self.trigger_explosion()
            f.create_text(WIDTH//2, HEIGHT//2, text="Too many clues used! You LOST!", fill="gold", font=("Arial", 12, "bold"), tags="win_text")
            

    def __on_ball_click(self, event): # Private function to avoid accidental calls
        if self.game_over:
            return
        item = f.find_withtag("current") # Current just finds the tag name for whatever element the cursor was on DURING the click.

        if item: # If it doesn't exist, maybe the user used a machine to move the cusor faster than the command ran, then we want to do nothing 
            tag = f.gettags(item[0])
            if self.gamestate["column"] == 4:
                return 
            self.gamestate["col"] = tag[1]
            self.gamestate["guess"] = f"{self.gamestate['guess']}{tag[1][0]}" # Append first character of the letter
            self.__update()
            self.gamestate["column"] += 1

    def __check(self):
        if self.gamestate.get("column") != 4:
            return
            
        chars = {}
        usrguess = list(self.gamestate.get("guess"))
        for each in usrguess:
            if each in chars:
                chars[each] += 1
            else:
                chars[each] = 1
                
        print(f"DEBUG: {chars}")
        for b, e in enumerate(pick):
            if e in chars and chars.get(e) != 0:
                chars[e] -= 1
                if e == usrguess[b]:
                    self.gamestate["guesseval"] += "1"
                else:
                    self.gamestate["guesseval"] += "2"
            else:
                self.gamestate["guesseval"] += "0"

        eval_list = list(self.gamestate["guesseval"]) 
        shuffle(eval_list)                            
        self.gamestate["guesseval"] = "".join(eval_list)
        self.__update() 
        
        if self.gamestate["guesseval"] == "1111":
            self.game_over = True
            self.trigger_win()
            return
        
        self.gamestate["level"] += 1

        if self.gamestate.get("level") == self.level_max:
            for c, e in enumerate(pick):
                if e == "r":
                    f.itemconfig(f"s{c}", fill="red")
                elif e == "o":
                    f.itemconfig(f"s{c}", fill="orange")
                elif e == "y":
                    f.itemconfig(f"s{c}", fill="yellow")
                elif e == "g":
                    f.itemconfig(f"s{c}", fill="green")
                elif e == "p":
                    f.itemconfig(f"s{c}", fill="purple")
                elif e == "b":
                    f.itemconfig(f"s{c}", fill="blue")
                else:
                    f.itemconfig(f"s{c}", fill="black")
            return 

        self.gamestate["column"] = 0
        self.gamestate["guess"] = ""
        self.gamestate["guesseval"] = ""
        self.gamestate["col"] = "white"
        self.__update()
    

    def trigger_win(self):
        # Reveal solution first
        for c, e in enumerate(pick):
            if e == "r": f.itemconfig(f"s{c}", fill="red")
            elif e == "o": f.itemconfig(f"s{c}", fill="orange")
            elif e == "y": f.itemconfig(f"s{c}", fill="yellow")
            elif e == "g": f.itemconfig(f"s{c}", fill="green")
            elif e == "p": f.itemconfig(f"s{c}", fill="purple")
            elif e == "b": f.itemconfig(f"s{c}", fill="blue")
            else: f.itemconfig(f"s{c}", fill="black")

        f.create_text(WIDTH//2, HEIGHT//2, text="YOU WIN!", fill="gold", font=("Arial", 48, "bold"), tags="win_text")
        
        self.confetti_array = []
        confetti_colors = ["red", "blue", "green", "yellow", "purple", "orange", "white", "pink"]
        
        for _ in range(100):
            x = rand(50, WIDTH-50)
            y = rand(-200, 0) 
            speed_y = rand(3, 8) 
            color = confetti_colors[rand(0, len(confetti_colors)-1)]
            
            particle_id = f.create_oval(x, y, x+8, y+8, fill=color, outline="")
            self.confetti_array.append({"id": particle_id, "speed": speed_y})
            
        self.animate_confetti()

    def animate_confetti(self):
        if not self.game_over: 
            f.delete("win_text")
            for p in self.confetti_array:
                f.delete(p["id"])
            return

        for particle in self.confetti_array:
            f.move(particle["id"], 0, particle["speed"])
            
            coords = f.coords(particle["id"])
            if coords and coords[1] > HEIGHT:
                f.move(particle["id"], 0, -HEIGHT - 50)
                
        r.after(30, self.animate_confetti)

    def __delete(self):
        if self.gamestate["column"] == 0 or self.game_over:
            return
        self.gamestate["column"] -= 1
        self.gamestate["col"] = "white"
        self.gamestate["guess"] = self.gamestate["guess"][:-1] # Get rid of the most recent guess
        self.__update()

    def __new_game(self):
        self.game_over = False
        self.revealed_clues = []

        f.delete("loss_text") 
        f.delete("win_text") 
        for i in range(0,self.level_max):
            for x in range(0,4):
                self.gamestate = {"level":i, "column":x, "col":"white", "guess":"", "guesseval":"0000"}
                self.__update()

        for col in range(4):
            f.itemconfig(f"s{col}", fill="#FFFEFE")
        self.gamestate["level"] = 0
        self.gamestate["column"] = 0
        self.gamestate["guesseval"] = ""
        pick_word(fi)
        self.__update()
        

    
    def __update(self):
        # Update Triangle and reset other triangles to grey
        for i in range(0,10):
            if self.gamestate.get("level") == i:
                f.itemconfig(f"p{i}", fill="blue")
            else:
                f.itemconfig(f"p{i}", fill="#555555")

        # Update the ball colour
        current_level = self.gamestate.get("level")
        current_col = self.gamestate.get("column")
        f.itemconfig(f"bh_{current_level}_{current_col}", fill=self.gamestate.get("col"))

        # Update the guesseval
        for x, g in enumerate(self.gamestate.get("guesseval")):
            if g == "0":
                f.itemconfig(f"h_{current_level}_{x}", fill="white")
            elif g == "1":
                f.itemconfig(f"h_{current_level}_{x}", fill="black")
            else:
                f.itemconfig(f"h_{current_level}_{x}", fill="yellow")

    
    def draw_gameboard(self):
        # Background panel for the gameboard
        board_x1, board_y1 = WIDTH - 330, 20
        board_x2, board_y2 = WIDTH - 20, HEIGHT - 20
        f.create_rectangle(board_x1, board_y1, board_x2, board_y2, fill="#3B3737", outline="black", width=2)

        # Title Text
        f.create_text(425, 45, text="MasterMind", fill="white", font=("Arial", 24, "bold"))

        # Dimensions for the grid
        start_y = 70
        row_height = 43
        wood_color = "#A66B38"
        hole_color = "#FFFEFE"

        for row in range(self.level_max):
            y = start_y + (row * row_height)
            center_y = y + (row_height / 2)

            # Draw the Triangle Pointer (Left side)
            f.create_polygon(285, center_y - 12, 285, center_y + 12, 310, center_y, 
                                fill="#555555", outline="black", width=2, tags=f"p{row}")

            # Draw the Brown Wooden Background for guesseval 
            f.create_rectangle(320, y, 480, y + row_height, fill=wood_color, outline="black")
            
            # Vertical separator lines for the guesseval slots
            for col in range(1, 4):
                line_x = 320 + (col * 40)
                f.create_line(line_x, y, line_x, y + row_height, fill="black")

            # Draw the 4 guesseval ball Holes
            for col in range(4):
                hole_x = 340 + (col * 40)
                # Outer shadow/highlight ring and inner black hole
                f.create_oval(hole_x - 10, center_y - 10, hole_x + 10, center_y + 10, fill=hole_color, outline="#777777", width=2, tags=(f"bh_{row}_{col}"))

            # Draw the Brown Background
            f.create_rectangle(490, y, 550, y + row_height, fill=wood_color, outline="black")

            # Draw the 4 little Feedback Holes (2x2 grid)
            f.create_oval(505 - 4, center_y - 10 - 4, 505 + 4, center_y - 10 + 4, fill=hole_color, outline="black", width=1, tags=f"h_{row}_0") # Top-left
            f.create_oval(535 - 4, center_y - 10 - 4, 535 + 4, center_y - 10 + 4, fill=hole_color, outline="black", width=1, tags=f"h_{row}_1") # Top-right
            f.create_oval(505 - 4, center_y + 10 - 4, 505 + 4, center_y + 10 + 4, fill=hole_color, outline="black", width=1, tags=f"h_{row}_2") # Bottom-left
            f.create_oval(535 - 4, center_y + 10 - 4, 535 + 4, center_y + 10 + 4, fill=hole_color, outline="black", width=1, tags=f"h_{row}_3") # Bottom-right

        # Draw the Solution Area at the bottom
        solution_y = start_y + (10 * row_height)
        
        # "Solution" Text
        f.create_text(425, solution_y + 15, text="Solution", fill="white", font=("Arial", 16, "bold"))
        
        # Solution wooden panel
        sol_panel_y = solution_y + 30
        f.create_rectangle(340, sol_panel_y, 500, sol_panel_y + 35, fill=wood_color, outline="black")
        
        # Solution vertical lines
        for col in range(1, 4):
            line_x = 340 + (col * 40)
            f.create_line(line_x, sol_panel_y, line_x, sol_panel_y + 35, fill="black")

        # Solution holes
        for col in range(4):
            hole_x = 360 + (col * 40)
            center_y = sol_panel_y + 17.5
            f.create_oval(hole_x - 10, center_y - 10, hole_x + 10, center_y + 10, fill=hole_color, outline="#777777", width=2, tags=f"s{col}")
        self.__update()
    
    def draw_balls(self):
        start_x = 35 # x coordinate
        y = 100 # y coordinate
        dimeter = 25 # Diameter of the ball
        spce = 35 # Space between each balls

        for i in range(0,len(self.colors)):
            x = start_x + (i*spce)
            f.create_oval(x, y, x+dimeter, y+dimeter,
                          fill=self.colors[i],
                          outline="#4a4a4a",
                          width=2,
                          tags=("ball",self.colors[i])) # Assign tag ball and the color. Ball isn't required here since its a easy animation but added it as practice
        f.create_oval(x+5, y+5, x+12, y+12, fill="white", outline="", tags=("ball", self.colors[i])) # Add 3D 
        f.tag_bind("ball", "<Button-1>", self.__on_ball_click)
    
    def draw_buttons(self):
        check_btn = tk.Button(r, text="Check", font=("Arial", 12), command=self.__check)
        f.create_window(80,160, window=check_btn)

        delete_btn = tk.Button(r, text="Delete", font=("Arial", 12), command=self.__delete)
        f.create_window(180, 160, window=delete_btn)

        new_game_btn = tk.Button(r, text="New Game", font=("Arial", 12), command=self.__new_game)
        f.create_window(125, 210, window=new_game_btn)

        clue_btn = tk.Button(r, text="Buy Clue (-2 rows)", font=("Arial", 12), command=self.__buy_clue)
        f.create_window(125, 260, window=clue_btn)

game = Gameboard()
game.draw_instructions()
game.draw_balls()
game.draw_buttons()
game.draw_gameboard()

f.mainloop()

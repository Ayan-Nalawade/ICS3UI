import tkinter as tk
from random import randint as rand

pick:str = ""

while True:
    fi = input("Easy or Hard mode?: ")
    if fi.lower() == "easy":
        with open("Easy combinations.txt", "r") as x:
            data = x.readlines()
            pick = data[rand(0,len(data)-1)]
            
        break
    elif fi.lower() == "hard":
        with open("Hard combinations.txt", "r") as x:
            data = x.readlines()
            pick = data[rand(0,len(data)-1)]
            
        break
    else:
        print("Enter Easy or Hard!")
        continue
    
print(f"Debug: {pick}")
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
        self.gamestate = {"level":0, "column":0, "col":"white", "guess":"0000"} # For guess 0=null, 1=black, 2=yellow
        self.colors = ["blue", "green", "red", "purple", "orange"]
    
    def draw_instructions(self):
        f.create_rectangle(20, 20, WIDTH-350, HEIGHT-20, fill="#3B3737")
        f.create_text(135, 50, text="Click on the colored ball \nto place into the row", fill="white")

    def __on_ball_click(self, event): # Private function to avoid accidental calls
        item = f.find_withtag("current") # Current just finds the tag name for whatever element the cursor was on DURING the click.

        if item: # If it doesn't exist, maybe the user used a machine to move the cusor faster than the command ran, then we want to do nothing 
            tag = f.gettags(item[0])
            if self.gamestate["column"] == 4:
                return 
            self.gamestate["col"] = tag[1]
            self.__update()
            self.gamestate["column"] += 1
            print(tag)
            print(f"I clicked {tag[1]} ball!!!")

    def __check(self):
        pass

    def __delete(self):
        pass

    def __new_game(self):
        pass
    
    def __update(self):
        # Update Triangle and reset other triangles to grey
        for i in range(0,10):
            if self.gamestate.get("level") == i:
                f.itemconfig(f"p{i}", fill="blue")
            else:
                f.itemconfig(f"p{i}", fill="#555555")

        # Update the ball colour
        f.itemconfig(f"bh{self.gamestate.get("column")}", fill=self.gamestate.get("col"))

        # Update the guess
        for x, g in enumerate(self.gamestate.get("guess")):
            if g == "0":
                f.itemconfig(f"h{x}", fill="white")
            elif g == "1":
                f.itemconfig(f"h{x}", fill="black")
            else:
                f.itemconfig(f"h{x}", fill="yellow")

    
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

        # Draw the 10 guess rows
        for row in range(10):
            y = start_y + (row * row_height)
            center_y = y + (row_height / 2)

            # Draw the Triangle Pointer (Left side)
            f.create_polygon(285, center_y - 12, 285, center_y + 12, 310, center_y, 
                                fill="#555555", outline="black", width=2, tags=f"p{row}")

            # Draw the Brown Wooden Background for Guess 
            f.create_rectangle(320, y, 480, y + row_height, fill=wood_color, outline="black")
            
            # Vertical separator lines for the guess slots
            for col in range(1, 4):
                line_x = 320 + (col * 40)
                f.create_line(line_x, y, line_x, y + row_height, fill="black")

            # Draw the 4 Guess ball Holes
            for col in range(4):
                hole_x = 340 + (col * 40)
                # Outer shadow/highlight ring and inner black hole
                f.create_oval(hole_x - 10, center_y - 10, hole_x + 10, center_y + 10, fill=hole_color, outline="#777777", width=2, tags=(f"bh{col}"))

            # Draw the Brown Background
            f.create_rectangle(490, y, 550, y + row_height, fill=wood_color, outline="black")

            # Draw the 4 little Feedback Holes (2x2 grid)
            f.create_oval(505 - 4, center_y - 10 - 4, 505 + 4, center_y - 10 + 4, fill=hole_color, outline="black", width=1, tags="h0") # Top-left
            f.create_oval(535 - 4, center_y - 10 - 4, 535 + 4, center_y - 10 + 4, fill=hole_color, outline="black", width=1, tags="h1") # Top-right
            f.create_oval(505 - 4, center_y + 10 - 4, 505 + 4, center_y + 10 + 4, fill=hole_color, outline="black", width=1, tags="h2") # Bottom-left
            f.create_oval(535 - 4, center_y + 10 - 4, 535 + 4, center_y + 10 + 4, fill=hole_color, outline="black", width=1, tags="h3") # Bottom-right

        # Draw the Solution Area at the bottom
        solution_y = start_y + (10 * row_height)
        
        # "Solution" Text
        f.create_text(425, solution_y + 15, text="Solution", fill="white", font=("Arial", 16, "bold"))
        
        # Solution wooden panel
        sol_panel_y = solution_y + 30
        f.create_rectangle(320, sol_panel_y, 480, sol_panel_y + 35, fill=wood_color, outline="black")
        
        # Solution vertical lines
        for col in range(1, 4):
            line_x = 320 + (col * 40)
            f.create_line(line_x, sol_panel_y, line_x, sol_panel_y + 35, fill="black")

        # Solution holes
        for col in range(4):
            hole_x = 340 + (col * 40)
            center_y = sol_panel_y + 17.5
            f.create_oval(hole_x - 10, center_y - 10, hole_x + 10, center_y + 10, fill=hole_color, outline="#777777", width=2)
        self.__update()
    
    def draw_balls(self):
        start_x = 50 # x coordinate
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

    
    




game = Gameboard()
game.draw_instructions()
game.draw_balls()
game.draw_buttons()
game.draw_gameboard()

f.mainloop()
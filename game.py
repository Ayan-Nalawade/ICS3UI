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
WIDTH = 600
HEIGHT = 600
r.geometry(f"{WIDTH}x{HEIGHT}")
f = tk.Canvas(r, background="#8b8378")
f.pack(fill="both", expand=True) # Only after the user picks we want to create the screen

class Gameboard:
    def __init__(self):
        self.gamestate = []
        self.colors = ["b", "g", "o", "p", "r", "g"]
    
    def draw_instructions(self):
        f.create_rectangle(20, 20, WIDTH-350, HEIGHT-20, fill="#3B3737")
        f.create_text(130, 40, text="Click on the colored peg \nTo place into the row", fill="white")
    
    def draw_balls(self):
        start_x = 35 # x coordinate
        y = 100 # y coordinate
        dimeter = 25 # Diameter of the ball
        spce = 35 # Space between each balls

        for i in range(0,len(self.colors)):
            x = start_x + (i*spce)
            f.create_oval(x, y, x+dimeter, y+dimeter,
                          fill=self.colors[i],
                          outlint="#4a4a4a",
                          width=2,
                          tags=("ball",self.colors[i])) # Assign tag ball and the color. Ball isn't required here since its a easy animation but added it as practice
        



game = Gameboard()
game.draw_instructions()

f.mainloop()
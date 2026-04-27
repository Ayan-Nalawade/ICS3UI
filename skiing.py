import tkinter as tk
from random import randint as rand
from random import uniform as uni
from time import sleep
from math import sqrt, sin, cos

r = tk.Tk()
# WIDTH = r.winfo_screenwidth() # x
# HEIGHT = r.winfo_screenheight() # y
WIDTH = 600
HEIGHT=600
r.geometry(f'{WIDTH}x{HEIGHT}')
f = tk.Canvas(r, width=WIDTH, height=HEIGHT, background="#87CEEB")
f.pack()


def draw_scenery():
    f.create_oval(WIDTH - 150, -50, WIDTH + 50, 150, fill="#FFD700", outline="") # Sun
    
    # Mountains (better)
    f.create_polygon(0, HEIGHT//2, WIDTH//4, HEIGHT//4, WIDTH//2, HEIGHT//2, fill="#7A8B99", outline="")
    f.create_polygon(WIDTH//3, HEIGHT//2, WIDTH*0.7, HEIGHT//5, WIDTH, HEIGHT//2, fill="#8B9CA8", outline="")
    f.create_polygon(WIDTH*0.6, HEIGHT//2, WIDTH*0.85, HEIGHT//3.5, WIDTH+100, HEIGHT//2, fill="#6C7A86", outline="")
    
    #Draw Snow Caps for mountains
    f.create_polygon(WIDTH//4, HEIGHT//4, WIDTH//3.2, HEIGHT//3, WIDTH//5.5, HEIGHT//3, fill="white", outline="")
    f.create_polygon(WIDTH*0.7, HEIGHT//5, WIDTH*0.75, HEIGHT//3.2, WIDTH*0.62, HEIGHT//3.2, fill="white", outline="")
    
    # Draw the main Snowy Hill
    f.create_polygon(-10, HEIGHT//2.5, WIDTH+10, HEIGHT//1.5, WIDTH+10, HEIGHT+10, -10, HEIGHT+10, fill="#F0F8FF", outline="")


def draw_clouds():
    size = 10
    f.create_oval(50,50,130,90, fill="white", outline="")
    f.create_oval(80,30,160,80, fill="white", outline="")
    f.create_oval(100,50, 190,90, fill="white", outline="")
    # Cloud 1 on the left
    
    f.create_oval(WIDTH-350,60,WIDTH-250, 100, fill="white", outline="")
    f.create_oval(WIDTH-300, 40, WIDTH-200, 90, fill="white", outline="")
    f.create_oval(WIDTH-260, 60, WIDTH-160, 100, fill="white", outline="")
    # Draw the cloud on the left
    
def draw_pine_tree(x, y):
    f.create_rectangle(x-3, y, x+3, y+15, fill="#5C4033", outline="", tags="tree") #Trunk
    f.create_polygon(x, y-20, x-15, y+5, x+15, y+5, fill="#2E8B57", outline="", tags="tree") # Create pine 1
    f.create_polygon(x, y-30, x-12, y-5, x+12, y-5, fill="#2E8B57", outline="", tags="tree") # Create pine 2
    f.create_polygon(x, y-40, x-10, y-15, x+10, y-15, fill="#2E8B57", outline="", tags="tree") # Create pine 3

def place_trees():
    for _ in range(20):
        xt = rand(50,WIDTH-50)
        
        hty = (HEIGHT//2.5) + (xt/WIDTH) * ((HEIGHT//1.5) - (HEIGHT//2.5))
        
        yt = rand(int(hty) + 20, HEIGHT-50)
        draw_pine_tree(xt, yt)
        

draw_scenery()
draw_clouds()
place_trees()
    
class Skier:
    def __init__(self, canvas):
        self.can = canvas
        self.trail_ids = []
        self.reset_vars()
        
        colors = ["red", "blue", "green", "orange", "black", "yellow"]
        color = colors[rand(0, len(colors)-1)] # -1 because index 0 (starts at 0)
        self.ski_l = self.can.create_line(0,0,0,0, fill="#222222", width="3", tags="skier")
        self.ski_r = self.can.create_line(0,0,0,0, fill="#222222", width="3", tags="skier")
        self.pole_l = self.can.create_line(0,0,0,0, fill="#555555", width="1", tags="skier")
        self.pole_r = self.can.create_line(0,0,0,0, fill="#555555", width="1", tags="skier")
        self.body = self.can.create_oval(0,0,0,0, fill=color, outline="black", tags="skier")
        self.head = self.can.create_oval(0,0,0,0, fill=color, outline="black", tags="skier")
        
        
        self.update_coords()
        
    def reset_vars(self):
        for t_id in self.trail_ids:
            self.can.delete(t_id)
        self.trail_ids.clear()
        
        self.t = rand(0,100)
        
        self.xs = uni(-100, -20)
        self.ys = uni(HEIGHT//2.5+20, HEIGHT-100)
        
        self.A = uni(30,80)
        self.B = uni(0.02, 0.06)
        
        self.xspeed = uni(2,5)
        self.ySpeed = uni(0.5, 2)
        
        self.prev_x = None
        self.prev_y = None
        
        
    def update_coords(self):
        x = self.xs + self.xspeed * self.t
        y = self.ys + self.ySpeed * self.t + self.A * sin(self.B * self.t)
        
        y2 = self.A * self.B * cos(self.B * self.t) # Since its a tilt, calculate the vertical tilt on the skies
        tilt = y2 * 1.5
        
        self.can.coords(self.ski_l, x-10, y-tilt, x+10, y+tilt)
        self.can.coords(self.ski_r, x-10, y+8-tilt, x+10, y+8+tilt)
        # Update skies
        
        self.can.coords(self.pole_l, x-5, y-5, x+5, y-5)
        self.can.coords(self.pole_r, x-5,y+15, x+5, y+15)
        # UPdate the poles
        
        self.can.coords(self.body, x-5, y-2, x+5, y+10)
        self.can.coords(self.head, x+1, y-5, x+9, y+3)
        # Update body and head
        
        if self.prev_x is not None and self.prev_y is not None:
            trail_l = self.can.create_line(self.prev_x-10, self.prev_y, x-10, y, fill="#D3E0EA", width="2") # Left
            trail_r = self.can.create_line(self.prev_x-10, self.prev_y+8, x-10, y+8, fill="#D3E0EA", width="2") # Right
            self.trail_ids.extend([trail_l, trail_r]) # New command I learned: Basically, if I want to add [4,2] to a list, append will do: [3,2,3,[4,2]]. Extend will fix and do [3,2,3,4,2]

        self.prev_x = x
        self.prev_y = y

    def move(self):
        self.t += 1
        self.update_coords()
        
        self.can.tag_raise("skier")
        self.can.tag_raise("tree") # New command I learned: Basically this raises the element with tags `tree` for example to the foreground

        x = self.xs + self.xspeed*self.t
        y = self.ys + self.ySpeed*self.t
        if x > WIDTH+50 or y > HEIGHT+50:
            self.reset_vars() # If skier going off

skiers:list = []        
for _ in range(0,100): 
    skiers.append(Skier(f))
        
def animate():
    for skier in skiers:
        skier.move()
    r.after(30, animate)

animate()

    
    

    





r.mainloop()
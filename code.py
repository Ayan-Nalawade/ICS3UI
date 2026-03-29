# UPDATE CODE FROM INITAL WITH COMMENTS AND BETTER READABILITY

from tkinter import *
import time
import math 

r = Tk()
r.title("Mario Yeehaw")

height = 600
width = 800
s = Canvas(r, width=width, height=height, bg="#5C94FC")
s.pack()

class creation:
    def __init__(self):
        self.SKY = "#5C94FC"
        self.BRICK = "#C84C0C"
        self.BRICK_DARK = "#8B2E0D"
        self.GROUND = "#C84C0C"
        self.GROUND_DARK = "#8B2E0D"
        self.PIPE = "#1E9C2A"
        self.PIPE_DARK = "#0F6B1C"
        self.HILL = "#4AAE2A"
        self.HILL_DARK = "#2E7D1A"
        self.CLOUD = "#FFFFFF"
        self.CLOUD_SHADOW = "#CDE8FF"
        self.QUESTION = "#F7A000"
        self.QUESTION_DARK = "#B26B00"
        self.MARIO_RED = "#E43B2C"
        self.MARIO_BROWN = "#8B4513"
        self.MARIO_SKIN = "#FFD2A6"
        self.GOOMBA = "#B5652A"
        self.GOOMBA_DARK = "#7A3B12"
        self.HUD = "#FFFFFF"
        self.COIN = "#F7D000"

    def clouds(self, x, y, scale = 1.0) -> None:
        w = 70 * scale
        h = 30 * scale 
        s.create_oval(x, y, x+w, y + h, fill=self.CLOUD, outline=self.CLOUD)
        s.create_oval(x + 25 * scale, y-10 * scale, x+85 * scale, y + 25 * scale, fill=self.CLOUD, outline=self.CLOUD) # Add the illusion that theres two clouds 
        s.create_oval(x + 10 * scale, y + 10 * scale, x + 60 * scale, y + 40 * scale, fill=self.CLOUD_SHADOW, outline=self.CLOUD_SHADOW) # Add a light blue oval slightly under the cloud to make it look like a real detailed cloud
    
    def draw_hill(self, x,y,w,h):
        s.create_oval(x, y-h, x+w, y+h, fill=self.HILL, outline=self.HILL) # Draw hill region anchored to the height and width of the screen
    
    def draw_ground(self):
        bw = 50 # Brick width
        bh = 40 # Brick height

        y0 = height-80
        rows = 2
        for r in range(rows):
            y = y0 + r * bh # update brick values 
            for c in range(width//bw + 2):
                x = c*bw # update brick values so their drawn side by side
                s.create_rectangle(x, y, x+bw, y + bh, fill=self.GROUND, outline=self.GROUND_DARK, width=2)
                s.create_line(x + bw /2, y, x+bw/2, y+bh, fill=self.GROUND_DARK, width=2) # Split boxes more; draws a line through the rectangles to split them more. Kind of like a circle being split up
    
    def draw_brick(self, x,y,size=40):
        s.create_rectangle(x, y, x+size, y+size, fill=self.BRICK, outline=self.BRICK_DARK, width=2)
        s.create_rectangle(x, y+size/2, x+size, y+size/2, fill=self.BRICK, outline=self.BRICK_DARK, width=2) # "Split" to get the classical mario blocks
        s.create_rectangle(x+size/2, y, x+size/2, y+size/2, fill=self.BRICK_DARK, width=2) # Draw a new brick underneath  <small brick><small brick> \n <brick>
        s.create_rectangle(x + size/2, y+size/2, x+size, y+size/2, fill=self.BRICK_DARK, width=2) # Draw another rectangle 


        
    

class_call = creation()
class_call.draw_brick(360-40, height-220)
# class_call.draw_ground()
# class_call.clouds(90,80, 1.1)

# class_call.draw_hill(40, height-120, 160,120)



s.mainloop()
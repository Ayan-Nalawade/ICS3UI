# UPDATE CODE FROM INITAL WITH COMMENTS AND BETTER READABILITY

from tkinter import *
import time
import math 

r = Tk()
r.title("Mario Yeehaw")

height = 600
s = Canvas(r, width=800, height=height, bg="#5C94FC")
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
        s.create_oval(x, y-h, x+w, y+h, fill=self.HILL, outline=self.HILL)
        
    

class_call = creation()
class_call.clouds(90,80, 1.1)

class_call.draw_hill(40, height-120, 160,120)



s.mainloop()
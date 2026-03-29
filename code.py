from tkinter import *
import time
import math 

r = Tk()
r.title("Mario Yeehaw")

s = Canvas(r, width=800, height=600, bg="#5C94FC")
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
    
    def setupHUD(self) -> None:
        s.create_text(60, 30, text="MARIO", fill=self.HUD, font=("Helvetica", 16, "bold"))
        
    

class_call = creation()



s.mainloop()
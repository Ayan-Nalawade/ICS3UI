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
        self.brick_y = height-220 # Y coords anchored to screen size
        self.brick_x = 360 # X coords anchored to screen size
        self.pipe_x = 140 # X coords for the pipe
        self.pipe_y = height-80 # Y coords for the pipe anchored to the screen size
        self.mario_x = self.pipe_x + 20 # X coords for mario anchored to the pipe
        self.mario_y = self.pipe_y - 120 - 28 # Y coords for mario anchored to the pipe

    def draw_clouds(self, x, y, scale = 1.0) -> None:
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
        s.create_rectangle(x + size/2, y+size/2, x+size, y+size/2, fill=self.BRICK_DARK, width=2) # Draw another rectangle <small brick><hightlight><smallbrick><highlight underneath> \n <brick>\
    
    def draw_question_block(self, x,y,size=40):
        s.create_rectangle(x, y, x+size, y+size, fill=self.QUESTION, outline=self.QUESTION_DARK, width=2) # Draw the coin box
        s.create_text(x+size/2, y+size/2, text="?", font=("Helvetica", 20, "bold"), fill="#3B2A00") # Draw the ? inside of the block
    
    def draw_pipe(self, x,y,height=120):
        s.create_rectangle(x, y-height, x+60,y, fill=self.PIPE, outline=self.PIPE_DARK, width=2) # Draw rectangle
        s.create_rectangle(x-10, y-height, x+70, y-height+20, fill=self.PIPE, outline=self.PIPE_DARK, width=2) # Draw a small rectangle on top to make it look like a pipe
        s.create_line(x+30, y-height, x+30, y, fill=self.PIPE_DARK, width=2) # Split shape from centre to make it look like a pipe (add highlights)
    
    def draw_mario(self, x,y,scale=2):
        pixels = [
            "....RRRRRR....",
            "...RRRRRRRR...",
            "...RRR..RRR...",
            "..SSSSSSSSS...",
            "..SSS..SSS....",
            "..SSSSSSSS....",
            "...BBBBBBB....",
            "..RBBBBBBR....",
            ".RRRBBBBRRR...",
            ".RRBBBBBBRR...",
            "..BBBBBBBB....",
            "..BB..BB......",
            ".BBB..BBB.....",
            ".BB....BB.....",
        ] # This will mapp the mario sprite
        color_map = {
            "R": self.MARIO_RED,
            "B": self.MARIO_BROWN,
            "S": self.MARIO_SKIN,
            ".": None,
        }  # Define what colour to be used 

        ixr = []
        for r,l in enumerate(pixels): # Map over each pixel/character
            for col, ch in enumerate(l): 
                color = color_map.get(ch) # Map each pixel/character to a colour
                if color: # For valid colours
                    x0 = x+col*scale # Define coords
                    y0 = y+r*scale 
                    ixr.append(s.create_rectangle(x0,y0,x0+scale, y0+scale, fill=color, outline=color)) # Append the colours into a list for use
        return ixr
    
    def draw_goomba(self, x,y):
        ixr = []
        ixr.append(s.create_oval(x, y-18, x+30, y+8, fill=self.GOOMBA, outline=self.GOOMBA_DARK, width=2)) # Draw circle to draw outline for goomba
        ixr.append(s.create_oval(x+6, y-8, x+12, y-2, fill="white", outline="white")) # Left eye
        ixr.append(s.create_oval(x+18, y-8, x+24, y-2, fill="white", outline="white")) # Right eye
        ixr.append(s.create_oval(x+8, y-6, x+10, y-4, fill="black", outline="black")) # Left eyeball
        ixr.append(s.create_oval(x+20,y-6,x+22,y-4, fill="black", outline="black")) # Right eyeball
        return ixr
    
    def draw_screen(self):
        self.draw_clouds(90,80,1.1)
        self.draw_clouds(520, 90, 1.4)

        hb = height - 120 # Hill base
        self.draw_hill(10, hb, 160, 120)
        self.draw_hill(520, hb + 10, 120, 90)

        self.draw_ground()



        self.draw_pipe(self.pipe_x, self.pipe_y, 120)

        # Place mario on TOP of the pipe
        mario_ixr = self.draw_mario(self.mario_x, self.mario_y, 2)

        # Brick row + question block for mario to jump
        self.draw_brick(self.brick_x-40, self.brick_y)
        self.draw_question_block(self.brick_x, self.brick_y)
        self.draw_brick(self.brick_x+40, self.brick_y)
        self.draw_brick(self.brick_x+80, self.brick_y)

        # Goombas !
        goomba1 = self.draw_goomba(560, height-95)
        goomba2 = self.draw_goomba(610, height-95)

        return mario_ixr, goomba1, goomba2
    
    def __move_items(self, ixr, x, y): # Private function so I don't accidently use it
        for i in ixr:
            s.move(i, x, y) # Move to the new x and y coords
    
    def __set_mario_pos(x, y):
        global speech_id

    
    def draw_animation(self, m, g1, g2): # IXR values for mario (m) , goomba1 (g1) , goomba2 (g2)
        # Animation constants
        MARIO_W:int = 32
        MARIO_H:int = 28
        GOOMBA_W:int = 30
        GOOMBA_TOP_OFFSET:int = -18
        GOOMBA_BOB_AMPLITUDE:int = 9
        GOOMBA_BOB_SPEED:float = 6.0

        mario_state = {
            "x":float(self.mario_x),
            "y":float(self.mario_y),
            "jump":None,
            "run":None
        } # Define mario's physics, including location

        goombas = [
            {
                "x": 560.0,
                "base_y": float(height - 95),
                "offset": 0.0,
                "phase": 0.0,
                "alive": True,
                "ids": g1,
            },
            {
                "x": 610.0,
                "base_y": float(height - 95),
                "offset": 0.0,
                "phase": math.pi,
                "alive": True,
                "ids": g2,
            },
        ] # Define the goomba physics including location

        eld:float = 0.0 # Elapsed time 
        last_tick = time.perf_counter()
        speech_id = None
        bomb_ixr = []
        bf_t:float = 0.0 #Bomb fuse time
        bf_td:float = 2.4 # Bomb fuse duration
        sm = "main" # Sequence

        gty = height-80 # Define the y coords for the ground TOP
        gmy = gty-MARIO_H # Setup mario ground coordinates







class_call = creation()
q,e,r = class_call.draw_screen()
class_call.draw_animation(q,e,r)
# class_call.draw_goomba(520,300)
# class_call.draw_pipe(520,520)
# class_call.draw_question_block(20,20)
# class_call.draw_brick(360-40, height-220)
# class_call.draw_ground()
# class_call.clouds(90,80, 1.1)

# class_call.draw_hill(40, height-120, 160,120)



s.mainloop()
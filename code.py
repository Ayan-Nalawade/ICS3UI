# UPDATE CODE FROM INITIAL WITH COMMENTS AND BETTER READABILITY 
# AND IT WAS FREEZING FOR SOME REASON

from tkinter import * 
import math  
import time

r = Tk()  
r.title("Mario Yeehaw")  # Set the title shown in the window bar.

height = 600  
width = 800  
s = Canvas(r, width=width, height=height, bg="#5C94FC", highlightthickness=0)  # Create the drawing canvas.
s.pack()  # Attach the canvas to the Tk window layout.

# Shared animation state
mario_state = {}  # Store mario position and current movement state.
goombas = []  # Store per-goomba animation and sprite data.
eld = 0.0  
lt = 0.0  # Last frame timestamp used to compute delta-time (time difference).
speech_id = None  # Canvas item id for mario speech text (Yeehaw~ uh...Mario!).
bomb_ixr = []  # Canvas item ids for bomb body/fuse/spark.
bft = 0.0  # Bomb fuse timer progress.
sm = "main"  # Sequence mode controlling animation phase.


class creation:  
    def __init__(self):
        # Define HEX values for colour codes to add more colour options
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

        self.brick_y = height - 220  # Brick row Y anchored to screen size.
        self.brick_x = 360  # Question/brick row X anchored to screen size.
        self.pipe_x = 140  # Pipe X anchor.
        self.pipe_y = height - 80  # Pipe bottom Y anchored to screen size (ground top).
        self.mario_x = self.pipe_x + 8  # Mario starting X on top of pipe.
        self.mario_y = self.pipe_y - 120 - 28  # Mario starting Y on top of pipe.

        # Animation constants
        self.MARIO_W = 32  # Mario sprite width in pixels.
        self.MARIO_H = 28  # Mario sprite height in pixels.
        self.GOOMBA_W = 30  # Goomba sprite width 
        self.GOOMBA_TOP_OFFSET = -18  # Offset to goomba top.
        self.GOOMBA_BOB_AMPLITUDE = 9  # Vertical bobbing amplitude.
        self.GOOMBA_BOB_SPEED = 6.0  # Vertical bobbing angular speed.
        self.bf_td = 2.4  # Bomb fuse total duration.
        # Values are dereived from trial and error. 

        self.gty = height - 80  # Ground top Y value.
        self.gmy = self.gty - self.MARIO_H  # Mario Y when standing on ground.

        self.mario_ixr = []  # Canvas ids for mario sprite pixels. These allow easy modification (saved as pointers)

    def draw_clouds(self, x, y, scale=1.0) -> None:  
        w = 70 * scale  # Base cloud width adjusted by scale.
        h = 30 * scale  # Base cloud height adjusted by scale.
        s.create_oval(x, y, x + w, y + h, fill=self.CLOUD, outline=self.CLOUD)  # Left cloud puff.
        s.create_oval(  # Right cloud puff.
            x + 25 * scale,
            y - 10 * scale,
            x + 85 * scale,
            y + 25 * scale,
            fill=self.CLOUD,
            outline=self.CLOUD,
        )
        s.create_oval(  # Lower shadow puff for depth and make it realistic.
            x + 10 * scale,
            y + 10 * scale,
            x + 60 * scale,
            y + 40 * scale,
            fill=self.CLOUD_SHADOW,
            outline=self.CLOUD_SHADOW,
        )

    def draw_hill(self, x, y, w, h):  
        s.create_oval(x, y - h, x + w, y + h, fill=self.HILL, outline=self.HILL)  # Hill body.

    def draw_ground(self):
        bw = 50  # Single ground brick width.
        bh = 40  # Single ground brick height.
        y0 = height - 80  # Top Y where ground starts.

        for row in range(2):  # Draw two stacked rows of ground.
            y = y0 + row * bh  # Compute row Y.
            for col in range(width // bw + 2):  # Draw enough columns to cover screen.
                x = col * bw  # Compute column X.
                s.create_rectangle(x, y, x + bw, y + bh, fill=self.GROUND, outline=self.GROUND_DARK, width=2)  # Draw brick.
                s.create_line(x + bw / 2, y, x + bw / 2, y + bh, fill=self.GROUND_DARK, width=2)  # Draw vertical split.

    def draw_brick(self, x, y, size=40):  # Draw mario-style brick block.
        s.create_rectangle(x, y, x + size, y + size, fill=self.BRICK, outline=self.BRICK_DARK, width=2)  # Brick border.
        s.create_line(x, y + size / 2, x + size, y + size / 2, fill=self.BRICK_DARK, width=2)  # Horizontal split.
        s.create_line(x + size / 2, y, x + size / 2, y + size / 2, fill=self.BRICK_DARK, width=2)  # Upper-right split.
        s.create_line(x + size / 2, y + size / 2, x + size, y + size / 2, fill=self.BRICK_DARK, width=2)  # Lower-right split.

    def draw_question_block(self, x, y, size=40):  # Draw one question block.
        s.create_rectangle(x, y, x + size, y + size, fill=self.QUESTION, outline=self.QUESTION_DARK, width=2)  # Block body.
        s.create_text(x + size / 2, y + size / 2, text="?", font=("Helvetica", 20, "bold"), fill="#3B2A00")  # Question mark.

    def draw_pipe(self, x, y, pipe_height=120):  # Draw green mario pipe.
        s.create_rectangle(x, y - pipe_height, x + 60, y, fill=self.PIPE, outline=self.PIPE_DARK, width=2)  # Pipe shaft.
        s.create_rectangle(x - 10, y - pipe_height, x + 70, y - pipe_height + 20, fill=self.PIPE, outline=self.PIPE_DARK, width=2)  # Pipe top.
        s.create_line(x + 30, y - pipe_height, x + 30, y, fill=self.PIPE_DARK, width=2)  # Pipe center split.

    def draw_mario(self, x, y, scale=2):  # Draw pixel-art mario and return item ids.
        pixels = [  # Encoded mario sprite rows.
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
        ]

        color_map = {  # Map sprite symbols to colors.
            "R": self.MARIO_RED,
            "B": self.MARIO_BROWN,
            "S": self.MARIO_SKIN,
            ".": None,
        }

        ixr = []  # Collect created rectangle ids.
        for row, line in enumerate(pixels):  # Loop each sprite row.
            for col, char in enumerate(line):  # Loop each sprite column.
                color = color_map.get(char)  # See what colour is used
                if color:  # Only draw non-empty sprite cells. So "." shouldn't be included or should be blank
                    x0 = x + col * scale  # Compute pixel left X based on scale.
                    y0 = y + row * scale  # Compute pixel top Y based on scale.
                    ixr.append(s.create_rectangle(x0, y0, x0 + scale, y0 + scale, fill=color, outline=color))  # Draw one pixel block.
        return ixr  # Return mario canvas ids.

    def draw_goomba(self, x, y):  
        ixr = []  # Collect goomba canvas ids.
        ixr.append(s.create_oval(x, y - 18, x + 30, y + 8, fill=self.GOOMBA, outline=self.GOOMBA_DARK, width=2))  # Body oval.
        ixr.append(s.create_oval(x + 6, y - 8, x + 12, y - 2, fill="white", outline="white"))  # Left eye.
        ixr.append(s.create_oval(x + 18, y - 8, x + 24, y - 2, fill="white", outline="white"))  # Right eye.
        ixr.append(s.create_oval(x + 8, y - 6, x + 10, y - 4, fill="black", outline="black"))  # Left eyeball.
        ixr.append(s.create_oval(x + 20, y - 6, x + 22, y - 4, fill="black", outline="black"))  # Right eyeball.
        return ixr  # Return goomba canvas ids.

    def draw_screen(self):  
        self.draw_clouds(90, 80, 1.1)  # Draw first cloud cluster.
        self.draw_clouds(520, 90, 1.4)  # Draw second cloud cluster.

        hb = height - 120  # hill baseline.
        self.draw_hill(40, hb, 160, 120)  # Draw left hill.
        self.draw_hill(320, hb + 10, 120, 90)  # Draw right hill.

        self.draw_ground()  # Draw brick ground tiles.
        self.draw_pipe(self.pipe_x, self.pipe_y, 120)  # Draw pipe 

        mario_ixr = self.draw_mario(self.mario_x, self.mario_y, 2)  # Draw mario on pipe.

        self.draw_brick(self.brick_x - 40, self.brick_y)  # Draw brick left of question block.
        self.draw_question_block(self.brick_x, self.brick_y)  # Draw center question block.
        self.draw_brick(self.brick_x + 40, self.brick_y)  # Draw brick right of question block.
        self.draw_brick(self.brick_x + 80, self.brick_y)  # Draw far-right brick.

        goomba1 = self.draw_goomba(560, height - 95)  # Draw first goomba.
        goomba2 = self.draw_goomba(610, height - 95)  # Draw second goomba.

        return mario_ixr, goomba1, goomba2  # Return ids for animation setup.

    # Private class to ensure its not called from outside as it can cause conflicts (I caught a few crashes)
    def __move_items(self, ixr, x, y):  # Translate a list of canvas items.
        for item_id in ixr:  # Iterate all item ids.
            s.move(item_id, x, y)  # Move one item by delta x/y (difference). special command that deletes for us

    
    def __set_mario_pos(self, x, y):  
        global speech_id  # Use global speech bubble
        x = x - mario_state["x"]  # Compute mario delta x.
        y = y - mario_state["y"]  # Compute mario delta y.
        self.__move_items(self.mario_ixr, x, y)  # Shift all mario pixels.
        mario_state["x"] = x  # Store new mario x.
        mario_state["y"] = y  # Store new mario y.
        # Store into central variable
            
    
    def __goomba_offset_at(self, t, goomba):  # Compute vertical bob at time t.
        return self.GOOMBA_BOB_AMPLITUDE * math.sin(t * self.GOOMBA_BOB_SPEED + goomba["phase"])  # Sinusoidal bob.

    
    def __goomba_top_at(self, t, goomba):  
        return goomba["base_y"] + self.__goomba_offset_at(t, goomba) + self.GOOMBA_TOP_OFFSET  # Base + bob + offset.

    def __kill_goomba(self, goomba):  # Not exactly kill, just squash
        if not goomba["alive"]:  # Ignore if already dead. Shouldn't ideally happen unless external intervention from the code
            return  

        goomba["alive"] = False  # Mark goomba dead.
        for item_id in goomba["ids"]:  # Remove all existing goomba parts.
            s.delete(item_id)  # Delete one goomba canvas item.

        y_now = goomba["base_y"] + goomba["offset"]  # Current goomba body Y.
        x = goomba["x"]  # Current goomba body X.
        squashed = s.create_oval(  # Draw flattened goomba body.
            x,
            y_now - 5,
            x + self.GOOMBA_W,
            y_now + 6,
            fill=self.GOOMBA_DARK,
            outline=self.GOOMBA_DARK,
        )
        goomba["ids"] = [squashed]  # Replace id list with squashed sprite.


    def __jump_to(self, tx, ty, duration, jump_height, on_complete=None):  
        mario_state["jump"] = {  # Save jump parameters for update loop.
            "start_time": eld,
            "duration": duration,
            "sx": mario_state["x"],
            "sy": mario_state["y"],
            "tx": tx,
            "ty": ty,
            "height": jump_height,
            "on_complete": on_complete,
        }

    def __run_right(self, speed):  
        mario_state["run"] = {"speed": speed}  # Positive speed means right.

    def __run_left(self, speed):  
        mario_state["run"] = {"speed": -speed}  # Negative speed means left.

    def __exit_right(self):  # Switch sequence to rightward exit motion.
        global sm  # Use global sequence mode.
        sm = "exiting"  # Enter exiting state. Again naming doesn't matter here as long as "exiting" is common
        self.__run_right(255.0)  # Apply rightward run speed. Value guessed and random

    def __jump_to_ground(self):  
        tx = mario_state["x"] + 44  # Push landing point forward on X.
        self.__jump_to(tx, self.gmy, duration=0.8, jump_height=70.0, on_complete=self.__exit_right)  # Start jump then exit.

    
    def __remove_speech(self):  # Remove current speech text if present.
        global speech_id  
        if speech_id is not None:  
            s.delete(speech_id)  
            speech_id = None  

    
    def __clear_speech(self):  
        global speech_id  
        speech_id = s.create_text(  
            mario_state["x"] + 10,
            mario_state["y"] - 16,
            text="Yeehaw~ uh.. Mario!",
            fill=self.HUD,
            font=("Helvetica", 16, "bold"),
            anchor="s",
        )
        r.after(1400, self.__remove_speech)  
        r.after(1400, self.__jump_to_ground)  

    def create_bomb(self):  
        global bomb_ixr, bft  #Bomb fuse time must be global
        if bomb_ixr:  
            return  # Exit if bomb already exists.

        bx = mario_state["x"] - 10  # Bomb base x near mario hand.
        by = mario_state["y"] + 20  # Bomb base y near mario hand.
        body = s.create_oval(bx, by, bx + 16, by + 16, fill="#1D1D1D", outline="#000000", width=2)  # Bomb body.
        fuse = s.create_line(bx + 12, by + 1, bx + 20, by - 8, fill="#222222", width=2)  # Fuse line.
        spark = s.create_oval(bx + 19, by - 10, bx + 23, by - 6, fill="#FFD44D", outline="#FF8C00")  # Spark tip.

        bomb_ixr = [body, fuse, spark]  
        bft = 0.0  

    def clear_bomb(self):
        global bomb_ixr, bft  
        for item_id in bomb_ixr:  
            s.delete(item_id)  
        bomb_ixr = []  
        bft = 0.0  

    def animate_bomb_fuse(self, dt):  
        global bft  
        if len(bomb_ixr) != 3:
            return  # Exit if bomb is incomplete. Shouldn't happen unless external interference or a bug.

        body, fuse, spark = bomb_ixr  
        bft = min(self.bf_td, bft + dt)  
        p = bft / self.bf_td  

        bx1, by1, bx2, _ = s.coords(body)  
        start_x = bx1 + 12  # Fuse start x at bomb top-right.
        start_y = by1 + 2  # Fuse start y at bomb top edge.

        far_x = bx2 + 7  # Fuse tip x when unburned.
        far_y = by1 - 10  # Fuse tip y when unburned.
        near_x = bx1 + 14  # Fuse tip x near end of burn.
        near_y = by1 - 3  # Fuse tip y near end of burn.

        end_x = far_x + (near_x - far_x) * p
        end_y = far_y + (near_y - far_y) * p  
        s.coords(fuse, start_x, start_y, end_x, end_y)  # Update fuse line.

        fuse_color = "#F5A623" if p > 0.35 else "#3A2A1A"  # Brighten fuse after initial burn.

        pulse = 2.1 + 0.9 * (0.5 + 0.5 * math.sin(eld * 38.0))  
        s.coords(spark, end_x - pulse, end_y - pulse, end_x + pulse, end_y + pulse)  

        if int(eld * 22) % 3 == 0:  # Spark color frame A.
            s.itemconfig(spark, fill="#FFE36C", outline="#FF7A00")  # Apply warm yellow/orange.
        elif int(eld * 22) % 3 == 1:  # Spark color frame B.
            s.itemconfig(spark, fill="#FFC94A", outline="#FF5A00")  # Apply deeper orange.
        else:  # Spark color frame C.
            s.itemconfig(spark, fill="#FFF2B3", outline="#FF8C00")  # Apply bright pale yellow.

    def reenter_with_bomb(self):  # Bring mario back from right carrying bomb.
        global sm  
        sm = "returning_with_bomb"  
        self.__set_mario_pos(width + 5, self.gmy)
        self.create_bomb()  
        self.__run_left(240.0)  

    def explode_map(self): # Explode the map at the end
        global sm  
        sm = "exploding"  
        mario_state["run"] = None  
        self.clear_bomb()  

        x = mario_state["x"] + 10  # Explosion center x near mario.
        y = self.gmy - 10  # Explosion center y near ground.

        blast1 = s.create_oval(x - 12, y - 12, x + 12, y + 12, fill="#FFF2B3", outline="#FF9900", width=2)  # Inner blast ring.
        blast2 = s.create_oval(x - 35, y - 35, x + 35, y + 35, fill="#FFB347", outline="#FF6A00", width=3)  # Mid blast ring.
        blast3 = s.create_oval(x - 65, y - 65, x + 65, y + 65, fill="#FF5A36", outline="#D72600", width=4)  # Outer blast ring.
        flash = s.create_rectangle(0, 0, width, height, fill="#FFF5D6", outline="")  # Full-screen flash.

        def wipe_scene():  # Replace level graphics with boom message.
            s.delete("all")  # Clear all canvas items.
            s.configure(bg="#1A120E")  # Set dark background color.
            s.create_text(width / 2, height / 2 - 18, text="BOOM!", fill="#FFB347", font=("Helvetica", 58, "bold"))  
            s.create_text(width / 2, height / 2 + 34, text="The map exploded.", fill="#FFE4C4", font=("Helvetica", 22, "bold"))  

        def delete_flash():  # Remove flash shortly after trigger.
            s.delete(flash)

        def delete_blasts():  # Remove blast rings.
            s.delete(blast1)
            s.delete(blast2)
            s.delete(blast3)

        r.after(120, delete_flash)
        r.after(240, delete_blasts)
        r.after(260, wipe_scene)  # Replace scene with final text.

    def jump_to_box(self):  
        target_x = self.brick_x + 4  
        target_y = self.brick_y - self.MARIO_H
        self.__jump_to(target_x, target_y, duration=1.0, jump_height=95.0, on_complete=self.jump_to_goomba1)  

    def jump_to_goomba1(self):  
        g1 = goombas[0]  
        landing_t = eld + 0.95  # Predict time at landing.
        target_x = g1["x"] + self.GOOMBA_W / 2 - self.MARIO_W / 2  # Center mario over goomba.
        target_y = self.__goomba_top_at(landing_t, g1) - self.MARIO_H + 1  # Land on goomba head.
        self.__jump_to(target_x, target_y, duration=0.95, jump_height=110.0, on_complete=self.stomp_goomba1)  

    def stomp_goomba1(self):  # Stomp first goomba then chain next jump.
        self.__kill_goomba(goombas[0])  # Squash first goomba.
        self.jump_to_goomba2()  # Immediately jump toward second goomba.

    def jump_to_goomba2(self):  # Jump from first stomp to second goomba.
        g2 = goombas[1]  # Select second goomba state.
        landing_t = eld + 0.95  # Predict time at landing.
        target_x = g2["x"] + self.GOOMBA_W / 2 - self.MARIO_W / 2  # Center mario over second goomba.
        target_y = self.__goomba_top_at(landing_t, g2) - self.MARIO_H + 1  # Land on second goomba head.
        self.__jump_to(target_x, target_y, duration=0.95, jump_height=92.0, on_complete=self.stomp_goomba2)  

    def stomp_goomba2(self):  # Stomp second goomba then show speech.
        self.__kill_goomba(goombas[1])  # Squash second goomba.
        self.__clear_speech()  # Show speech line and continue sequence.

    def draw_animation(self, mario_ixr, goomba1_ixr, goomba2_ixr):  # Initialize everything
        global mario_state, goombas, eld, lt, speech_id, bomb_ixr, bft, sm  

        self.mario_ixr = mario_ixr  # Store mario sprite ids for movement updates.

        mario_state = {  # Reset mario animation state.
            "x": float(self.mario_x),
            "y": float(self.mario_y),
            "jump": None,
            "run": None,
        }

        goombas = [  # Reset goomba runtime state.
            {
                "x": 560.0,
                "base_y": float(height - 95),
                "offset": 0.0,
                "phase": 0.0,
                "alive": True,
                "ids": goomba1_ixr,
            },
            {
                "x": 610.0,
                "base_y": float(height - 95),
                "offset": 0.0,
                "phase": math.pi,
                "alive": True,
                "ids": goomba2_ixr,
            },
        ]

        eld = 0.0  # Reset elapsed timer.
        lt = time.perf_counter()  # Capture initial frame clock.
        speech_id = None  # Clear speech text id.
        bomb_ixr = []  # Clear bomb ids.
        bft = 0.0  # Reset bomb fuse timer.
        sm = "main"  # Set initial sequence mode.

        r.after(500, self.jump_to_box)  
        r.after(16, self.update_scene)  

    def update_scene(self):  
        global eld, lt  

        now = time.perf_counter()  
        dt = min(0.05, now - lt)  
        lt = now  
        eld += dt  

        # Goombas continuously bob while alive
        for goomba in goombas:  
            if goomba["alive"]:  
                new_offset = self.__goomba_offset_at(eld, goomba)
                y = new_offset - goomba["offset"]
                goomba["offset"] = new_offset  
                self.__move_items(goomba["ids"], 0, y)  

        if bomb_ixr:  # Animate bomb only when bomb exists.
            self.animate_bomb_fuse(dt)  

        jump = mario_state["jump"]  
        if jump is not None:  # Handle parabolic jump motion.
            t = (eld - jump["start_time"]) / jump["duration"]
            if t > 1.0:  
                t = 1.0  

            base_x = jump["sx"] + (jump["tx"] - jump["sx"]) * t
            base_y = jump["sy"] + (jump["ty"] - jump["sy"]) * t  
            arc = jump["height"] * 4.0 * t * (1.0 - t)  
            self.__set_mario_pos(base_x, base_y - arc)  

            if t >= 1.0:
                mario_state["jump"] = None  
                if jump["on_complete"] is not None:  
                    jump["on_complete"]()  
        elif mario_state["run"] is not None:  # Handle if Mario state is not "run" which shouldn't happen
            speed = mario_state["run"]["speed"]  
            self.__set_mario_pos(mario_state["x"] + speed * dt, mario_state["y"])  

            if bomb_ixr:  
                self.__move_items(bomb_ixr, speed * dt, 0)  

            if sm == "exiting" and mario_state["x"] > width + 36:  
                mario_state["run"] = None  # Stop running at off-screen point.
                r.after(420, self.reenter_with_bomb)  
            elif sm == "returning_with_bomb" and mario_state["x"] < width * 0.62:  
                self.explode_map()  # Trigger explosion sequence.
                return  

        r.after(16, self.update_scene)  # Wait before starting next thing


class_call = creation()  
mario_ixr, goomba1_ixr, goomba2_ixr = class_call.draw_screen()  # Draw static scene and get ids.
class_call.draw_animation(mario_ixr, goomba1_ixr, goomba2_ixr)  # Initialize animation state and loops.

r.mainloop()  
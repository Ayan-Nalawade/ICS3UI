# UPDATE CODE FROM INITIAL WITH COMMENTS AND BETTER READABILITY

from tkinter import *  # Import Tkinter widgets and canvas primitives.
import math  # Import math for sine-wave bobbing and pulse effects.
import time  # Import time utilities for frame delta timing.

r = Tk()  # Create the main application window.
r.title("Mario Yeehaw")  # Set the title shown in the window bar.

height = 600  # Define the window/canvas height in pixels.
width = 800  # Define the window/canvas width in pixels.
s = Canvas(r, width=width, height=height, bg="#5C94FC", highlightthickness=0)  # Create the drawing canvas.
s.pack()  # Attach the canvas to the Tk window layout.

# Shared animation state
mario_state = {}  # Store mario position and current movement state.
goombas = []  # Store per-goomba animation and sprite data.
eld = 0.0  # Elapsed animation time in seconds.
lt = 0.0  # Last frame timestamp used to compute delta-time.
speech_id = None  # Canvas item id for mario speech text.
bomb_ixr = []  # Canvas item ids for bomb body/fuse/spark.
bft = 0.0  # Bomb fuse timer progress.
sm = "main"  # Sequence mode controlling animation phase.


class creation:  # Scene builder + animation controller class.
    def __init__(self):  # Initialize palette, constants, and anchor coordinates.
        self.SKY = "#5C94FC"  # Sky blue background color.
        self.BRICK = "#C84C0C"  # Main brick face color.
        self.BRICK_DARK = "#8B2E0D"  # Brick outline/shadow color.
        self.GROUND = "#C84C0C"  # Ground block color.
        self.GROUND_DARK = "#8B2E0D"  # Ground line/shadow color.
        self.PIPE = "#1E9C2A"  # Pipe main green color.
        self.PIPE_DARK = "#0F6B1C"  # Pipe outline/shadow color.
        self.HILL = "#4AAE2A"  # Hill body color.
        self.HILL_DARK = "#2E7D1A"  # Reserved darker hill color.
        self.CLOUD = "#FFFFFF"  # Cloud white color.
        self.CLOUD_SHADOW = "#CDE8FF"  # Cloud shadow highlight color.
        self.QUESTION = "#F7A000"  # Question block fill color.
        self.QUESTION_DARK = "#B26B00"  # Question block border color.
        self.MARIO_RED = "#E43B2C"  # Mario hat/shirt red color.
        self.MARIO_BROWN = "#8B4513"  # Mario hair/shoes brown color.
        self.MARIO_SKIN = "#FFD2A6"  # Mario skin tone color.
        self.GOOMBA = "#B5652A"  # Goomba body color.
        self.GOOMBA_DARK = "#7A3B12"  # Goomba outline/dark tone.
        self.HUD = "#FFFFFF"  # HUD text color.
        self.COIN = "#F7D000"  # Coin color.

        self.brick_y = height - 220  # Brick row Y anchor.
        self.brick_x = 360  # Question/brick row X anchor.
        self.pipe_x = 140  # Pipe X anchor.
        self.pipe_y = height - 80  # Pipe bottom Y anchor (ground top).
        self.mario_x = self.pipe_x + 8  # Mario starting X on top of pipe.
        self.mario_y = self.pipe_y - 120 - 28  # Mario starting Y on top of pipe.

        # Animation constants
        self.MARIO_W = 32  # Mario sprite width in pixels.
        self.MARIO_H = 28  # Mario sprite height in pixels.
        self.GOOMBA_W = 30  # Goomba sprite width reference.
        self.GOOMBA_TOP_OFFSET = -18  # Offset to approximate goomba top.
        self.GOOMBA_BOB_AMPLITUDE = 9  # Vertical bobbing amplitude.
        self.GOOMBA_BOB_SPEED = 6.0  # Vertical bobbing angular speed.
        self.bf_td = 2.4  # Bomb fuse total duration.

        self.gty = height - 80  # Ground top Y value.
        self.gmy = self.gty - self.MARIO_H  # Mario Y when standing on ground.

        self.mario_ixr = []  # Canvas ids for mario sprite pixels.

    def draw_clouds(self, x, y, scale=1.0) -> None:  # Draw layered cloud cluster at x/y.
        w = 70 * scale  # Base cloud width adjusted by scale.
        h = 30 * scale  # Base cloud height adjusted by scale.
        s.create_oval(x, y, x + w, y + h, fill=self.CLOUD, outline=self.CLOUD)  # Left cloud puff.
        s.create_oval(  # Middle/top cloud puff.
            x + 25 * scale,
            y - 10 * scale,
            x + 85 * scale,
            y + 25 * scale,
            fill=self.CLOUD,
            outline=self.CLOUD,
        )
        s.create_oval(  # Lower shadow puff for depth.
            x + 10 * scale,
            y + 10 * scale,
            x + 60 * scale,
            y + 40 * scale,
            fill=self.CLOUD_SHADOW,
            outline=self.CLOUD_SHADOW,
        )

    def draw_hill(self, x, y, w, h):  # Draw a simple oval hill.
        s.create_oval(x, y - h, x + w, y + h, fill=self.HILL, outline=self.HILL)  # Hill body.

    def draw_ground(self):  # Draw tiled ground rows across screen width.
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
        s.create_rectangle(x - 10, y - pipe_height, x + 70, y - pipe_height + 20, fill=self.PIPE, outline=self.PIPE_DARK, width=2)  # Pipe lip.
        s.create_line(x + 30, y - pipe_height, x + 30, y, fill=self.PIPE_DARK, width=2)  # Pipe center seam.

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
                color = color_map.get(char)  # Translate char to color.
                if color:  # Only draw non-empty sprite cells.
                    x0 = x + col * scale  # Compute pixel rect left X.
                    y0 = y + row * scale  # Compute pixel rect top Y.
                    ixr.append(s.create_rectangle(x0, y0, x0 + scale, y0 + scale, fill=color, outline=color))  # Draw one pixel block.
        return ixr  # Return mario canvas ids.

    def draw_goomba(self, x, y):  # Draw one goomba and return item ids.
        ixr = []  # Collect goomba canvas ids.
        ixr.append(s.create_oval(x, y - 18, x + 30, y + 8, fill=self.GOOMBA, outline=self.GOOMBA_DARK, width=2))  # Body oval.
        ixr.append(s.create_oval(x + 6, y - 8, x + 12, y - 2, fill="white", outline="white"))  # Left eye white.
        ixr.append(s.create_oval(x + 18, y - 8, x + 24, y - 2, fill="white", outline="white"))  # Right eye white.
        ixr.append(s.create_oval(x + 8, y - 6, x + 10, y - 4, fill="black", outline="black"))  # Left pupil.
        ixr.append(s.create_oval(x + 20, y - 6, x + 22, y - 4, fill="black", outline="black"))  # Right pupil.
        return ixr  # Return goomba canvas ids.

    def draw_screen(self):  # Draw static scene and return sprite ids.
        self.draw_clouds(90, 80, 1.1)  # Draw first cloud cluster.
        self.draw_clouds(520, 90, 1.4)  # Draw second cloud cluster.

        hb = height - 120  # Compute hill baseline.
        self.draw_hill(40, hb, 160, 120)  # Draw left hill.
        self.draw_hill(320, hb + 10, 120, 90)  # Draw right hill.

        self.draw_ground()  # Draw brick ground tiles.
        self.draw_pipe(self.pipe_x, self.pipe_y, 120)  # Draw pipe in foreground.

        mario_ixr = self.draw_mario(self.mario_x, self.mario_y, 2)  # Draw mario on pipe.

        self.draw_brick(self.brick_x - 40, self.brick_y)  # Draw brick left of question block.
        self.draw_question_block(self.brick_x, self.brick_y)  # Draw center question block.
        self.draw_brick(self.brick_x + 40, self.brick_y)  # Draw brick right of question block.
        self.draw_brick(self.brick_x + 80, self.brick_y)  # Draw far-right brick.

        goomba1 = self.draw_goomba(560, height - 95)  # Draw first goomba.
        goomba2 = self.draw_goomba(610, height - 95)  # Draw second goomba.

        return mario_ixr, goomba1, goomba2  # Return ids for animation setup.

    # Move every canvas item in a list
    def __move_items(self, ixr, dx, dy):  # Translate a list of canvas items.
        for item_id in ixr:  # Iterate all item ids.
            s.move(item_id, dx, dy)  # Move one item by delta x/y.

    # Move mario sprite and sync speech bubble
    def __set_mario_pos(self, x, y):  # Move mario sprite to absolute x/y.
        global speech_id  # Use global speech bubble id.
        dx = x - mario_state["x"]  # Compute mario delta x.
        dy = y - mario_state["y"]  # Compute mario delta y.
        self.__move_items(self.mario_ixr, dx, dy)  # Shift all mario pixels.
        mario_state["x"] = x  # Store new mario x.
        mario_state["y"] = y  # Store new mario y.

        if speech_id is not None:  # Reposition text if speech exists.
            s.coords(speech_id, x + 10, y - 16)  # Keep speech above mario.

    # Bobbing offset for a goomba
    def __goomba_offset_at(self, t, goomba):  # Compute vertical bob offset at time t.
        return self.GOOMBA_BOB_AMPLITUDE * math.sin(t * self.GOOMBA_BOB_SPEED + goomba["phase"])  # Sinusoidal bob.

    # Top position for stomping
    def __goomba_top_at(self, t, goomba):  # Estimate goomba top Y for landing.
        return goomba["base_y"] + self.__goomba_offset_at(t, goomba) + self.GOOMBA_TOP_OFFSET  # Base + bob + offset.

    # Replace alive goomba with squashed sprite
    def __kill_goomba(self, goomba):  # Convert a living goomba to squashed state.
        if not goomba["alive"]:  # Ignore if already dead.
            return  # Exit early when already handled.

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

    # Create a jump arc toward a target
    def __jump_to(self, tx, ty, duration, jump_height, on_complete=None):  # Start jump state machine.
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

    def __run_right(self, speed):  # Start continuous run to the right.
        mario_state["run"] = {"speed": speed}  # Positive speed means right.

    def __run_left(self, speed):  # Start continuous run to the left.
        mario_state["run"] = {"speed": -speed}  # Negative speed means left.

    def __exit_right(self):  # Switch sequence to rightward exit motion.
        global sm  # Use global sequence mode.
        sm = "exiting"  # Enter exiting state.
        self.__run_right(255.0)  # Apply rightward run speed.

    def __jump_to_ground(self):  # Queue jump down from blocks to ground.
        tx = mario_state["x"] + 44  # Push landing point forward on X.
        self.__jump_to(tx, self.gmy, duration=0.8, jump_height=70.0, on_complete=self.__exit_right)  # Start jump then exit.

    # Delete speech bubble
    def __remove_speech(self):  # Remove current speech text if present.
        global speech_id  # Use global speech id.
        if speech_id is not None:  # Ensure there is text to remove.
            s.delete(speech_id)  # Delete speech text from canvas.
            speech_id = None  # Clear stored speech id.

    # Show speech and queue next action
    def __clear_speech(self):  # Show text line and schedule next jump.
        global speech_id  # Use global speech id.
        speech_id = s.create_text(  # Create speech bubble text.
            mario_state["x"] + 10,
            mario_state["y"] - 16,
            text="Yeehaw~ uh.. Mario!",
            fill=self.HUD,
            font=("Helvetica", 16, "bold"),
            anchor="s",
        )
        r.after(1400, self.__remove_speech)  # Remove speech after delay.
        r.after(1400, self.__jump_to_ground)  # Start jump to ground after delay.

    def create_bomb(self):  # Spawn bomb attached to mario.
        global bomb_ixr, bft  # Use global bomb state.
        if bomb_ixr:  # Avoid duplicate bomb spawn.
            return  # Exit if bomb already exists.

        bx = mario_state["x"] - 10  # Bomb base x near mario hand.
        by = mario_state["y"] + 20  # Bomb base y near mario hand.
        body = s.create_oval(bx, by, bx + 16, by + 16, fill="#1D1D1D", outline="#000000", width=2)  # Bomb body.
        fuse = s.create_line(bx + 12, by + 1, bx + 20, by - 8, fill="#222222", width=2)  # Fuse line.
        spark = s.create_oval(bx + 19, by - 10, bx + 23, by - 6, fill="#FFD44D", outline="#FF8C00")  # Spark tip.

        bomb_ixr = [body, fuse, spark]  # Save bomb item ids.
        bft = 0.0  # Reset fuse timer.

    def clear_bomb(self):  # Delete bomb sprites and reset fuse.
        global bomb_ixr, bft  # Use global bomb state.
        for item_id in bomb_ixr:  # Iterate bomb parts.
            s.delete(item_id)  # Delete one bomb part.
        bomb_ixr = []  # Clear bomb id list.
        bft = 0.0  # Reset fuse timer to zero.

    def animate_bomb_fuse(self, dt):  # Animate fuse shortening and spark pulse.
        global bft  # Use global fuse timer.
        if len(bomb_ixr) != 3:  # Require all bomb parts to animate.
            return  # Exit if bomb is incomplete.

        body, fuse, spark = bomb_ixr  # Unpack bomb canvas ids.
        bft = min(self.bf_td, bft + dt)  # Advance fuse timer with cap.
        p = bft / self.bf_td  # Normalize fuse progress 0..1.

        bx1, by1, bx2, _ = s.coords(body)  # Read bomb body bounds.
        start_x = bx1 + 12  # Fuse start x at bomb top-right.
        start_y = by1 + 2  # Fuse start y at bomb top edge.

        far_x = bx2 + 7  # Fuse tip x when unburned.
        far_y = by1 - 10  # Fuse tip y when unburned.
        near_x = bx1 + 14  # Fuse tip x near end of burn.
        near_y = by1 - 3  # Fuse tip y near end of burn.

        end_x = far_x + (near_x - far_x) * p  # Interpolate fuse tip x.
        end_y = far_y + (near_y - far_y) * p  # Interpolate fuse tip y.
        s.coords(fuse, start_x, start_y, end_x, end_y)  # Update fuse line.

        fuse_color = "#F5A623" if p > 0.35 else "#3A2A1A"  # Brighten fuse after initial burn.
        s.itemconfig(fuse, fill=fuse_color)  # Apply dynamic fuse color.

        pulse = 2.1 + 0.9 * (0.5 + 0.5 * math.sin(eld * 38.0))  # Spark pulse radius.
        s.coords(spark, end_x - pulse, end_y - pulse, end_x + pulse, end_y + pulse)  # Move spark to fuse tip.

        if int(eld * 22) % 3 == 0:  # Spark color frame A.
            s.itemconfig(spark, fill="#FFE36C", outline="#FF7A00")  # Apply warm yellow/orange.
        elif int(eld * 22) % 3 == 1:  # Spark color frame B.
            s.itemconfig(spark, fill="#FFC94A", outline="#FF5A00")  # Apply deeper orange.
        else:  # Spark color frame C.
            s.itemconfig(spark, fill="#FFF2B3", outline="#FF8C00")  # Apply bright pale yellow.

    def reenter_with_bomb(self):  # Bring mario back from right carrying bomb.
        global sm  # Use global sequence mode.
        sm = "returning_with_bomb"  # Switch sequence phase.
        self.__set_mario_pos(width + 5, self.gmy)  # Teleport mario just offscreen right.
        self.create_bomb()  # Spawn bomb in mario hand.
        self.__run_left(240.0)  # Start running left.

    def explode_map(self):  # Trigger explosion and final scene wipe.
        global sm  # Use global sequence mode.
        sm = "exploding"  # Mark sequence as exploding.
        mario_state["run"] = None  # Stop run motion.
        self.clear_bomb()  # Remove bomb graphics.

        cx = mario_state["x"] + 10  # Explosion center x near mario.
        cy = self.gmy - 10  # Explosion center y near ground.

        blast1 = s.create_oval(cx - 12, cy - 12, cx + 12, cy + 12, fill="#FFF2B3", outline="#FF9900", width=2)  # Inner blast ring.
        blast2 = s.create_oval(cx - 35, cy - 35, cx + 35, cy + 35, fill="#FFB347", outline="#FF6A00", width=3)  # Mid blast ring.
        blast3 = s.create_oval(cx - 65, cy - 65, cx + 65, cy + 65, fill="#FF5A36", outline="#D72600", width=4)  # Outer blast ring.
        flash = s.create_rectangle(0, 0, width, height, fill="#FFF5D6", outline="")  # Full-screen flash.

        def wipe_scene():  # Replace level graphics with boom message.
            s.delete("all")  # Clear all canvas items.
            s.configure(bg="#1A120E")  # Set dark background color.
            s.create_text(width / 2, height / 2 - 18, text="BOOM!", fill="#FFB347", font=("Helvetica", 58, "bold"))  # Draw boom title.
            s.create_text(width / 2, height / 2 + 34, text="The map exploded.", fill="#FFE4C4", font=("Helvetica", 22, "bold"))  # Draw subtitle.

        r.after(120, lambda: s.delete(flash))  # Remove flash shortly after trigger.
        r.after(240, lambda: [s.delete(blast1), s.delete(blast2), s.delete(blast3)])  # Remove blast rings.
        r.after(260, wipe_scene)  # Replace scene with final text.

    def jump_to_box(self):  # Start first jump from pipe to brick row.
        target_x = self.brick_x + 4  # Target x near center question block.
        target_y = self.brick_y - self.MARIO_H  # Target y to stand on top.
        self.__jump_to(target_x, target_y, duration=1.0, jump_height=95.0, on_complete=self.jump_to_goomba1)  # Chain to first stomp jump.

    def jump_to_goomba1(self):  # Jump from block toward first goomba.
        g1 = goombas[0]  # Select first goomba state.
        landing_t = eld + 0.95  # Predict time at landing.
        target_x = g1["x"] + self.GOOMBA_W / 2 - self.MARIO_W / 2  # Center mario over goomba.
        target_y = self.__goomba_top_at(landing_t, g1) - self.MARIO_H + 1  # Land on goomba head.
        self.__jump_to(target_x, target_y, duration=0.95, jump_height=110.0, on_complete=self.stomp_goomba1)  # Chain stomp callback.

    def stomp_goomba1(self):  # Stomp first goomba then chain next jump.
        self.__kill_goomba(goombas[0])  # Squash first goomba.
        self.jump_to_goomba2()  # Immediately jump toward second goomba.

    def jump_to_goomba2(self):  # Jump from first stomp to second goomba.
        g2 = goombas[1]  # Select second goomba state.
        landing_t = eld + 0.95  # Predict time at landing.
        target_x = g2["x"] + self.GOOMBA_W / 2 - self.MARIO_W / 2  # Center mario over second goomba.
        target_y = self.__goomba_top_at(landing_t, g2) - self.MARIO_H + 1  # Land on second goomba head.
        self.__jump_to(target_x, target_y, duration=0.95, jump_height=92.0, on_complete=self.stomp_goomba2)  # Chain second stomp callback.

    def stomp_goomba2(self):  # Stomp second goomba then show speech.
        self.__kill_goomba(goombas[1])  # Squash second goomba.
        self.__clear_speech()  # Show speech line and continue sequence.

    def draw_animation(self, mario_ixr, goomba1_ixr, goomba2_ixr):  # Initialize all mutable animation state.
        global mario_state, goombas, eld, lt, speech_id, bomb_ixr, bft, sm  # Use shared global runtime state.

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

        r.after(500, self.jump_to_box)  # Delay then start first jump action.
        r.after(16, self.update_scene)  # Start frame update loop.

    def update_scene(self):  # Per-frame animation update callback.
        global eld, lt  # Use shared frame timers.

        now = time.perf_counter()  # Read current high-res timestamp.
        dt = min(0.05, now - lt)  # Compute and clamp frame delta.
        lt = now  # Save timestamp for next frame.
        eld += dt  # Advance elapsed animation time.

        # Goombas continuously bob while alive
        for goomba in goombas:  # Iterate each goomba state record.
            if goomba["alive"]:  # Animate only living goombas.
                new_offset = self.__goomba_offset_at(eld, goomba)  # Compute desired bob offset.
                dy = new_offset - goomba["offset"]  # Compute movement delta.
                goomba["offset"] = new_offset  # Store latest offset.
                self.__move_items(goomba["ids"], 0, dy)  # Apply vertical movement.

        if bomb_ixr:  # Animate bomb only when bomb exists.
            self.animate_bomb_fuse(dt)  # Advance bomb fuse visuals.

        jump = mario_state["jump"]  # Read active jump state.
        if jump is not None:  # Handle parabolic jump motion.
            t = (eld - jump["start_time"]) / jump["duration"]  # Compute normalized jump progress.
            if t > 1.0:  # Cap jump progress at the end.
                t = 1.0  # Clamp to exactly finished.

            base_x = jump["sx"] + (jump["tx"] - jump["sx"]) * t  # Interpolate horizontal position.
            base_y = jump["sy"] + (jump["ty"] - jump["sy"]) * t  # Interpolate baseline vertical position.
            arc = jump["height"] * 4.0 * t * (1.0 - t)  # Parabolic jump arc height.
            self.__set_mario_pos(base_x, base_y - arc)  # Apply mario jump position.

            if t >= 1.0:  # Complete jump when progress reaches end.
                mario_state["jump"] = None  # Clear current jump state.
                if jump["on_complete"] is not None:  # Run callback if provided.
                    jump["on_complete"]()  # Trigger next sequence action.
        elif mario_state["run"] is not None:  # Otherwise handle run motion.
            speed = mario_state["run"]["speed"]  # Read current run speed.
            self.__set_mario_pos(mario_state["x"] + speed * dt, mario_state["y"])  # Move mario by speed.

            if bomb_ixr:  # Move bomb with mario if bomb is active.
                self.__move_items(bomb_ixr, speed * dt, 0)  # Apply same horizontal shift.

            if sm == "exiting" and mario_state["x"] > width + 36:  # Check if mario exited right side.
                mario_state["run"] = None  # Stop running at off-screen point.
                r.after(420, self.reenter_with_bomb)  # Schedule return with bomb.
            elif sm == "returning_with_bomb" and mario_state["x"] < width * 0.62:  # Check explosion trigger point.
                self.explode_map()  # Trigger explosion sequence.
                return  # Stop loop restart for this frame.

        r.after(16, self.update_scene)  # Schedule next frame update.


class_call = creation()  # Instantiate scene/animation controller.
mario_ixr, goomba1_ixr, goomba2_ixr = class_call.draw_screen()  # Draw static scene and get ids.
class_call.draw_animation(mario_ixr, goomba1_ixr, goomba2_ixr)  # Initialize animation state and loops.

r.mainloop()  # Enter Tkinter event loop.

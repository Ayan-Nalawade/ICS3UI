from tkinter import *
from random import *
import time

root = Tk()

screen = Canvas(root, width=800, height=600, bg="green")
screen.pack()


screen.create_oval(0, 285, 50, 315, fill="gray", width=0)
screen.create_oval(750, 285, 800, 315, fill="gray", width=0)


screen.create_rectangle(350, 0, 450, 600, fill="turquoise", width=0)

colors = ["gray26", "gray36", "gray47", "gray62"]


for i in range(100):
    space = 8 * i
    size = randint(5, 7)
    size2 = randint(5, 7)
    color = choice(colors)
    color2 = choice(colors)

    screen.create_oval(350 - size, space - size,
                       350 + size, space + size,
                       fill=color, width=0)

    screen.create_oval(450 - size2, space - size2,
                       450 + size2, space + size2,
                       fill=color2, width=0)

screen.create_rectangle(335, 20, 465, 85,
                        fill="saddlebrown",
                        width=5, outline="brown4")

screen.create_rectangle(335, 515, 465, 580,
                        fill="saddlebrown",
                        width=5, outline="brown4")


for x in range(340, 465, 12):
    screen.create_rectangle(x, 20, x+6, 85, fill="peru", width=0)   # top
    screen.create_rectangle(x, 515, x+6, 580, fill="peru", width=0) # bottom


player = screen.create_rectangle(25, 290, 45, 310, fill="blue", width=2)


screen.create_rectangle(125, 225, 150, 375, fill="gray45", width=2)
screen.create_rectangle(50, 200, 150, 225, fill="gray45", width=2)
screen.create_rectangle(50, 375, 150, 400, fill="gray45", width=2)


screen.create_rectangle(675, 225, 650, 375, fill="gray45", width=2)
screen.create_rectangle(750, 200, 650, 225, fill="gray45", width=2)
screen.create_rectangle(750, 375, 650, 400, fill="gray45", width=2)


screen.create_line(660, 250, 660, 330, fill="black", width=4)  # pole
screen.create_polygon(660, 260, 710, 280, 660, 300, fill="red", outline="darkred")


screen.create_rectangle(645, 240, 720, 250, fill="gray30", width=3)  # top
screen.create_rectangle(645, 320, 720, 330, fill="gray30", width=3)  # bottom
screen.create_rectangle(645, 240, 655, 330, fill="gray30", width=3)  # left
screen.create_rectangle(710, 240, 720, 330, fill="gray30", width=3)  # right


fish = []
for i in range(5):
    x = randint(355, 445)
    y = randint(100, 500)
    f = screen.create_oval(x-8, y-4, x+12, y+4, fill="orange", outline="darkorange")
    fish.append((f, randint(-2,2), randint(-1,1)))  

def animate_fish():
    for i in range(len(fish)):
        f, x, y = fish[i]
        screen.move(f, x, y)

        x1, y1, x2, y2 = screen.coords(f)

        if x1 < 350 or x2 > 450:
            x = -x
        if y1 < 0 or y2 > 600:
            y = -y
            
        if 350 < x1 and x2 < 450:
            # top bridge
            if y1 < 85 and y2 > 20:
                y = abs(y)
            # bottom bridge
            if y2 > 515 and y1 < 580:
                y = -abs(y)

        fish[i] = (f, x, y)

    root.after(50, animate_fish)  # loop animation properly

animate_fish()

root.mainloop()
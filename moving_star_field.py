import tkinter as tk
from random import randint as rand
from random import uniform as uni
from time import sleep

check_list_only = False

r = tk.Tk()
r.geometry('600x600')
WIDTH = r.winfo_screenwidth()
HEIGHT = r.winfo_screenheight()
f = tk.Canvas(r, width=WIDTH, height=HEIGHT, background="black")
f.pack()

color = "floral white"

how_many_stars = 1000

x = []
y = []

xspeed = []
yspeed = []

size = []
def setup_stars():
    x.clear()
    y.clear()
    xspeed.clear()
    yspeed.clear()
    for _ in range(how_many_stars):
        x.append(rand(0,WIDTH))
        y.append(rand(0,HEIGHT))
        
        xspeed.append(uni(-10,-5))
        yspeed.append(0)
        
        size.append(rand(0,6))

setup_stars()

for n in range(how_many_stars):
    for b in range(how_many_stars):
        f.create_oval(x[b], y[b], x[b]+size[b], y[b]+size[b], fill=color)
        x[b] += xspeed[b]
        
        if x[b] < 0:
            x[b] = WIDTH
            y[b] = rand(0,HEIGHT)
    
    f.update()
    r.after(100)
    f.delete("all")



r.mainloop()
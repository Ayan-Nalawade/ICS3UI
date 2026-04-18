import tkinter as tk

r = tk.Tk()
r.geometry('600x600')
WIDTH = 600
HEIGHT = 600
f = tk.Canvas(r, width=WIDTH, height=HEIGHT, background="black")
f.pack()

word = "trees"
wl: list = list(word) # Word List
gl:list = [] # Guess List

picked:dict = {}

g_max = 6
g_usr = 0

box_s = 50
ini_x = 10
ini_y = 10

def end_game():
    t_box.delete(0, tk.END)
    t_box.insert(0, f"The word was: {word}")
    t_box.config(state='disabled')

def game_won():
    t_box.delete(0, tk.END)
    t_box.insert(0, "You guessed the word!!")
    t_box.config(state='disabled')

def update(ini_y):
    global box_s
    global ini_x
    global picked
    global gl
    global wl

    count = 0

    picked.clear()   
    ini_x = 10       

    for e in range(0, len(gl)):
        color = ""


        if gl[e] == wl[e]:
            color = "green"
            picked[gl[e]] = 1
            count += 1

        elif gl[e] in wl:

            compare = wl.copy()


            for i in range(len(gl)):
                if gl[i] == wl[i] and gl[i] == gl[e]:
                    if gl[e] in compare:
                        compare.remove(gl[e])

            if gl[e] in compare:
                color = "orange"
            else:
                color = "grey"

        else:
            color = "grey"

        f.create_rectangle(
            ini_x, ini_y,
            ini_x + box_s, ini_y + box_s,
            outline="black",
            fill=color
        )

        f.create_text(
            ini_x + (box_s / 2),
            ini_y + (box_s / 2),
            text=gl[e].upper(),
            fill="white",
            font="Helvetica"
        )

        ini_x += box_s + 5

        if count == len(word):
            game_won()
            return

def submit(event=None):
    global g_usr
    global ini_x
    global gl
    g = t_box.get()
    if len(g) != len(word):
        t_box.delete(0, tk.END)
        return 
    gl = list(g)
    yval = plist.get(g_usr)
    update(yval)
    if g_usr == g_max-1:
        end_game()
        return
    ini_x = 10
    g_usr += 1
    t_box.delete(0, tk.END)


def draw_box() -> dict:
    global ini_x
    global ini_y
    global box_s 

    mlist = {}
    for i in range(0,g_max):
        for _ in range(0,len(word)):
            f.create_rectangle(ini_x, ini_y, ini_x+box_s, ini_y+box_s, outline="black", fill="grey")
            ini_x += box_s+5
        ini_x = 10
        mlist[i] = ini_y
        ini_y += box_s+5
    return mlist

plist = draw_box() # Save dict in this
print(plist)


t_box = tk.Entry(r)
t_box.place(x=0, y=HEIGHT-50, width=WIDTH, height=50)


t_box.bind("<Return>", submit)


r.mainloop()
import tkinter as tk
from random import randint as rand

pick:str = ""

while True:
    fi = input("Easy or Hard mode?: ")
    if fi.lower() == "easy":
        with open("Easy combinations.txt", "r") as x:
            data = x.readlines()
            pick = data[rand(0,len(data)-1)]
            
        break
    elif fi.lower() == "hard":
        with open("Hard combinations.txt", "r") as x:
            data = x.readlines()
            pick = data[rand(0,len(data)-1)]
            
        break
    else:
        print("Enter Easy or Hard!")
        continue
    
print(f"Debug: {pick}")
# Pick a random word based on the user decision to play easy or hard mode
r = tk.Tk()
WIDTH = 600
HEIGHT = 600
r.geometry(f"{WIDTH}x{HEIGHT}")
f = tk.Canvas(r, background="orange")
f.pack(fill="both", expand=True) # Only after the user picks we want to create the screen
    


f.create_rectangle(10,10,60,60,fill="#3D360F")


f.mainloop()
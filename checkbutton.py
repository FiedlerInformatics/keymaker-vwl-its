import tkinter as tk
from tkinter import *

root = tk.Tk()
root.geometry("350x350")

def printCheckbuttonBool():
    if checkButtonBool.get():
        print("True")
    else:
        print("False") 

checkButtonBool = IntVar()
checkbutton  = tk.Checkbutton(root, text="Checkbutton", variable=checkButtonBool)
button = tk.Button(root,text="Print Checkbutton value")

checkbutton.pack()
button.pack()


button.bind("<Button-1>", lambda event: printCheckbuttonBool())
root.mainloop()


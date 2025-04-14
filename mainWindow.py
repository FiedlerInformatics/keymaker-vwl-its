import pykeepass.exceptions
from keepassObject import Key
from tkinter import *
import tkinter as tk
from tkinter import ttk, filedialog
import sv_ttk
import pykeepass
from pykeepass import PyKeePass
from pathlib import Path
from PIL import ImageTk, Image

main_window = tk.Tk()
main_window.geometry("900x700")
main_window.title("Keymaker")

style = ttk.Style(main_window)
style.theme_use("vista")
main_window.iconbitmap(default="keymaker_images/lockSymbol.ico")

trennlinie = tk.Frame(main_window,bg='black',width=1)

create_key_buttton = ttk.Label(main_window,text="Key erstellen",font="Helvetica 17")
print_key_buttton = ttk.Label(main_window,text="Key drucken", font="Helvetica 17")

gerat_label = ttk.Label(main_window,text="Gerät", font="Helvetica 15 bold")
gerat_input = ttk.Entry(main_window,width=50,font=("Helvetica 15"))

# Layout main_window
main_window.columnconfigure(0, weight=1)
for col in (1, 2):
    main_window.columnconfigure(col, weight=4)
for row in range(16):
    main_window.rowconfigure(row, weight=1)


create_key_buttton.grid(column=0,row=1,sticky='w',padx=40)
print_key_buttton.grid(column=0,row=2,sticky='w',padx=40)

trennlinie.grid(row=0,column=0,sticky="nes",rowspan=16,padx=10)

gerat_label.grid(row=1,column=1,sticky='wn')
gerat_input.grid(row=1,column=1,sticky='ws')

main_window.mainloop()
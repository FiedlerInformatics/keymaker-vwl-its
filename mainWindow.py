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
from keepassObject import Key
import subprocess
import pickle
import os



main_window = tk.Tk()
main_window.geometry("900x700")
main_window.minsize(900,700)
main_window.title("Keymaker")

style = ttk.Style(main_window)
style.theme_use("vista")
main_window.iconbitmap(default="keymaker_images/lockSymbol.ico")

trennlinie = tk.Frame(main_window,bg='black',width=1)

browse_txt = ttk.Button(main_window, text=".txt-Datei")
txt_entry = ttk.Entry(main_window)

create_key_buttton = ttk.Label(main_window,text="Key erstellen",font="Helvetica 12 bold")
print_key_buttton = ttk.Label(main_window,text="Key drucken", font="Helvetica 12 bold")

person_label = ttk.Label(main_window,text="Person", font="Helvetica 12")
person_input = ttk.Entry(main_window, font=("Helvetica 12"))

geraet_label = ttk.Label(main_window,text="Gerät", font="Helvetica 12")
geraet_input = ttk.Entry(main_window,font=("Helvetica 12"))

lehrstuhl_label = ttk.Label(main_window, text="Lehrstuhl", font="Helvetica 12")
lehrstuhl_input = ttk.Entry(main_window, font=("Helvetica 12"))

seriennummer_label = ttk.Label(main_window, text="Seriennummer", font="Helvetica 12")
seriennummer_input = ttk.Entry(main_window, font=("Helvetica 12"))

datum_label = ttk.Label(main_window, text="Datum", font="Helvetica 12")
datum_input = ttk.Entry(main_window, font=("Helvetica 12"))

inventarnummer_label = ttk.Label(main_window, text="Inventarnummer", font="Helvetica 12 ")
inventarnummer_input = ttk.Entry(main_window, font=("Helvetica 12"))

hilfskraft_label = ttk.Label(main_window, text="Hilfskraft", font="Helvetica 12")
hilfskraft_input = ttk.Entry(main_window, font=("Helvetica 12"))

bitlocker_key_label = ttk.Label(main_window, text="Bitlocker Key", font="Helvetica 12")
bitlocker_key_input = ttk.Entry(main_window, font=("Helvetica 12"))

bitlocker_bezeichner_label = ttk.Label(main_window, text="Bitlocker Bezeichner", font="Helvetica 12")
bitlocker_bezeichner_input = ttk.Entry(main_window, font=("Helvetica 12"))


main_window.columnconfigure(0,weight=1)
main_window.columnconfigure(1,weight=1)
main_window.columnconfigure(2,weight=1)
main_window.columnconfigure(4,weight=1)
for col in (1, 3):
    main_window.columnconfigure(col, weight=3)
for row in range(16):
    main_window.rowconfigure(row, weight=1)


create_key_buttton.grid(column=0,row=1,sticky='w',padx=(10,5))
print_key_buttton.grid(column=0,row=2,sticky='w',padx=(10,5))

trennlinie.grid(row=0,column=0,sticky="nes",rowspan=16,padx=10)

person_label.grid(row=2,column=1,sticky='wn',padx=(20,0))
person_input.grid(row=2,column=1,sticky='wes',padx=(20,0))

geraet_label.grid(row=2,column=3,sticky='wn',padx=(0,20))
geraet_input.grid(row=2,column=3,sticky='wes',padx=(0,20))  

lehrstuhl_label.grid(row=4, column=1, sticky='wn',padx=(20,0))
lehrstuhl_input.grid(row=4, column=1, sticky='wes',padx=(20,0))

seriennummer_label.grid(row=4, column=3, sticky='wn',padx=(0,20))
seriennummer_input.grid(row=4, column=3, sticky='wes',padx=(0,20))

datum_label.grid(row=6, column=1, sticky='wn',padx=(20,0))
datum_input.grid(row=6, column=1, sticky='wes', padx=(20,0))

inventarnummer_label.grid(row=6, column=3, sticky='wn',padx=(0,20))
inventarnummer_input.grid(row=6, column=3, sticky='wes', padx=(0,20))

hilfskraft_label.grid(row=8, column=1, sticky='wn',padx=(20,0))
hilfskraft_input.grid(row=8, column=1, sticky='wes', padx=(20,0))

bitlocker_bezeichner_label.grid(row=10, column=1, sticky='wn', padx=(20,20))
bitlocker_bezeichner_input.grid(row=10, column=1, sticky='wes', columnspan=3, padx=(20,20))

bitlocker_key_label.grid(row=12, column=1, sticky='wn',padx=(20,20 ))
bitlocker_key_input.grid(row=12, column=1, sticky='wes', columnspan=3, padx=(20,20))

main_window.mainloop()

    
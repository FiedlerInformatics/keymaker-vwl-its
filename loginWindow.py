from keepassObject import Key
from tkinter import *
import tkinter as tk
from tkinter import ttk
import sv_ttk
import pykeepass as pykp
from pathlib import Path
from PIL import ImageTk, Image

login_window = tk.Tk()
login_window.geometry("700x433")
login_window.resizable(False,False)
login_window.title("Keymaker")

style = ttk.Style()
style.theme_use("vista")
login_window.iconbitmap(default="keymaker_images/lockSymbol.ico")

image = ImageTk.PhotoImage(Image.open("keymaker_images/loginImage2.jpg"))
image_label = ttk.Label(login_window, image=image)

keymakerHeader = ttk.Label(login_window,text="Keymaker",font="Helvetica 40 bold")
datenbankAuswahlMeldung = ttk.Label(login_window, text="Wählen Sie eine .kdbx-Datei", font="Helvetica")
error_message = ttk.Label(login_window, text="")

browse_database = ttk.Button(text=".kdbx-Datei")
database_entry = ttk.Entry(login_window, width=50)

password_label = ttk.Label(login_window, text="Password", font="Helvetica 10")
password_entry = ttk.Entry(login_window, show="●", width=50)

login_button = ttk.Button(text="Anmelden", width=20)

# Layout login_window

image_label.place(x=0,y=0)
keymakerHeader.place(x=365,y=40)
datenbankAuswahlMeldung.place(x=365,y=144)
error_message.place(x=400,y=180)

browse_database.place(x=340,y=215)
database_entry.place(x=340,y=245)

password_label.place(x=340,y=280)
password_entry.place(x=340, y=302)

login_button.place(x=430,y=357)

# Aktualisierung der Eingabe
login_window.mainloop()
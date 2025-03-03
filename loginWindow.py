from keepassObject import Key
import tkinter as tk
import pykeepass as pykp
from pathlib import Path
from PIL import ImageTk, Image

login_window = tk.Tk()
login_window.geometry("700x433")
login_window.resizable(False,False)
login_window.title("Keymaker")
im = Image.open("loginImage.jpg")
image = ImageTk.PhotoImage(im)
image_label = tk.Label(login_window, image=image)

datenbankAuswahlMeldung = tk.Label(login_window, text="Wählen Sie eine .kdbx-Datei")
error_message = tk.Label(login_window, text="")

browse_database = tk.Button(text=".kdbx-Datei")
database_entry = tk.Entry(login_window, width=50)

password_label = tk.Label(login_window, text="Password")
password_entry = tk.Entry(login_window, show="●", width=50)

login_button = tk.Button(text="Anmelden", width=20, height=2)

# Layout login_window



image_label.place(x=0,y=0)
datenbankAuswahlMeldung.place(x=400,y=144)
error_message.place(x=400,y=180)

browse_database.place(x=340,y=210)
database_entry.place(x=340,y=245)

password_label.place(x=340,y=285)
password_entry.place(x=340, y=305)

# Aktualisierung der Eingabe
login_window.mainloop()
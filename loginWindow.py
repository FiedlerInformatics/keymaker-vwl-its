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
import subprocess
import sys
import pickle
#############################
# ERSTELLEN DES KEY OBJECTS #
#############################
keyObject = Key()
for attr in keyObject.__dict__:
    setattr(keyObject, attr, None)
############################
login_window = tk.Tk()
login_window.geometry("700x433")
login_window.resizable(False,False)
login_window.title("Keymaker")
##############
# FUNKTIONEN #
##############
def getDataBase() -> None:
    keyObject.database_path = filedialog.askopenfilename(initialdir="/",title="Öffne die KeePass Datenbank", filetypes=[("KeePass Database Files","*kdbx")])
    if keyObject.database_path:
        database_entry.delete(0,tk.END)
        database_entry.insert(0,keyObject.database_path)
        print(keyObject.database_path)

def check_file_type(filepath, extension) -> bool:
    return Path(filepath).suffix.lower() == extension.lower()

def check_password() -> bool:
    try: pk= PyKeePass(database_entry.get(), password=password_entry.get())
    except pykeepass.exceptions.CredentialsError:
        return False
    return True

def login() -> None:
    if len(keyObject.database_path) == 0:
        error_message.config(text="Es wurde keine Datei ausgewählt", fg="red")
        print(keyObject.database_path)
    else:
        if not check_password():
            error_message.config(text="Falsches Passwort", fg="red")
            return
        else:       
            keyObject.password = password_entry.get()
            keyObject.database_path = database_entry.get()
            open_mainWindow()

def open_mainWindow() -> None:
   with open("keyObj.pickle", "wb") as f:
    pickle.dump(keyObject, f)
    f.close()
    subprocess.Popen(                             # Starten des Hauptfensters
        [sys.executable, "mainWindow.py"] ,
        creationflags=subprocess.CREATE_NO_WINDOW # Verhinderd das Öffnen eines Konsolenfensters
    )
    login_window.destroy()

style = ttk.Style()
style.theme_use("vista")
login_window.iconbitmap(default="keymaker_images/lockSymbol.ico")

image = ImageTk.PhotoImage(Image.open("keymaker_images/loginImage2.jpg")) # Bild am Rand 
image_label = ttk.Label(login_window, image=image)

keymakerHeader = ttk.Label(login_window,text="Keymaker",font="Helvetica 40 bold")
datenbankAuswahlMeldung = ttk.Label(login_window, text="Wählen Sie eine .kdbx-Datei", font="Helvetica")

error_message = tk.Label(login_window, text="")

browse_database = ttk.Button(text=".kdbx-Datei")
database_entry = ttk.Entry(login_window, width=50)

password_label = ttk.Label(login_window, text="Password", font="Helvetica 10")
password_entry = ttk.Entry(login_window, show="●", width=50)

login_button = ttk.Button(text="Anmelden", width=20)
#######################
# LAYOUT LOGIN WINDOW #
#######################
image_label.place(x=0,y=0)
keymakerHeader.place(x=365,y=40)
datenbankAuswahlMeldung.place(x=365,y=144)
error_message.place(x=440,y=185)

browse_database.place(x=340,y=215)
database_entry.place(x=340,y=245)

password_label.place(x=340,y=280)
password_entry.place(x=340, y=302)

login_button.place(x=430,y=357)

browse_database.configure(command=getDataBase)    # Konfiguration der Buttons
login_button.configure(command=login)

login_window.mainloop()                           # Aktualisierung der Eingabe

import mainWindow
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
import os
import pickle
import pyAesCrypt
import configparser

keyObject = Key()
for attr in keyObject.__dict__:
    setattr(keyObject, attr, None)

login_window = tk.Tk()
login_window.geometry("700x433")
login_window.resizable(False,False)
login_window.title("Keymaker")
########################################################

def resource_path(relative_path):
    """ Gibt den absoluten Pfad zur Ressource zurück, funktioniert für Entwicklung und PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def read_INI_path() -> str:
    config = configparser.ConfigParser()
    config.read('databasePath.ini')
    #databasepath = config['Path']['lastdatabasepath']
    #print("Database path from read_INI_path(): " + databasepath)
    if 'Path' not in config or 'lastdatabasepath' not in config['Path']:
        error_message.config(text="Falscher Dateipfad in .ini-Datei", fg="red")
        error_message.place(x=440,y=185)
    else:
        return  config['Path']['lastdatabasepath']

def getDataBase() -> None:
   
    keyObject.database_path = filedialog.askopenfilename(
        title= "Datenbank auswählen",
        filetypes=[("KeePass Database", "*.kdbx")]
   )
   # Lösche vorherige Eingabe
    database_entry.delete(0, tk.END)

    if keyObject.database_path:
        database_entry.insert(0, keyObject.database_path)
        database_entry.config(fg="black")
        error_message.config(text="")
    
    
def login() -> None:
    def checkPassword() -> bool:
        try: pk= PyKeePass(database_entry.get(), password=password_entry.get())
        except pykeepass.exceptions.CredentialsError:
                return False
        return True

    def write_INI_path(path:str) -> None:
        config = configparser.ConfigParser()
        config['Path'] = {'lastDatabasePath': path}
        with open('databasePath.ini', 'w+') as configfile:
            config.write(configfile)

    if len(keyObject.database_path) == 0:
        error_message.config(text="Es wurde keine Datei ausgewählt", fg="red")
        error_message.place(x=440,y=185)
    else:
        if not checkPassword():
            error_message.config(text="Falsches Passwort", fg="red")
            error_message.place(x=430,y=185)
            return
        else:
            keyObject.password = password_entry.get()
            keyObject.database_path = database_entry.get()
            write_INI_path(keyObject.database_path)
            open_mainWindow()

def check_password() -> bool:
    try: pk= PyKeePass(database_entry.get(), password=password_entry.get())
    except pykeepass.exceptions.CredentialsError:
        return False
    return True

############################################################
style = ttk.Style()
style.theme_use("vista")
login_window.iconbitmap(resource_path("keymaker_images/keymaker_logo.ico"))

image = ImageTk.PhotoImage(Image.open(resource_path("keymaker_images/loginImage2.jpg"))) # Bild am Rand 
image_label = ttk.Label(login_window, image=image)
image_label.image = image

keymakerHeader = ttk.Label(login_window,text="Keymaker",font="Helvetica 40 bold")
datenbankAuswahlMeldung = ttk.Label(login_window, text="Wählen Sie eine .kdbx-Datei", font="Helvetica")

error_message = tk.Label(login_window, text="", font="Helvetica 12", fg="red")

browse_database = ttk.Button(text=".kdbx-Datei")
database_entry = tk.Entry(login_window, width=50)

password_label = ttk.Label(login_window, text="Password", font="Helvetica 10")
password_entry = ttk.Entry(login_window, show="●", width=50)

login_button = ttk.Button(text="Anmelden", width=20)
############################################################
# LAYOUT LOGIN WINDOW #
############################################################
image_label.place(x=0,y=0)
keymakerHeader.place(x=365,y=40)
datenbankAuswahlMeldung.place(x=365,y=144)

browse_database.place(x=340,y=215)
database_entry.place(x=340,y=245)

password_label.place(x=340,y=280)
password_entry.place(x=340, y=302)

login_button.place(x=430,y=357)
##############
# FUNKTIONEN #
##############
def serialisation(kpo: Key) -> None:
    with open("keyObj.pickle", "wb") as f:
        pickle.dump(kpo, f)
        f.close()

def encrypt() -> None:
    password = "long-and-random-password"
    try:
        pyAesCrypt.encryptFile("keyObj.pickle", "keyObjPickle.aes", password, 64 * 1024)
    except FileNotFoundError as e:
        print(f"Encryption Error: {e}")

def open_mainWindow() -> None:
    login_window.destroy()
    mainWindow.openMainWindow(keyObject)
    
if os.path.isfile("databasePath.ini"):
    ini_path = read_INI_path()
    if ini_path and os.path.exists(ini_path):
        database_entry.config(fg="black")
        database_entry.delete(0, tk.END)
        database_entry.insert(0, ini_path)
        keyObject.database_path = ini_path
    else:
        error_message.place(x=385,y=185)
        if ini_path is None:
            error_message.config(text=".ini Datei enthält keinen Eintrag", fg="red")
        else:
            error_message.config(text=".ini Datei enthält falschen Eintrag", fg="red")
            database_entry.insert(0, ini_path)
            database_entry.config(fg="red")

        
browse_database.configure(command=getDataBase)    # Konfiguration der Buttons
login_button.configure(command=login)

login_window.mainloop()                          
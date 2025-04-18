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


INIpath = 'databasePath.ini' # Pfad zur INI-Datei
corruptDatabasePath = False

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
########################################################
def getDataBase() -> None:
    global corruptDatabasePath
    password_entry.delete(0, tk.END)  # Löschen des Passwortfeldes
    database_entry.delete(0, tk.END)  # Löschen des Datenbankpfad-Feldes

    if not os.path.isfile(INIpath):
        # Wenn keine INI-Datei vorhanden ist, öffne den Dateiauswahldialog
        keyObject.database_path = filedialog.askopenfilename(
            title="Datenbank auswählen",
            filetypes=[("KeePass Database", "*.kdbx")],
        )
        if keyObject.database_path:
            database_entry.insert(0, keyObject.database_path)
            database_entry.config(fg="black")
            error_message.config(text="")
            corruptDatabasePath = False
    else:
        try:
            databasepathFromINI = get_database_path()
        except Exception as e:
            error_message.config(text="Fehler beim Lesen der INI-Datei", fg="red")
            corruptDatabasePath = True
            return

        if os.path.isfile(databasepathFromINI):
            # Gültiger Pfad aus INI
            keyObject.database_path = databasepathFromINI
            database_entry.insert(0, databasepathFromINI)
            database_entry.config(fg="black")
            error_message.config(text="")
            corruptDatabasePath = False
        else:
            # Ungültiger Pfad -> Fehlermeldung & Dateiauswahl
            error_message.config(text="Dateipfad inkorrekt", fg="red")
            database_entry.insert(0, databasepathFromINI)
            database_entry.config(fg="red")
            corruptDatabasePath = True

            # --> Neue Auswahl ermöglichen
            new_path = filedialog.askopenfilename(
                title="Datenbank auswählen",
                filetypes=[("KeePass Database", "*.kdbx")],
            )
            if new_path:
                keyObject.database_path = new_path
                database_entry.delete(0, tk.END)
                database_entry.insert(0, new_path)
                database_entry.config(fg="black")
                error_message.config(text="")
                corruptDatabasePath = False
        
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
            write_INI(keyObject.database_path) # Speichern des Pfades in der INI-Datei
            open_mainWindow()

def get_database_path() -> str:
    config = configparser.ConfigParser()
    config.read(INIpath)
    if 'Path' not in config or 'lastDatabasePath' not in config['Path']:
        raise ValueError("Path section not found in the config file.") 
    return config['Path']['lastDatabasePath']

def write_INI(path:str) -> None:
    config = configparser.ConfigParser()
    config['Path'] = {'lastDatabasePath': path}
    with open(INIpath, 'w') as configfile:
        config.write(configfile)



def check_password() -> bool:
    try: pk= PyKeePass(database_entry.get(), password=password_entry.get())
    except pykeepass.exceptions.CredentialsError:
        return False
    return True

############################################################
style = ttk.Style()
style.theme_use("vista")
login_window.iconbitmap(default="keymaker_images/lockSymbol.ico")

image = ImageTk.PhotoImage(Image.open("keymaker_images/loginImage2.jpg")) # Bild am Rand 
image_label = ttk.Label(login_window, image=image)

keymakerHeader = ttk.Label(login_window,text="Keymaker",font="Helvetica 40 bold")
datenbankAuswahlMeldung = ttk.Label(login_window, text="Wählen Sie eine .kdbx-Datei", font="Helvetica")

error_message = tk.Label(login_window, text="", font="Helvetica 12", fg="red")

browse_database = ttk.Button(text=".kdbx-Datei")
database_entry = tk.Entry(login_window, width=50)

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
    serialisation(keyObject) # Serialisierung des KeyObjects
    encrypt()               # Verschlüsselung der pickle-Datei
    os.remove("keyObj.pickle")
    subprocess.Popen(                             # Starten des Hauptfensters
        [sys.executable, "mainWindow.py"] ,
        creationflags=subprocess.CREATE_NO_WINDOW # Verhinderd das Öffnen eines Konsolenfensters
    )
    write_INI(database_entry.get()) # Speichern des Pfades in der INI-Datei
    login_window.destroy()

# Überprüfen, ob die INI-Datei existiert und den Pfad auslesen

if os.path.isfile(INIpath):
    # Überprüfen, ob der Pfad in der INI-Datei gültig ist
    databasepath = get_database_path()
    if os.path.isfile(databasepath):
        keyObject.database_path = get_database_path()
        database_entry.insert(0, databasepath) # Einfügen des Pfades in das Entry-Feld
    else:
        error_message.config(text="Dateipfad inkorrekt", fg="red")
        database_entry.insert(0,databasepath)
        database_entry.config(fg="red")
        corruptDatabasePath = True
# Überprüfen, ob er Dateipfad korrigiert wurde

        
browse_database.configure(command=getDataBase)    # Konfiguration der Buttons
login_button.configure(command=login)

login_window.mainloop()                          

import mainWindow
from mainWindow import resource_path
from keepassObject import Key
from loginWindowGUI import LOGIN

import pykeepass.exceptions
from tkinter import *
import tkinter as tk
from tkinter import ttk, filedialog
import pykeepass
from pykeepass import PyKeePass
import os
import pickle
import configparser

keyObject = Key()
for attr in keyObject.__dict__:
    setattr(keyObject, attr, None)

loginwindow_obj = LOGIN()

########################################################

def read_INI_path() -> str:
    config = configparser.ConfigParser()
    config.read('databasePath.ini')
    if 'Path' not in config or 'lastdatabasepath' not in config['Path']:
        loginwindow_obj.error_message.config(text="Falscher Dateipfad in .ini-Datei", fg="red")
        loginwindow_obj.error_message.place(x=440,y=185)
    else:
        return  config['Path']['lastdatabasepath']

def getDataBase() -> None:
   
    keyObject.database_path = filedialog.askopenfilename(
        title= "Datenbank auswählen",
        filetypes=[("KeePass Database", "*.kdbx")]
   )
   # Lösche vorherige Eingabe
    loginwindow_obj.database_entry.delete(0, tk.END)

    if keyObject.database_path:
        loginwindow_obj.database_entry.insert(0, keyObject.database_path)
        loginwindow_obj.database_entry.config(fg="black")
        loginwindow_obj.error_message.config(text="")
    
    
def login() -> None:
    def checkPassword() -> bool:
        try: pk= PyKeePass(loginwindow_obj.database_entry.get(), password=loginwindow_obj.password_entry.get())
        except pykeepass.exceptions.CredentialsError:
                return False
        return True

    def write_INI_path(path:str) -> None:
        config = configparser.ConfigParser()
        config['Path'] = {'lastDatabasePath': path}
        with open('databasePath.ini', 'w+') as configfile:
            config.write(configfile)

    if len(keyObject.database_path) == 0:
        loginwindow_obj.error_message.config(text="Es wurde keine Datei ausgewählt", fg="red")
        loginwindow_obj.error_message.place(x=440,y=185)
    else:
        if not checkPassword():
            loginwindow_obj.error_message.config(text="Falsches Passwort", fg="red")
            loginwindow_obj.error_message.place(x=430,y=185)
            return
        else:
            keyObject.password = loginwindow_obj.password_entry.get()
            keyObject.database_path = loginwindow_obj.database_entry.get()
            write_INI_path(keyObject.database_path)
            open_mainWindow()

def check_password() -> bool:
    try: pk= PyKeePass(loginwindow_obj.database_entry.get(), password=loginwindow_obj.password_entry.get())
    except pykeepass.exceptions.CredentialsError:
        return False
    return True

def serialisation(kpo: Key) -> None:
    with open("keyObj.pickle", "wb") as f:
        pickle.dump(kpo, f)
        f.close()

def open_mainWindow() -> None:
    loginwindow_obj.login_window.destroy()
    mainWindow.openMainWindow(keyObject)
    
if os.path.isfile("databasePath.ini"):
    ini_path = read_INI_path()
    if ini_path and os.path.exists(ini_path):
        loginwindow_obj.database_entry.config(fg="black")
        loginwindow_obj.database_entry.delete(0, tk.END)
        loginwindow_obj.database_entry.insert(0, ini_path)
        keyObject.database_path = ini_path
    else:
        loginwindow_obj.error_message.place(x=385,y=185)
        if ini_path is None:
            loginwindow_obj.error_message.config(text=".ini Datei enthält keinen Eintrag", fg="red")
        else:
            loginwindow_obj.error_message.config(text=".ini Datei enthält falschen Eintrag", fg="red")
            loginwindow_obj.database_entry.insert(0, ini_path)
            loginwindow_obj.database_entry.config(fg="red")

        
loginwindow_obj.browse_database.configure(command=getDataBase)    # Konfiguration der Buttons
loginwindow_obj.login_button.configure(command=login)

loginwindow_obj.login_window.mainloop()                          
#from mainWindow import resource_path
import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk, Image

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class LOGIN():

    login_window = tk.Tk()
    login_window.geometry("700x433")
    login_window.resizable(False,False)    
    login_window.title("keymaker")

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
    
    image_label.place(x=0,y=0)
    keymakerHeader.place(x=365,y=40)
    datenbankAuswahlMeldung.place(x=365,y=144)
    browse_database.place(x=340,y=215)
    database_entry.place(x=340,y=245)
    password_label.place(x=340,y=280)
    password_entry.place(x=340, y=302)
    login_button.place(x=430,y=357)


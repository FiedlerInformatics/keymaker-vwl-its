from keepassObject import Key
import tkinter as tk
from tkinter import ttk
import pykeepass as pykp
from pathlib import Path
from PIL import ImageTk, Image

# Create main window
login_window = tk.Tk()
login_window.geometry("700x433")
login_window.resizable(False, False)
login_window.title("Keymaker")

# Apply a Tkinter theme
style = ttk.Style()
style.theme_use("vista")  # Change this to 'clam', 'alt', 'classic', etc.

# Load image
image = ImageTk.PhotoImage(Image.open("loginImage.jpg"))
image_label = ttk.Label(login_window, image=image)  # CHANGED TO ttk.Label

# Use ttk.Label instead of tk.Label
keymakerHeader = ttk.Label(login_window, text="Keymaker", font="Helvetica 40 bold")
datenbankAuswahlMeldung = ttk.Label(login_window, text="Wählen Sie eine .kdbx-Datei", font="Helvetica")
error_message = ttk.Label(login_window, text="")

# Use ttk.Button instead of tk.Button
browse_database = ttk.Button(login_window, text=".kdbx-Datei")
database_entry = ttk.Entry(login_window, width=50)  # CHANGED TO ttk.Entry

password_label = ttk.Label(login_window, text="Password", font="Helvetica")
password_entry = ttk.Entry(login_window, show="●", width=50)  # CHANGED TO ttk.Entry

login_button = ttk.Button(login_window, text="Anmelden", width=20)  # CHANGED TO ttk.Button

# Layout login_window
image_label.place(x=0, y=0)
keymakerHeader.place(x=355, y=40)
datenbankAuswahlMeldung.place(x=380, y=144)
error_message.place(x=400, y=180)

browse_database.place(x=340, y=210)
database_entry.place(x=340, y=245)

password_label.place(x=340, y=280)
password_entry.place(x=340, y=305)

login_button.place(x=340, y=340)

# Start application
login_window.mainloop()

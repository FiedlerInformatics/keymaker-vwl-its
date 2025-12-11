from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk
from helper import resource_path

class WARNING(ABC):

    def __init__(self):

        if type(self) is WARNING:
            raise TypeError("WARNING abstract class darf nicht direkt instanziiert werden.")

        self.warning_window = tk.Tk()
        self.warning_window.geometry("700x433")
        self.warning_window.resizable(False,False)
        self.warning_window.title("keymaker")
        self.style = ttk.Style()
        self.style.theme_use("vista")
        self.warning_window.iconbitmap(resource_path("keymaker_images/keymaker_logo.ico"))
        
        self.warning_window.grid_columnconfigure(0, weight=1, minsize=350)
        self.warning_window.grid_columnconfigure(1,weight=1,minsize=350)
        self.warning_window.grid_rowconfigure(0, minsize=216)
        self.warning_window.grid_rowconfigure(1, minsize=217)
        # Obere Textzeile
        self.warning_text = ttk.Label(self.warning_window,justify="center", font="Helvetica 12")
        self.warning_text.grid(row=0, column=0, columnspan=2, sticky="n", pady=80)
        # Linker Button
        self.button_verwerfen = ttk.Button(self.warning_window, text="Verwerfen", width=10)
        self.button_verwerfen.grid(row=1, column=0, pady=50)
        # Rechter Button
        self.button_ueberschreiben = ttk.Button(self.warning_window, text="Überschreiben")
        self.button_ueberschreiben.grid(row=1, column=1, pady=50, ipadx=10)

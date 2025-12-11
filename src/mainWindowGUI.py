# from mainWindow import resource_path
import tkinter as tk
from tkinter import IntVar
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
import pykeepass
from pykeepass import PyKeePass
from datetime import date
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MAIN:

    def __init__(self, lehrstuhlLst, entriesLst):
        """
        Initializes the main window GUI for the Keymaker application.
        Args:
            lehrstuhlLst (list[str]): List of available "Lehrstuhl" (departments/chairs) for selection in the GUI.
            entriesLst (list[str]): List of existing database entries for selection in the GUI.
        Attributes:
            lehrstuhlLst (list[str]): Stores the list of Lehrstuhl options.
            entriesLst (list[str]): Stores the list of database entries.
            main_window (tk.Tk): The main Tkinter window instance.
            createKey_symbol, printKey_symbol, key_symbol, calendar_symbol, person_symbol, lehrstuhl_symbol, id_symbol, geraet_symbol, hiwi_symbol, seriennummer_symbol, inventarnummer_symbol (ImageTk.PhotoImage): Image assets for GUI elements.
            create_key_windowButton, print_key_windowButton (ttk.Label): Sidebar navigation buttons.
            trennlinie (tk.Frame): Visual separator in the layout.
            browse_txt (ttk.Button): Button to browse for .txt files.
            txt_entry (tk.Entry): Entry field for .txt file path.
            person_label, geraet_label, lehrstuhl_label, seriennummer_label, datum_label, inventarnummer_label, hilfskraft_label, bitlocker_key_label, bitlocker_bezeichner_label (tk.Label/ttk.Label): Labels for form fields.
            person_input, geraet_input, lehrstuhl_input, seriennummer_input, datum_input, inventarnummer_input, hilfskraft_input, bitlocker_key_input, bitlocker_bezeichner_input (tk.Entry/ttk.Entry/ttk.Combobox): Input fields for form data.
            lehrstuhl_var (tk.StringVar): Variable for Lehrstuhl combobox selection.
            create_pdf_checkButton_bool (tk.IntVar): State variable for PDF creation checkbox.
            create_pdf_checkButton (tk.Checkbutton): Checkbox to enable/disable PDF creation.
            mainWindow_error, mainWindow_success (tk.Label): Labels for displaying error/success messages.
            create_key_button (ttk.Button): Button to trigger key creation.
            entrieset_var (tk.StringVar): Variable for database entries dropdown.
            database_entries_dropdown (ttk.Combobox): Dropdown for selecting existing database entries.
            print_key_button (ttk.Button): Button to trigger PDF creation for selected entry.
            printKey_window_success, printKey_window_error (tk.Label): Labels for displaying print window messages.
            createKey_windowsLayout (dict): Layout configuration for widgets in the create key window.
        Note:
            This class sets up the main window, loads all required images, initializes all widgets, and arranges them using a grid layout.
        """
        self.lehrstuhlLst = lehrstuhlLst
        self.entriesLst = entriesLst

        self.main_window = tk.Tk()
        self.main_window.geometry("900x700")
        self.main_window.minsize(900,700)
        self.main_window.title("Keymaker")
        style = ttk.Style(self.main_window)
        style.theme_use("vista")
        self.main_window.iconbitmap(resource_path("keymaker_images/keymaker_logo.ico"))

        self.createKey_symbol = ImageTk.PhotoImage(Image.open(resource_path('keymaker_images/createkeySymbol.png')))
        self.printKey_symbol = ImageTk.PhotoImage(Image.open(resource_path('keymaker_images/printKeySymbol.png')))
        self.key_symbol = ImageTk.PhotoImage(Image.open(resource_path('keymaker_images/keySymbol.png')))
        self.calendar_symbol = ImageTk.PhotoImage(Image.open(resource_path('keymaker_images/calendarSymbol.png')))
        self.person_symbol = ImageTk.PhotoImage(Image.open(resource_path('keymaker_images/userSymbol.png')))
        self.lehrstuhl_symbol = ImageTk.PhotoImage(Image.open(resource_path('keymaker_images/lehrstuhlSymbol.png')))
        self.id_symbol = ImageTk.PhotoImage(Image.open(resource_path('keymaker_images/idSymbol.png')))
        self.geraet_symbol = ImageTk.PhotoImage(Image.open(resource_path('keymaker_images/geraetSymbol.png')))
        self.hiwi_symbol = ImageTk.PhotoImage(Image.open(resource_path('keymaker_images/hiwiSymbol.png')))
        self.seriennummer_symbol = ImageTk.PhotoImage(Image.open(resource_path('keymaker_images/seriennummerSymbol.png')))
        self.inventarnummer_symbol = ImageTk.PhotoImage(Image.open(resource_path('keymaker_images/ivnSymbol.png')))

        self.create_key_windowButton = ttk.Label(self.main_window,text="Key erstellen",image=self.createKey_symbol,compound='left', font="Helvetica 12 bold", cursor="hand2")
        self.print_key_windowButton = ttk.Label(self.main_window,text="Key drucken", image=self.printKey_symbol, compound='left', font="Helvetica 12", cursor="hand2")
        self.trennlinie = tk.Frame(self.main_window,bg='grey',width=1)
        self.browse_txt = ttk.Button(self.main_window, text=".txt-Datei")
        self.txt_entry = tk.Entry(self.main_window, font=("Helvetica 12"))
        self.person_label = tk.Label(self.main_window,text="Person",image=self.person_symbol,compound='left',font="Helvetica 12")
        self.person_input = tk.Entry(self.main_window, font=("Helvetica 12"))
        self.geraet_label = tk.Label(self.main_window,text="Gerät", image=self.geraet_symbol, compound='left', font="Helvetica 12")
        self.geraet_input = tk.Entry(self.main_window,font=("Helvetica 12"))
        self.lehrstuhl_label = tk.Label(self.main_window, text="Lehrstuhl",image=self.lehrstuhl_symbol,compound='left',font="Helvetica 12")
        self.lehrstuhl_var = tk.StringVar()
        self.lehrstuhl_input = ttk.Combobox(self.main_window, textvariable=self.lehrstuhl_var,values= lehrstuhlLst, font=("Helvetica", 12))
        self.lehrstuhl_input.set("Lehrstuhl auswählen") # Setzen des Standardwerts auf "Lehrstuhl auswählen"
        self.seriennummer_label = tk.Label(self.main_window, text="Seriennummer",image=self.seriennummer_symbol, compound='left',font="Helvetica 12")
        self.seriennummer_input = ttk.Entry(self.main_window, font=("Helvetica 12"))
        self.datum_label = tk.Label(self.main_window, text="Datum",image=self.calendar_symbol, compound='left', font="Helvetica 12")
        self.datum_input = ttk.Entry(self.main_window, font=("Helvetica 12"))
        self.datum_input.insert(0,date.today().strftime("%d.%m.%Y")) # Setzen des Datums auf das heutige Datum
        self.inventarnummer_label = ttk.Label(self.main_window, text="Inventarnummer",image=self.inventarnummer_symbol, compound='left',  font="Helvetica 12 ")
        self.inventarnummer_input = ttk.Entry(self.main_window, font=("Helvetica 12"))
        self.hilfskraft_label = tk.Label(self.main_window, text="Hilfskraft", image=self.hiwi_symbol, compound='left', font="Helvetica 12")
        self.hilfskraft_input = ttk.Entry(self.main_window, font=("Helvetica 12"))
        self.bitlocker_key_label = tk.Label(self.main_window, text="Bitlocker Key",image=self.key_symbol, compound='left', font="Helvetica 12")
        self.bitlocker_key_input = ttk.Entry(self.main_window, font=("Helvetica 12"))
        self.bitlocker_bezeichner_label = tk.Label(self.main_window, text="Bitlocker Bezeichner",image=self.id_symbol, compound='left', font="Helvetica 12")
        self.bitlocker_bezeichner_input = ttk.Entry(self.main_window, font=("Helvetica 12"))
        self.create_pdf_checkButton_bool = IntVar(value=1)  # Set default state to checked
        self.create_pdf_checkButton = tk.Checkbutton(self.main_window, text="PDF erstellen", font="Helvetica 12", variable=self.create_pdf_checkButton_bool)
        self.mainWindow_error = tk.Label(self.main_window, text="", font="Helvetica 12", fg="red", width=35, anchor="center",justify= 'center')
        self.mainWindow_success = tk.Label(self.main_window, text="", font="Helvetica 12", fg="green", width=35, anchor="center",justify= 'center')
        self.create_key_button = ttk.Button(self.main_window, text="Key erstellen")

        self.entrieset_var = tk.StringVar()
        self.database_entries_dropdown = ttk.Combobox(self.main_window, textvariable=self.entrieset_var, values= entriesLst , font=("Helvetica", 12))
        self.database_entries_dropdown.set("Key auswählen")
        self.print_key_button = ttk.Button(self.main_window, text="PDF erstellen")
        self.printKey_window_success = tk.Label(self.main_window, text="", font="Helvetica 12", fg="green", width=35, anchor="center",justify= 'center')
        self.printKey_window_error = tk.Label(self.main_window, text="", font="Helvetica 12", fg="red", width=35, anchor="center",justify= 'center')

        for col in [0, 1, 2, 4]:
            self.main_window.columnconfigure(col, weight=1)
        for col in (1, 3):
            self.main_window.columnconfigure(col, weight=3)
        for row in range(17):
            self.main_window.rowconfigure(row, weight=1)

        # CRUCIAL!
        self.main_window.columnconfigure(0, minsize=190, weight=0) 

        self.create_key_windowButton.grid(column=0,row=1,sticky='w',padx=(10,5))
        self.print_key_windowButton.grid(column=0,row=2,sticky='w',padx=(10,5))
        self.trennlinie.grid(row=0,column=0,sticky="nes",rowspan=21,padx=10)

        self.createKey_windowsLayout = {
            self.browse_txt: {"row": 1, "column": 1, "sticky": 'wn', "padx": (20, 0)},
            self.txt_entry: {"row": 1, "column": 1, "sticky": 'wes', "columnspan": 3, "padx": (20, 20)},
            self.person_label: {"row": 3, "column": 1, "sticky": 'wn', "padx": (20, 0)},
            self.person_input: {"row": 3, "column": 1, "sticky": 'wes', "padx": (20, 0)},
            self.geraet_label: {"row": 3, "column": 3, "sticky": 'wn', "padx": (0, 20)},
            self.geraet_input: {"row": 3, "column": 3, "sticky": 'wes', "padx": (0, 20)},
            self.lehrstuhl_label: {"row": 5, "column": 1, "sticky": 'wn', "padx": (20, 0)},
            self.lehrstuhl_input: {"row": 5, "column": 1, "sticky": 'wes', "padx": (20, 0)},
            self.seriennummer_label: {"row": 5, "column": 3, "sticky": 'wn', "padx": (0, 20)},
            self.seriennummer_input: {"row": 5, "column": 3, "sticky": 'wes', "padx": (0, 20)},
            self.datum_label: {"row": 7, "column": 1, "sticky": 'wn', "padx": (20, 0)},
            self.datum_input: {"row": 7, "column": 1, "sticky": 'wes', "padx": (20, 0)},
            self.inventarnummer_label: {"row": 7, "column": 3, "sticky": 'wn', "padx": (0, 20)},
            self.inventarnummer_input: {"row": 7, "column": 3, "sticky": 'wes', "padx": (0, 20)},
            self.hilfskraft_label: {"row": 9, "column": 1, "sticky": 'wn', "padx": (20, 0)},
            self.hilfskraft_input: {"row": 9, "column": 1, "sticky": 'wes', "padx": (20, 0)},
            self.bitlocker_bezeichner_label: {"row": 11, "column": 1, "sticky": 'wn', "padx": (20, 20)},
            self.bitlocker_bezeichner_input: {"row": 11, "column": 1, "sticky": 'wes', "columnspan": 3, "padx": (20, 20)},
            self.bitlocker_key_label: {"row": 13, "column": 1, "sticky": 'wn', "padx": (20, 20)},
            self.bitlocker_key_input: {"row": 13, "column": 1, "sticky": 'wes', "columnspan": 3, "padx": (20, 20)},
            self.create_pdf_checkButton: {"row": 15, "column": 1, "sticky": 'wn', "padx": (20, 0)},
            self.mainWindow_error: {"row": 16, "column": 1, "sticky": 'new', 'columnspan': 5, "padx": (0,0)},
            self.mainWindow_success: {"row": 16, "column": 1, "sticky": 'new', 'columnspan': 5, "padx": (0,0)},
            self.create_key_button: {"row": 15, "column": 3, "sticky": 'en', "padx": (0, 20)},
        }
        for widget, layout in self.createKey_windowsLayout.items():
            widget.grid(**layout)
            

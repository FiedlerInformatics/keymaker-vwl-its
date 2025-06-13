from mainWindowGUI import MAIN
from keepassObject import Key
from warning_inventar import WARNING_INVENTAR
from warning_inventar_seriennummer import WARNING_INVENTAR_SERIENNUMMER
from warningSeriennummer import WARNING_SERIENNUMMER

from helper import resource_path
import pykeepass.exceptions
from keepassObject import Key
from tkinter import *
import tkinter as tk
from tkinter import ttk, filedialog
import pykeepass
from pykeepass import PyKeePass
from pathlib import Path
from PIL import ImageTk, Image
import os
import re
import sys
from io import StringIO
from datetime import date
from ctypes import windll
from configparser import ConfigParser
from fpdf import FPDF
from pathlib import Path
from barcode.writer import SVGWriter
from createPDF import PDF

def create_lehrstuhlLst(PyKeePass) -> list[str]:
    """Returns a List of all subdirectories of the 'General' directory"""
    regex = r'General/Bitlocker/.*'
    strLst = []
    for i in range(len(PyKeePass.groups)): 
        strVar = str(PyKeePass.groups[i]).replace('Group: ', '').replace('"','')
        if re.match(regex, strVar): 
            strLst.append(strVar.replace('General/Bitlocker/', ''))
    return strLst

def create_entriesLst(PyKeePass) -> list[str]:
    regex = r'General/Bitlocker/.*'
    strLst = []
    for i in range(len(PyKeePass.entries)): 
        strVar = str(PyKeePass.entries[i]).replace('Entry: ', '').replace('"','')
        if re.match(regex, strVar): 
            strLst.append(strVar.replace('(None)', ''))
    for i in range (len(strLst)):
        strLst[i] = re.sub(r"[\(\[].*?[\)\]]", "", strLst[i]).strip()
    return strLst

def openMainWindow(keyObject:Key):

    def create_entriesDict() -> dict[str, dict[str, str]]:
        """Returns a nested dictionary: [Titel,[Seriennummer, Inventarisierungsnummer]]"""
        entrdic = {}
        entrLst = create_entriesLst(database)
        for entry_path in entrLst:
            entry_title = os.path.basename(entry_path) # Enfernt die Dateipfade der Einträge
            entry = database.find_entries(title=entry_title, first=True)
            if entry:
                entrdic[entry_title] = {
                    "Seriennummer": entry.get_custom_property("Seriennummer") or "",
                    "Inventarisierungsnummer": entry.get_custom_property("Inventarisierungsnummer") or ""
                }
        return entrdic

    database = PyKeePass(keyObject.database_path, keyObject.password)
    mainWindow_obj = MAIN(create_lehrstuhlLst(database), create_entriesLst(database))
    entryDict = create_entriesDict()

    # https://stackoverflow.com/questions/77840560/why-opacity-in-tkinter-widgets-not-supported
    def set_opacity(widget, value: float):
        """0 = transparent | 1 = opaque"""
        widget = widget.winfo_id()
        value = int(255*value) # value from 0 to 1
        wnd_exstyle = windll.user32.GetWindowLongA(widget, -20)
        new_exstyle = wnd_exstyle | 0x00080000  
        windll.user32.SetWindowLongA(widget, -20, new_exstyle)  
        windll.user32.SetLayeredWindowAttributes(widget, 0, value, 2)

    def remove_createKey_window() -> None:
        for widget in mainWindow_obj.createKey_windowsLayout.keys():
            set_opacity(widget,0)

    def remove_createKey_window() -> None:
        set_opacity(mainWindow_obj.browse_txt, 0)
        set_opacity(mainWindow_obj.txt_entry, 0)
        set_opacity(mainWindow_obj.person_input, 0)
        set_opacity(mainWindow_obj.person_label, 0)
        set_opacity(mainWindow_obj.geraet_input, 0)
        set_opacity(mainWindow_obj.geraet_label, 0)
        set_opacity(mainWindow_obj.lehrstuhl_input, 0)
        set_opacity(mainWindow_obj.lehrstuhl_label, 0)
        set_opacity(mainWindow_obj.seriennummer_input, 0)
        set_opacity(mainWindow_obj.datum_input, 0)
        set_opacity(mainWindow_obj.datum_label, 0)
        set_opacity(mainWindow_obj.seriennummer_label, 0)
        set_opacity(mainWindow_obj.inventarnummer_input, 0)
        set_opacity(mainWindow_obj.inventarnummer_label, 0)
        set_opacity(mainWindow_obj.hilfskraft_input, 0)
        set_opacity(mainWindow_obj.hilfskraft_label, 0)
        set_opacity(mainWindow_obj.bitlocker_bezeichner_input, 0)
        set_opacity(mainWindow_obj.bitlocker_bezeichner_label, 0)
        set_opacity(mainWindow_obj.bitlocker_key_input, 0)
        set_opacity(mainWindow_obj.bitlocker_key_label, 0)
        set_opacity(mainWindow_obj.create_pdf_checkButton, 0)
        set_opacity(mainWindow_obj.create_key_button, 0)

    def show_createKey_window() -> None:
        set_opacity(mainWindow_obj.browse_txt, 1)
        set_opacity(mainWindow_obj.txt_entry, 1)
        set_opacity(mainWindow_obj.person_input, 1)
        set_opacity(mainWindow_obj.person_label, 1)
        set_opacity(mainWindow_obj.geraet_input, 1)
        set_opacity(mainWindow_obj.geraet_label, 1)
        set_opacity(mainWindow_obj.lehrstuhl_input, 1)
        set_opacity(mainWindow_obj.lehrstuhl_label, 1)
        set_opacity(mainWindow_obj.seriennummer_input, 1)
        set_opacity(mainWindow_obj.datum_input, 1)
        set_opacity(mainWindow_obj.datum_label, 1)
        set_opacity(mainWindow_obj.seriennummer_label, 1)
        set_opacity(mainWindow_obj.inventarnummer_input, 1)
        set_opacity(mainWindow_obj.inventarnummer_label, 1)
        set_opacity(mainWindow_obj.hilfskraft_input, 1)
        set_opacity(mainWindow_obj.hilfskraft_label, 1)
        set_opacity(mainWindow_obj.bitlocker_bezeichner_input, 1)
        set_opacity(mainWindow_obj.bitlocker_bezeichner_label, 1)
        set_opacity(mainWindow_obj.bitlocker_key_input, 1)
        set_opacity(mainWindow_obj.bitlocker_key_label, 1)
        set_opacity(mainWindow_obj.create_pdf_checkButton, 1)
        set_opacity(mainWindow_obj.create_key_button, 1)

    def printKey_window() -> None:
        database_entries_dropdown.grid(row=1, column=1, sticky='we',padx=(20, 0))
        print_key_button.grid(row=2, column=1, sticky='sw',padx=(20,0))
        printKey_window_success.grid(row=16, column=1, sticky='new', padx=(0, 0))  # <-- Zeigt pos Meldung im Keywindow
        printKey_window_error.grid(row=16, column=1, sticky='new', padx=(0, 0))  # <-- Zeigt neg Meldung im Keywindow
        set_opacity(print_key_button,1)
        mainWindow_obj.create_key_windowButton.config(font="Helvetica 12")
        mainWindow_obj.print_key_windowButton.config(font="Helvetica 12 bold")
        remove_createKey_window()
        for widget in mainWindow_obj.createKey_windowsLayout.keys():
            set_opacity(widget, 0)
    
    def createKey_window() -> None:
        database_entries_dropdown.grid_remove()
        set_opacity(print_key_button,0)
        mainWindow_obj.create_key_windowButton.config(font="Helvetica 12 bold")
        mainWindow_obj.print_key_windowButton.config(font="Helvetica 12")
        database_entries_dropdown.set("Key auswählen")
        show_createKey_window()

        for createWindow_widget in mainWindow_obj.createKey_windowsLayout.keys():
            set_opacity(createWindow_widget, 1)
        
    def check_input_completeness() -> bool:
        """Checks if all input fields except 'Inventarisierungsnummer' are set by the user.<br>If so returns True, else False and changes the color of the input fields to red as a side effect"""
        if len(mainWindow_obj.txt_entry.get()) == 0 or len(mainWindow_obj.person_input.get()) == 0 or len(mainWindow_obj.geraet_input.get())== 0 or mainWindow_obj.lehrstuhl_input.get() == "Lehrstuhl auswählen" or len(mainWindow_obj.seriennummer_input.get()) == 0 or len(mainWindow_obj.datum_input.get()) == 0 or len(mainWindow_obj.hilfskraft_input.get()) == 0:
            for label in [mainWindow_obj.person_label, mainWindow_obj.geraet_label, mainWindow_obj.lehrstuhl_label, mainWindow_obj.seriennummer_label, mainWindow_obj.hilfskraft_label, mainWindow_obj.datum_label, mainWindow_obj.bitlocker_bezeichner_label, mainWindow_obj.bitlocker_key_label]:
                label.config(fg="red")
            return False
        else:
            mainWindow_obj.mainWindow_error.config(text="")
            set_opacity(mainWindow_obj.mainWindow_error,0)
            return True
    
    def print_key() -> None:
        """Reads the entry path user input from the drop-down menu and creates a PDF with it"""
        entryString = database_entries_dropdown.get()
        if entryString != "Key auswählen":
            entryString = os.path.basename(entryString) # Entfernt die Dateipfade der Einträge
            entry = database.find_entries(title=entryString, first=True)
            keyObject.user = entry.get_custom_property("Name") or ""
            keyObject.geraet = entry.get_custom_property("Gerät") or ""
            keyObject.lehrstuhl = entry.get_custom_property("Lehrstuhl") or ""
            keyObject.serienNummer = entry.get_custom_property("Seriennummer") or ""
            keyObject.date = entry.get_custom_property("Datum") or ""
            keyObject.ivs = entry.get_custom_property("Inventarisierungsnummer") or ""
            keyObject.hiwi = entry.get_custom_property("Hilfskraft") or ""
            keyObject.id = entry.get_custom_property("Bezeichner") or ""
            keyObject.key = entry.get_custom_property("Wiederherstellungsschluessel") or ""
            try:
                txt_to_pdf(keyObject)
                set_opacity(printKey_window_error,0)
                printKey_window_success.config(text="PDF wurde erstellt")
            except Exception as e:
                set_opacity(printKey_window_success,0)
                printKey_window_error.config(text=f"Fehler beim Erstellen des PDFs: {e}")
                print(f"Error: {e}")

    # Entferne alle Eingaben aus den Inputfeldern des main windows
    def clear_mainWindow_inputFields() -> None:
        mainWindow_obj.person_input.delete(0, tk.END)
        mainWindow_obj.geraet_input.delete(0, tk.END)
        mainWindow_obj.seriennummer_input.delete(0, tk.END)
        mainWindow_obj.hilfskraft_input.delete(0, tk.END)
        mainWindow_obj.inventarnummer_input.delete(0, tk.END)
        mainWindow_obj.lehrstuhl_input.set("Lehrstuhl auswählen")
        mainWindow_obj.bitlocker_key_input.delete(0, tk.END)
        mainWindow_obj.bitlocker_bezeichner_input.delete(0, tk.END)
        mainWindow_obj.txt_entry.delete(0, tk.END)
        mainWindow_obj.mainWindow_error.config(text="")
        mainWindow_obj.mainWindow_success.config(text="")


    def getKeyTxtFile() -> None:
        """Opens a filedialog to choose and check a valid .txt-Bitlocker key"""
        clear_mainWindow_inputFields() # Löschen der Eingaben im main window
        keyObject.txt_path = filedialog.askopenfilename(initialdir="/",title="Öffne die .txt-Datei", filetypes=[("Text Files","*txt")])
        if keyObject.txt_path:
            # Löschen des Eintrags im Textfeld
            mainWindow_obj.txt_entry.delete(0,tk.END)
            try:
                keyObject.id, keyObject.key = extract_ID_KEY(remove_CRLF(keyObject.txt_path))
                # Einfügen des Pfades, id und des Keys in die Textfelder
                mainWindow_obj.txt_entry.insert(0,keyObject.txt_path)
                mainWindow_obj.txt_entry.config(fg="black")
                mainWindow_obj.bitlocker_bezeichner_input.insert(0,keyObject.id)
                mainWindow_obj.bitlocker_bezeichner_input.config(state="disabled") # Blocking manual input
                mainWindow_obj.bitlocker_key_input.insert(0,keyObject.key)
                mainWindow_obj.bitlocker_key_input.config(state="disabled")  # Blocking manual input
            except TypeError as e:
                # Ausgeben der Fehlermeldung im Textfeld 
                mainWindow_obj.txt_entry.insert(0, "kein gültiger Key" + str(e))
                mainWindow_obj.txt_entry.config(fg="red")
    
    def extract_ID_KEY(file) -> tuple:
        """Returns the identifier- and recovery string from the bitlocker .txt file<br>TypeError of None is found."""
        content = file.read()
        identifier_pattern = r"[A-Z0-9]{8}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}"
        recovery_key_pattern = r"[0-9]{6}-[0-9]{6}-[0-9]{6}-[0-9]{6}-[0-9]{6}-[0-9]{6}-[0-9]{6}-[0-9]{6}"

        identifierMatchObj = re.search(identifier_pattern, content)
        identifier = identifierMatchObj.group() if identifierMatchObj else None

        recovery_keyMatchObj = re.search(recovery_key_pattern, content)
        recovery_key = recovery_keyMatchObj.group() if recovery_keyMatchObj else None

        if identifier is None:
            raise TypeError("TypeError: No Identifier found")
        elif recovery_key is None:
            raise TypeError("TypeError: No Bitlocker-key found")
        else: 
            return identifier, recovery_key

    def remove_CRLF(file_path) -> StringIO:
        """CRUCIAL! Removes special charcters in the original bitlocker txt file."""
        with open(file_path, "r") as file:
            content = file.read()
            clean_content = content.replace('\r', '')
            clean_content = ''.join(filter(lambda x: x.isprintable() or x == '\n', clean_content))
            file_curr = StringIO()
            file_curr.write(clean_content)
            file_curr.seek(0)
        return file_curr

    def get_fieldInputs() -> None:
        """Reads strings from the input fields and stores them in the attributes of the Key object."""
        keyObject.txt_path = mainWindow_obj.txt_entry.get()
        keyObject.user = mainWindow_obj.person_input.get()
        keyObject.geraet = mainWindow_obj.geraet_input.get()
        keyObject.lehrstuhl = mainWindow_obj.lehrstuhl_input.get()
        keyObject.serienNummer = mainWindow_obj.seriennummer_input.get()
        keyObject.date = mainWindow_obj.datum_input.get()
        if len(mainWindow_obj.inventarnummer_input.get()) > 0:
            keyObject.ivs = mainWindow_obj.inventarnummer_input.get()
        else:
            keyObject.ivs = ""
        keyObject.hiwi = mainWindow_obj.hilfskraft_input.get()
        keyObject.id = mainWindow_obj.bitlocker_bezeichner_input.get()
        keyObject.key = mainWindow_obj.bitlocker_key_input.get()

    def checkFor_personInput_change() -> None:
        current = mainWindow_obj.person_input.get()
        if current != checkFor_personInput_change.last_value:
            mainWindow_obj.person_input.config(fg="black")
            mainWindow_obj.geraet_input.config(fg="black")
            mainWindow_obj.mainWindow_error.config(text="")
        else:
            mainWindow_obj.person_input.config(fg="red")
        mainWindow_obj.main_window.after(100, checkFor_personInput_change)	

    def checkFor_geraetInput_change() -> None:
        current = mainWindow_obj.geraet_input.get()
        if current != checkFor_geraetInput_change.last_value:
            mainWindow_obj.geraet_input.config(fg="black")
            mainWindow_obj.person_input.config(fg="black")
            mainWindow_obj.mainWindow_error.config(text="")
        else:
            mainWindow_obj.geraet_input.config(fg="red")
        mainWindow_obj.main_window.after(100, checkFor_geraetInput_change)

    def rename() -> str:
        """Returns the appended attributes of the key object.<br>Used by 'txt_to_pdf()' and 'write_entry()' """
        newFilename = "Bitlocker" + "_" + keyObject.date + "_" + keyObject.lehrstuhl + "_" + keyObject.user + "_SN-" + keyObject.serienNummer + "hiwi-" + keyObject.hiwi
        newFilename = newFilename.replace("/"," ").replace("\\","").replace(":"," ").replace("?","").replace("*","").replace("<","").replace(">","")
        return newFilename
       
    def txt_to_pdf(keyObject:Key) -> None:
        """Creates a PDF with the attributes of the key object and saves it in the Downloads directory"""
        download_dir = Path.home() / "Downloads" / str(rename() + ".pdf")
        pdf = PDF()
        pdf.add_page()
        pdf.header()
        pdf.device_info(keyObject)
        pdf.bezeichner_txt()
        pdf.print_bezeichner(keyObject)
        pdf.key_txt()
        pdf.key_barcode(keyObject)
        pdf.print_key(keyObject)
        pdf.output(download_dir)
        os.remove("key_barcode.svg")
    #############################################################

    def write_entry(entry) -> None:
        """Helper of 'make_keyEntry'<br> Writes a new entry with the data from the key object to the database"""
        if len(keyObject.txt_path) > 0:
            try:
                with open(keyObject.txt_path, 'rb') as f:
                    binary_id = database.add_binary(f.read())
                    entry.add_attachment(binary_id, rename() + ".txt") 
            except (FileNotFoundError, IOError) as e:
                mainWindow_obj.mainWindow_error.config(text=f"Fehler beim Anhängen der Datei: {e}", fg="red")
        entry.set_custom_property("Name", keyObject.user)
        entry.set_custom_property("Wiederherstellungsschluessel", keyObject.key)
        entry.set_custom_property("Bezeichner", keyObject.id)
        entry.set_custom_property("Gerät", keyObject.geraet)
        entry.set_custom_property("Datum", keyObject.date)
        entry.set_custom_property("Lehrstuhl", keyObject.lehrstuhl)
        entry.set_custom_property("Hilfskraft", keyObject.hiwi)
        entry.set_custom_property("Seriennummer", keyObject.serienNummer)
        entry.set_custom_property("Inventarisierungsnummer", keyObject.ivs)
        
        set_opacity(mainWindow_obj.mainWindow_success, 1)
        set_opacity(mainWindow_obj.mainWindow_error, 0)
        mainWindow_obj.mainWindow_success.config(text="Eintrag erfolgreich erstellt")

        if mainWindow_obj.create_pdf_checkButton_bool.get() == 1 :
            txt_to_pdf(keyObject)

    def handle_dublicates(double_entry) -> None:
        """Helper of 'make_keyEntry'<br> Creates a warning window which lets the user choose between dicarding the inputs or overwrite the entry with dublicate 'Seriennummer' """
        warningWindow_obj = None
        print(keyObject)
        print("------------")
        print(double_entry)
        if keyObject.ivs == double_entry.get_custom_property("Inventarisierungsnummer"):
            warningWindow_obj = WARNING_INVENTAR_SERIENNUMMER()
        else:
            warningWindow_obj = WARNING_SERIENNUMMER()
        
        warningWindow_obj.button_ueberschreiben.bind("<Button-1>", lambda event: (
            database.delete_entry(double_entry),
            write_entry(create_entry()),
            warningWindow_obj.warning_window.destroy()
        ))
        warningWindow_obj.button_verwerfen.bind("<Button-1>", lambda event: (
            mainWindow_obj.bitlocker_bezeichner_input.config(state="enabled"), # Enabeling manual input to delete it
            mainWindow_obj.bitlocker_key_input.config(state="enabled"),  # Enabling manual input to delete it
            clear_mainWindow_inputFields(),
            warningWindow_obj.warning_window.destroy()
        ))

        #warningWindow_obj.warning_window.mainloop()
        mainWindow_obj.main_window.wait_window(warningWindow_obj.warning_window)

    def create_entry():
        """Helper of 'make_keyEntry' <br> Returns a handle to a new new empty PyKeepass entry in the 'General' directory of the database"""
        generalGroup = database.find_groups(name='General',first=True)
        new_entry = database.add_entry(
            generalGroup,
            title = keyObject.user + " " + keyObject.geraet,
            username = keyObject.user,
            password = keyObject.key
        )
        return new_entry

    def make_keyEntry() -> None:
        mainWindow_obj.mainWindow_error.config(text="") # Clear previous error message
        mainWindow_obj.person_input.config(fg="black")
        mainWindow_obj.geraet_input.config(fg="black")
        # Setting all input text black
        for label in [mainWindow_obj.person_label, mainWindow_obj.geraet_label, mainWindow_obj.lehrstuhl_label, mainWindow_obj.seriennummer_label, mainWindow_obj.hilfskraft_label, mainWindow_obj.datum_label, mainWindow_obj.bitlocker_bezeichner_label, mainWindow_obj.bitlocker_key_label]:
            label.config(fg="black")

        get_fieldInputs()   # Read the user input from the fields and save it in the key object

        if not check_input_completeness():
            set_opacity(mainWindow_obj.mainWindow_success,0)
            set_opacity(mainWindow_obj.mainWindow_error, 1)
            mainWindow_obj.mainWindow_error.config(text="Eingabe unvollständig", fg="red")
            return
        # Überprüft, ob ein Eintrag mit der Bezeichnung: 'Titel + Gerät' bereits existiert.
        if database.find_entries(title=keyObject.user + " " + keyObject.geraet, first=True):
            set_opacity(mainWindow_obj.mainWindow_success, 0)
            set_opacity(mainWindow_obj.mainWindow_error, 1)
            mainWindow_obj.mainWindow_error.config(text="Eintrag mit dieser Bezeichnung existiert bereits", fg="red")
            mainWindow_obj.person_input.config(fg="red")
            mainWindow_obj.geraet_input.config(fg="red")
            checkFor_personInput_change.last_value = mainWindow_obj.person_input.get()
            checkFor_geraetInput_change.last_value = mainWindow_obj.geraet_input.get()
            raise ValueError("Eintrag existiert bereits")
        # Creates an empty KeePass entry
        double_entry = search_seriennummer(keyObject.serienNummer)
        if double_entry:
            handle_dublicates(double_entry)
        else:
            write_entry(create_entry())

        database.save()

    entrieset_var = tk.StringVar()
    database_entries_dropdown = ttk.Combobox(mainWindow_obj.main_window, textvariable=entrieset_var, values=create_entriesLst(database), font=("Helvetica", 12))
    database_entries_dropdown.set("Key auswählen")
    print_key_button = ttk.Button(mainWindow_obj.main_window, text="PDF erstellen")
    printKey_window_success = tk.Label(mainWindow_obj.main_window, text="", font="Helvetica 12", fg="green", width=35, anchor="center",justify= 'center')
    printKey_window_error = tk.Label(mainWindow_obj.main_window, text="", font="Helvetica 12", fg="red", width=35, anchor="center",justify= 'center')
    ############################
    # Konfiguration der Buttons #    
    #############################

    mainWindow_obj.browse_txt.configure(command=getKeyTxtFile)
    mainWindow_obj.print_key_windowButton.bind("<Button-1>", lambda event: printKey_window())
    mainWindow_obj.create_key_windowButton.bind("<Button-1>", lambda event: createKey_window())
    mainWindow_obj.create_key_button.bind("<Button-1>", lambda event: make_keyEntry())
    print_key_button.bind("<Button-1>", lambda event: print_key())

    def search_ivs(ivs:str) -> PyKeePass | None:
        """Searchs the KeePass database for a entry with the given IVS and returns it if existing, if not 'None' """
        entrytitle = None
        for titel,data in entryDict.items():
            if data.get("Inventarisierungsnummer") == ivs:
                entrytitle = titel
        if entrytitle:
            return database.find_entries(title=entrytitle, first=True)
        else:
            return None

    def search_seriennummer(sn:str) -> PyKeePass | None:
        """Searchs the KeePass database for a entry with the given 'Seriennummer' and returns it if existing, if not 'None' """
        entrytitle = None
        for titel,data in entryDict.items():
            if data.get("Seriennummer") == sn:
                entrytitle = titel
        if entrytitle:
            return database.find_entries(title=entrytitle, first=True)
        else:
            return None

    checkFor_geraetInput_change.last_value = mainWindow_obj.geraet_input.get() # Initialisierung der letzten Eingabe des Geräte-inputs
    checkFor_personInput_change.last_value = mainWindow_obj.person_input.get() # Initialisierung der letzten Eingabe des Person-inputs
    checkFor_geraetInput_change() # Aufruf der Funktion zur Überprüfung der Eingabe im Geräte-input
    checkFor_personInput_change() # Aufruf der Funktion zur Überprüfung der Eingabe im Person-input

    mainWindow_obj.main_window.mainloop()
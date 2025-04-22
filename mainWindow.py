import pykeepass.exceptions
from keepassObject import Key
#import createDatasheetPDF
from tkinter import *
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import BooleanVar
import sv_ttk
import pykeepass
from pykeepass import PyKeePass
from pathlib import Path
from PIL import ImageTk, Image
from keepassObject import Key
import subprocess
import pickle
import os
import re
import pyAesCrypt
import sys
from io import StringIO
from datetime import date
from ctypes import windll
from configparser import ConfigParser
import createDatasheetPDF

keyObject = None

############################################
# Laden des Key Objects aus der Binärdatei #
############################################

# Entschlüsseln der aes256 Datei
password = "long-and-random-password"
try:
    pyAesCrypt.decryptFile("keyObjPickle.aes","obj_de.pickle", password, 64 * 1024)
except FileNotFoundError as e:
    print(f"Decryption Error: {e}")

with open("obj_de.pickle", "rb") as f:
    keyObject = pickle.load(f)
    f.close()
#os.remove("obj_de.pickle") # Löschen der unverschlüsselten pickle-Datei
#os.remove("keyObjPickle.aes") # Löschen der verschlüsselten pickle-Datei
############################################

# https://stackoverflow.com/questions/77840560/why-opacity-in-tkinter-widgets-not-supported
def set_opacity(widget, value: float):
    widget = widget.winfo_id()
    value = int(255*value) # value from 0 to 1
    wnd_exstyle = windll.user32.GetWindowLongA(widget, -20)
    new_exstyle = wnd_exstyle | 0x00080000  
    windll.user32.SetWindowLongA(widget, -20, new_exstyle)  
    windll.user32.SetLayeredWindowAttributes(widget, 0, value, 2)

main_window = tk.Tk()
main_window.geometry("900x700")
main_window.minsize(900,700)
main_window.title("Keymaker")

database = PyKeePass(keyObject.database_path, keyObject.password)

def remove_createKey_window() -> None:
    for widget in createKey_windowsLayout.keys():
        set_opacity(widget, 0)

def printKey_window() -> None:
    database_entries_dropdown.grid(row=1, column=1, sticky='we',padx=(20, 0))
    get_databaseEntrie_button.grid(row=2, column=1, sticky='sw',padx=(20,0))
    create_key_windowButton.config(font="Helvetica 12")
    print_key_windowButton.config(font="Helvetica 12 bold")
    remove_createKey_window()

def createKey_window() -> None:
    database_entries_dropdown.grid_remove()
    set_opacity(get_databaseEntrie_button,0)
    create_key_windowButton.config(font="Helvetica 12 bold")
    print_key_windowButton.config(font="Helvetica 12")
    database_entries_dropdown.set("Key auswählen")
    for widget in createKey_windowsLayout.keys():
        set_opacity(widget, 1)

def get_databaseEntry() -> None:
    entryString = database_entries_dropdown.get()
    if entryString != "Key auswählen":
        try:
            entryString = os.path.basename(entryString)
            entry = database.find_entries(title=entryString, first=True)
            keyObject.user = entry.get_custom_property("Name")
            keyObject.device = entry.get_custom_property("Gerät")
            keyObject.lehrstuhl = entry.get_custom_property("Lehrstuhl")
            keyObject.serienNummer = entry.get_custom_property("Seriennummer")
            keyObject.date = entry.get_custom_property("Datum")
            keyObject.ivs = entry.get_custom_property("Inventarisierungsnummer")
            keyObject.hiwi = entry.get_custom_property("Hilfskraft")
            keyObject.id = entry.get_custom_property("Bezeichner")
            keyObject.key = entry.get_custom_property("Wiederherstellungsschluessel")

        except pykeepass.exceptions.KeePassFileError as e:
            print(f"Error: {e}")
          

# Entferne alle Eingaben aus den Inputfeldern des main windows
def clear_mainWindow_inputFields() -> None:
    person_input.delete(0, tk.END)
    geraet_input.delete(0, tk.END)
    seriennummer_input.delete(0, tk.END)
    hilfskraft_input.delete(0, tk.END)
    inventarnummer_input.delete(0, tk.END)
    lehrstuhl_input.set("Lehrstuhl auswählen")
    bitlocker_key_input.delete(0, tk.END)
    bitlocker_bezeichner_input.delete(0, tk.END)
    txt_entry.delete(0, tk.END)
    mainWindow_error.config(text="")
    mainWindow_success.config(text="")

def getKeyTxtFile() -> None:
    clear_mainWindow_inputFields() # Löschen der Eingaben im main window
    keyObject.txt_path = filedialog.askopenfilename(initialdir="/",title="Öffne die .txt-Datei", filetypes=[("Text Files","*txt")])
    if keyObject.txt_path:
        # Löschen des Eintrags im Textfeld
        txt_entry.delete(0,tk.END)
        try:
            keyObject.id, keyObject.key = extract_ID_KEY(remove_CRLF(keyObject.txt_path))
            # Einfügen des Pfades, id und des Keys in die Textfelder
            txt_entry.insert(0,keyObject.txt_path)
            txt_entry.config(fg="black")
            bitlocker_bezeichner_input.insert(0,keyObject.id)
            bitlocker_key_input.insert(0,keyObject.key)
        except TypeError as e:
            # Ausgeben der Fehlermeldung im Textfeld 
            txt_entry.insert(0, "kein gültiger Key" + str(e))
            txt_entry.config(fg="red")
 
def extract_ID_KEY(file) -> tuple:
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
        with open(file_path, "r") as file:
            content = file.read()
            clean_content = content.replace('\r', '')
            clean_content = ''.join(filter(lambda x: x.isprintable() or x == '\n', clean_content))
            file_curr = StringIO()
            file_curr.write(clean_content)
            file_curr.seek(0)
        return file_curr

def create_lehrstuhlLst(PyKeePass) -> list[str]:
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

# Lese die Eingabe aus den Textfeldern und speichere sie in den Attributen des Key-Objekts

def get_fieldInputs() -> None:
    keyObject.txt_path = txt_entry.get()
    keyObject.user = person_input.get()
    keyObject.geraet = geraet_input.get()
    keyObject.lehrstuhl = lehrstuhl_input.get()
    keyObject.serienNummer = seriennummer_input.get()
    keyObject.date = datum_input.get()
    keyObject.ivs = inventarnummer_input.get()
    keyObject.hiwi = hilfskraft_input.get()
    keyObject.id = bitlocker_bezeichner_input.get()
    keyObject.key = bitlocker_key_input.get()

def checkFor_personInput_change() -> None:
    current = person_input.get()
    if current != checkFor_personInput_change.last_value:
        person_input.config(fg="black")
        geraet_input.config(fg="black")
        mainWindow_error.config(text="")
    else:
        person_input.config(fg="red")
    main_window.after(100, checkFor_personInput_change)	

def checkFor_geraetInput_change() -> None:
    current = geraet_input.get()
    if current != checkFor_geraetInput_change.last_value:
        geraet_input.config(fg="black")
        person_input.config(fg="black")
        mainWindow_error.config(text="")
    else:
        geraet_input.config(fg="red")
    main_window.after(100, checkFor_geraetInput_change)

def rename_txt() -> str:
    newFilename = "Bitlocker" + "_" + keyObject.date + "_" + keyObject.lehrstuhl + "_" + keyObject.user + "_SN-" + keyObject.serienNummer + "hiwi-" + keyObject.hiwi + ".txt"
    newFilename = newFilename.replace("/"," ").replace("\\","").replace(":"," ").replace("?","").replace("*","").replace("<","").replace(">","")
    return newFilename

def create_keyEntry() -> None:
    mainWindow_error.config(text="") # Löschen der vorherigen Fehlermeldung
    person_input.config(fg="black")
    geraet_input.config(fg="black")

    get_fieldInputs()
    kp = PyKeePass(keyObject.database_path,keyObject.password)

    existingEntry = kp.find_entries(title=keyObject.user + " " + keyObject.geraet, first=True)
    if existingEntry:
        set_opacity(mainWindow_success, 0)
        mainWindow_error.config(text="Eintrag mit dieser Bezeichnung existiert bereits", fg="red")
        mainWindow_success
        person_input.config(fg="red")
        geraet_input.config(fg="red")
        checkFor_personInput_change.last_value = person_input.get()
        checkFor_geraetInput_change.last_value = geraet_input.get()
        raise ValueError("Eintrag existiert bereits")

    generalGroup = kp.find_groups(name='General',first=True)
    entry = kp.add_entry(
        generalGroup,
        title = keyObject.user + " " + keyObject.geraet,
        username = keyObject.user,
        password = keyObject.key # Bitlocker key
    )
    entry.set_custom_property("Name", keyObject.user)
    entry.set_custom_property("Wiederherstellungsschluessel", keyObject.key)
    entry.set_custom_property("Bezeichner", keyObject.id)
    entry.set_custom_property("Gerät", keyObject.geraet)
    entry.set_custom_property("Datum", keyObject.date)
    entry.set_custom_property("Lehrstuhl", keyObject.lehrstuhl)
    entry.set_custom_property("Hilfskraft", keyObject.hiwi)

    entry.set_custom_property("Seriennummer", keyObject.serienNummer)
    entry.set_custom_property("Inventarisierungsnummer", keyObject.ivs)

    with open(keyObject.txt_path, 'rb') as f:
        binary_id = kp.add_binary(f.read())
        entry.add_attachment(binary_id,rename_txt())

    set_opacity(mainWindow_success, 1)
    mainWindow_success.config(text="Eintrag erfolgreich erstellt")

    if create_pdf_checkButton_bool.get() == 1:
        createDatasheetPDF.txt_to_pdf(keyObject)

    kp.save()

######################################################################################
style = ttk.Style(main_window)
style.theme_use("vista")
main_window.iconbitmap(default="keymaker_images/lockSymbol.ico")

create_key_windowButton = ttk.Label(main_window,text="Key erstellen",font="Helvetica 12 bold", cursor="hand2")
print_key_windowButton = ttk.Label(main_window,text="Key drucken", font="Helvetica 12", cursor="hand2")

trennlinie = tk.Frame(main_window,bg='grey',width=1)

browse_txt = ttk.Button(main_window, text=".txt-Datei")
txt_entry = tk.Entry(main_window, font=("Helvetica 12"))

person_label = ttk.Label(main_window,text="Person", font="Helvetica 12")
person_input = tk.Entry(main_window, font=("Helvetica 12"))

geraet_label = ttk.Label(main_window,text="Gerät", font="Helvetica 12")
geraet_input = tk.Entry(main_window,font=("Helvetica 12"))

lehrstuhl_label = ttk.Label(main_window, text="Lehrstuhl", font="Helvetica 12")
lehrstuhl_var = tk.StringVar()
lehrstuhl_input = ttk.Combobox(main_window, textvariable=lehrstuhl_var, values=create_lehrstuhlLst(database), font=("Helvetica", 12))
lehrstuhl_input.set("Lehrstuhl auswählen") # Setzen des Standardwerts auf "Lehrstuhl auswählen"

seriennummer_label = ttk.Label(main_window, text="Seriennummer", font="Helvetica 12")
seriennummer_input = ttk.Entry(main_window, font=("Helvetica 12"))

datum_label = ttk.Label(main_window, text="Datum", font="Helvetica 12")
datum_input = ttk.Entry(main_window, font=("Helvetica 12"))
datum_input.insert(0,date.today().strftime("%d.%m.%Y")) # Setzen des Datums auf das heutige Datum

inventarnummer_label = ttk.Label(main_window, text="Inventarnummer", font="Helvetica 12 ")
inventarnummer_input = ttk.Entry(main_window, font=("Helvetica 12"))

hilfskraft_label = ttk.Label(main_window, text="Hilfskraft", font="Helvetica 12")
hilfskraft_input = ttk.Entry(main_window, font=("Helvetica 12"))

bitlocker_key_label = ttk.Label(main_window, text="Bitlocker Key", font="Helvetica 12")
bitlocker_key_input = ttk.Entry(main_window, font=("Helvetica 12"))

bitlocker_bezeichner_label = ttk.Label(main_window, text="Bitlocker Bezeichner", font="Helvetica 12")
bitlocker_bezeichner_input = ttk.Entry(main_window, font=("Helvetica 12"))

create_pdf_checkButton_bool = IntVar()
create_pdf_checkButton = tk.Checkbutton(main_window, text="PDF erstellen", font="Helvetica 12", variable = create_pdf_checkButton_bool)

mainWindow_error = tk.Label(main_window, text="", font="Helvetica 12", fg="red", width=35, anchor="center",justify= 'center')
mainWindow_success = tk.Label(main_window, text="", font="Helvetica 12", fg="green", width=35, anchor="center",justify= 'center')

#create_key_button_boolean = IntVar()
create_key_button = ttk.Button(main_window, text="Key erstellen")
###########################################################################
entrieset_var = tk.StringVar()
database_entries_dropdown = ttk.Combobox(main_window, textvariable=entrieset_var, values=create_entriesLst(database), font=("Helvetica", 12))
database_entries_dropdown.set("Key auswählen")
get_databaseEntrie_button = ttk.Button(main_window, text="PDF erstellen")
######################################################################################
for col in [0, 1, 2, 4]:
    main_window.columnconfigure(col, weight=1)
for col in (1, 3):
    main_window.columnconfigure(col, weight=3)
for row in range(17):
    main_window.rowconfigure(row, weight=1)

main_window.columnconfigure(0, minsize=150)

create_key_windowButton.grid(column=0,row=1,sticky='w',padx=(10,5))
print_key_windowButton.grid(column=0,row=2,sticky='w',padx=(10,5))

trennlinie.grid(row=0,column=0,sticky="nes",rowspan=21,padx=10)

createKey_windowsLayout = {
    browse_txt: {"row": 1, "column": 1, "sticky": 'wn', "padx": (20, 0)},
    txt_entry: {"row": 1, "column": 1, "sticky": 'wes', "columnspan": 3, "padx": (20, 20)},
    person_label: {"row": 3, "column": 1, "sticky": 'wn', "padx": (20, 0)},
    person_input: {"row": 3, "column": 1, "sticky": 'wes', "padx": (20, 0)},
    geraet_label: {"row": 3, "column": 3, "sticky": 'wn', "padx": (0, 20)},
    geraet_input: {"row": 3, "column": 3, "sticky": 'wes', "padx": (0, 20)},
    lehrstuhl_label: {"row": 5, "column": 1, "sticky": 'wn', "padx": (20, 0)},
    lehrstuhl_input: {"row": 5, "column": 1, "sticky": 'wes', "padx": (20, 0)},
    seriennummer_label: {"row": 5, "column": 3, "sticky": 'wn', "padx": (0, 20)},
    seriennummer_input: {"row": 5, "column": 3, "sticky": 'wes', "padx": (0, 20)},
    datum_label: {"row": 7, "column": 1, "sticky": 'wn', "padx": (20, 0)},
    datum_input: {"row": 7, "column": 1, "sticky": 'wes', "padx": (20, 0)},
    inventarnummer_label: {"row": 7, "column": 3, "sticky": 'wn', "padx": (0, 20)},
    inventarnummer_input: {"row": 7, "column": 3, "sticky": 'wes', "padx": (0, 20)},
    hilfskraft_label: {"row": 9, "column": 1, "sticky": 'wn', "padx": (20, 0)},
    hilfskraft_input: {"row": 9, "column": 1, "sticky": 'wes', "padx": (20, 0)},
    bitlocker_bezeichner_label: {"row": 11, "column": 1, "sticky": 'wn', "padx": (20, 20)},
    bitlocker_bezeichner_input: {"row": 11, "column": 1, "sticky": 'wes', "columnspan": 3, "padx": (20, 20)},
    bitlocker_key_label: {"row": 13, "column": 1, "sticky": 'wn', "padx": (20, 20)},
    bitlocker_key_input: {"row": 13, "column": 1, "sticky": 'wes', "columnspan": 3, "padx": (20, 20)},
    create_pdf_checkButton: {"row": 15, "column": 1, "sticky": 'wn', "padx": (20, 0)},
    mainWindow_error: {"row": 16, "column": 1, "sticky": 'new', 'columnspan': 5, "padx": (0,0)},
    mainWindow_success: {"row": 16, "column": 1, "sticky": 'new', 'columnspan': 5, "padx": (0,0)},
    create_key_button: {"row": 15, "column": 3, "sticky": 'en', "padx": (0, 20)},
}

for widget, layout in createKey_windowsLayout.items():
    widget.grid(**layout)
#############################
# Konfiguration der Buttons #    
#############################
browse_txt.configure(command=getKeyTxtFile)
print_key_windowButton.bind("<Button-1>", lambda event: printKey_window())
create_key_windowButton.bind("<Button-1>", lambda event: createKey_window())
create_key_button.bind("<Button-1>", lambda event: create_keyEntry())
get_databaseEntrie_button.bind("<Button-1>", lambda event: get_databaseEntry())

checkFor_geraetInput_change.last_value = geraet_input.get() # Initialisierung der letzten Eingabe des Geräte-inputs
checkFor_personInput_change.last_value = person_input.get() # Initialisierung der letzten Eingabe des Person-inputs
checkFor_geraetInput_change() # Aufruf der Funktion zur Überprüfung der Eingabe im Geräte-input
checkFor_personInput_change() # Aufruf der Funktion zur Überprüfung der Eingabe im Person-input

main_window.mainloop()
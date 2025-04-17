import pykeepass.exceptions
from keepassObject import Key
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
from io import StringIO
from datetime import date

keyObject = None
create_key = True
print_key = False

############################################
# Laden des Key Objects aus der Binärdatei #
############################################
with open("keyObj.pickle", "rb") as f:
    keyObject = pickle.load(f)
os.remove("keyObj.pickle") # Löschen der Binärdatei
############################################
main_window = tk.Tk()
main_window.geometry("900x700")
main_window.minsize(900,700)
main_window.title("Keymaker")

create_pdf = tk.BooleanVar(master=main_window,value=True)
database = PyKeePass(keyObject.database_path, keyObject.password)

####################
###  FUNKTIONEN  ###
####################
def getKeyTxtFile() -> None:
    keyObject.txt_path = filedialog.askopenfilename(initialdir="/",title="Öffne die .txt-Datei", filetypes=[("Text Files","*txt")])
    if keyObject.txt_path:
        # Löschen des Eintrags im Textfeld
        txt_entry.delete(0,tk.END)
        try:
            keyObject.id, keyObject.key = extract_ID_KEY(remove_CRLF(keyObject.txt_path))
            # Einfügen des Pfades, id und des Keys in die Textfelder
            txt_entry.insert(0,keyObject.txt_path)
            bitlocker_bezeichner_input.insert(0,keyObject.id)
            bitlocker_key_input.insert(0,keyObject.key)
        except TypeError as e:
            # Ausgeben der Fehlermeldung im Textfeld 
             txt_entry.insert(0,"kein gültiger Key" + str(e))

def extract_ID_KEY(file):
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

def remove_CRLF(file_path):
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
######################################################################################
style = ttk.Style(main_window)
style.theme_use("vista")
main_window.iconbitmap(default="keymaker_images/lockSymbol.ico")

create_key_windowButton = ttk.Label(main_window,text="Key erstellen",font="Helvetica 12 bold")
print_key_windowButton = ttk.Label(main_window,text="Key drucken", font="Helvetica 12 bold")

trennlinie = tk.Frame(main_window,bg='grey',width=1)

browse_txt = ttk.Button(main_window, text=".txt-Datei")
txt_entry = ttk.Entry(main_window, font=("Helvetica 12"))

person_label = ttk.Label(main_window,text="Person", font="Helvetica 12")
person_input = ttk.Entry(main_window, font=("Helvetica 12"))

geraet_label = ttk.Label(main_window,text="Gerät", font="Helvetica 12")
geraet_input = ttk.Entry(main_window,font=("Helvetica 12"))

lehrstuhl_label = ttk.Label(main_window, text="Lehrstuhl", font="Helvetica 12")
lehrstuhl_var = tk.StringVar()
lehrstuhl_input = ttk.Combobox(main_window, textvariable=lehrstuhl_var, values=create_lehrstuhlLst(database), font=("Helvetica", 12))
lehrstuhl_input.set("Lehrstuhl auswählen")

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

create_pdf_checkButton = tk.Checkbutton(main_window, text="PDF erstellen",variable=create_pdf, font="Helvetica 12")
create_key_button = ttk.Button(main_window, text="Key erstellen")

main_window.columnconfigure(0,weight=1)
main_window.columnconfigure(1,weight=1)
main_window.columnconfigure(2,weight=1)
main_window.columnconfigure(4,weight=1)
for col in (1, 3):
    main_window.columnconfigure(col, weight=3)
for row in range(16):
    main_window.rowconfigure(row, weight=1)


create_key_windowButton.grid(column=0,row=1,sticky='w',padx=(10,5))
print_key_windowButton.grid(column=0,row=2,sticky='w',padx=(10,5))

trennlinie.grid(row=0,column=0,sticky="nes",rowspan=20,padx=10)

browse_txt.grid(row=1,column=1,sticky='wn',padx=(20,0))
txt_entry.grid(row=1,column=1, sticky='wes', columnspan=3, padx=(20,20))

person_label.grid(row=3,column=1,sticky='wn',padx=(20,0))
person_input.grid(row=3,column=1,sticky='wes',padx=(20,0))

geraet_label.grid(row=3,column=3,sticky='wn',padx=(0,20))
geraet_input.grid(row=3,column=3,sticky='wes',padx=(0,20))  

lehrstuhl_label.grid(row=5, column=1, sticky='wn',padx=(20,0))
lehrstuhl_input.grid(row=5, column=1, sticky='wes',padx=(20,0))

seriennummer_label.grid(row=5, column=3, sticky='wn',padx=(0,20))
seriennummer_input.grid(row=5, column=3, sticky='wes',padx=(0,20))

datum_label.grid(row=7, column=1, sticky='wn',padx=(20,0))
datum_input.grid(row=7, column=1, sticky='wes', padx=(20,0))

inventarnummer_label.grid(row=7, column=3, sticky='wn',padx=(0,20))
inventarnummer_input.grid(row=7, column=3, sticky='wes', padx=(0,20))

hilfskraft_label.grid(row=9, column=1, sticky='wn',padx=(20,0))
hilfskraft_input.grid(row=9, column=1, sticky='wes', padx=(20,0))

bitlocker_bezeichner_label.grid(row=11, column=1, sticky='wn', padx=(20,20))
bitlocker_bezeichner_input.grid(row=11, column=1, sticky='wes', columnspan=3, padx=(20,20))

bitlocker_key_label.grid(row=13, column=1, sticky='wn',padx=(20,20 ))
bitlocker_key_input.grid(row=13, column=1, sticky='wes', columnspan=3, padx=(20,20))

create_pdf_checkButton.grid(row=15,column=1,sticky='wn',padx=(20,0))
create_key_button.grid(row=15,column=3,sticky='en',padx=(0,20))


# Konfiguration der Buttons    
browse_txt.configure(command=getKeyTxtFile)

main_window.mainloop()

    
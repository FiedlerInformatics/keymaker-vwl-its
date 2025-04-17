from pykeepass import PyKeePass
import re

# datenbank laden
kp = PyKeePass('testDatabase.kdbx', password='passwort')

entries = kp.entries

regex = r'General/Bitlocker/.*'
filtered_entries = []
print(entries)
for i in range(len(entries)):
    entry = entries[i]
    entry = str(entry).replace('Entry: ', '').replace('"','')
    if re.match(regex, entry): filtered_entries.append(entry.replace('(None)', ''))
    else: None
print("-----------------------")
print(filtered_entries)
from pykeepass import PyKeePass

kp = PyKeePass('testDatabase.kdbx', password='passwort')

# Alle Gruppen mit Pfad ausgeben
for group in kp.groups:
    print(group.path)

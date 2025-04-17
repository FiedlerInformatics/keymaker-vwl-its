from pykeepass import PyKeePass
import re

# Datenbank laden
kp = PyKeePass('testDatabase.kdbx', password='passwort')

# Zielgruppe finden
#bitlocker_group = kp.find_groups(path='General/Bitlocker')[0].subgroups[0]

#subgroup = kp.find_groups(path='General')

#strLst = [str(elem) for elem in kp.groups]

regex = r'General/Bitlocker/.*'

strLst = []
for i in range(len(kp.groups)): 
    strVar = str(kp.groups[i])
    strVar = strVar.replace('Group: ', '').replace('"','')
    if re.match(regex,strVar): strLst.append(strVar.replace('General/Bitlocker/','')) 
    else: None


#for i in range(len(kp.groups)):
#    print(kp.groups[i])

print(strLst)
from pykeepass import PyKeePass

kp = PyKeePass('testDatabase.kdbx', password='passwort')

generalGroup = kp.find_groups(name='General',first=True)

entry = kp.add_entry(
    generalGroup,  
    title='title',  
    username='username',
    password= 'password',
)

with open('loremipsum.txt', 'rb') as f:
    #entry.add_attachment('attachment.txt', f.read())
    binary_id = kp.add_binary(f.read())
    entry.add_attachment(binary_id,'attachment.txt')

kp.save()
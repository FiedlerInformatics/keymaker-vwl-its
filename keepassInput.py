from pykeepass import PyKeePass

# Open the KeePass database
kp = PyKeePass('testDatabase.kdbx', password='passwort')

# Get the group where you want to add the entry
group = kp.find_groups(name='General', first=True)

# Create a new entry with custom string fields
entry = kp.add_entry(
    group,
    title='My New Entry',
    username='myusername',
    password='mypassword',
    url='https://example.com',
    notes='This is a note.',
    #strings={ 'API Key': '123abc456def','Secret Token': 's3cr3tT0ken'}
)

entry.set_custom_property("Test_Property", "Test_Value")

# Save the database
kp.save()

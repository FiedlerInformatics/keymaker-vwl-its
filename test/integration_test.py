from pathlib import Path
from pykeepass import PyKeePass
import sys

# Ordnerstruktur ausgehend von dieser Testdatei auflösen
test_dir = Path(__file__).resolve().parent          # .../keymaker-vwl-its/test
project_root = test_dir.parent                     # .../keymaker-vwl-its
src_dir = project_root / "src"                     # .../keymaker-vwl-its/src

# src in sys.path ganz vorne einfügen
sys.path.insert(0, str(src_dir))

from keepassObject import Key
import mainWindow

db_path = test_dir / "testDatabase.kdbx"
db_handle = PyKeePass(filename=str(db_path), password="p")

def testOpen():
    print(f"Using database at: {db_path}")
    assert db_handle is not None

kpo = Key()
kpo.password = "p"
kpo.database_path = 'testDatabase.kdbx'

# Eintrag ohne 'Title' und 'User name'
def test_missing_TitleUser():
    mw = mainWindow.openMainWindow(kpo)
    
    pass


# Eintrag ohne Attribute
# Speichern von mehreren Keys hintereinander ohne Keymaker neu zu starten

# Überschreiben eines Eintrags ohne Attribute
# Überschreibung eines Eintrags ohne 'Title' und 'User name'
# Überschreibung von Keys mit identischer Seriennummer
# Überschreibung von Keys mit identischer Inventarisierungsnummer
# Überschreibung von Keys mit identischer Seriennummer und Inventarisierungsnummer

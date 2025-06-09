# VWL Keymaker
Automatisierungssoftware zur Archivierung von Bitlocker-keys in [KeePass](https://keepass.info/download.html) des technischen Supports der Volkswirtschaftlichen Fakultät der Ludwig-Maximilian-Universität München.

Eine Nutzungsanleitung finden Sie im [zugehörigen Wiki](https://github.com/FiedlerInformatics/keymaker-vwl-its/wiki).

![keymaker logo](https://github.com/FiedlerInformatics/keymaker-vwl-its/blob/main/keymaker_images/keymaker_header.jpg)
## Installation
Laden Sie den Ordner 'keymaker' mit der darin enthaltenen 'keymaker.exe' runter oder nutzen Sie den Git-Befehl 'git pull'.
Nach der ersten Nutzung wird der Dateipfad zur Datenbank in der Datei 'databasePath.ini' im selben Ordner gespeichert.

Alternativ kann auch das gesamte Github Repository mithilfe der Batch-Datei 'build_keymaker.bat' neu kompiliert werden. Hierfür muss zuvor die [PyInstaller Library](https://pyinstaller.org/en/stable/) installiert werden:
``` bash
pip install -U pyinstaller
```
## Screenshots
#### Login window
![keymaker login window](https://github.com/FiedlerInformatics/keymaker-vwl-its/blob/main/keymaker_images/Screenshot_loginWindow.jpg)

#### Main window
![keymaker login window](https://github.com/FiedlerInformatics/keymaker-vwl-its/blob/main/keymaker_images/Screenshot_mainWindow.jpg)

#### Key drucken Window
![keymaker key drucken window](https://github.com/FiedlerInformatics/keymaker-vwl-its/blob/main/keymaker_images/Screenshot_key-drucken_window.jpg)

#### Warning Windows
![keymaker login window](https://github.com/FiedlerInformatics/keymaker-vwl-its/blob/main/keymaker_images/warning_windows.jpg)

### Data sheet
![keymaker data sheet](https://github.com/FiedlerInformatics/keymaker-vwl-its/blob/main/keymaker_images/bitlocker-datasheet-example.jpg)

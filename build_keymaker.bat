@echo off
echo =====================================
echo   Starte Bereinigung vorheriger Builds
echo =====================================

REM Verzeichnisse löschen
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q __pycache__

REM .spec-Dateien löschen
del /f /q *.spec

echo =====================================
echo   Erzeuge Key-Maker.exe ...
echo =====================================

pyinstaller loginWindow.py --onefile --noconsole ^
--name "keymaker" ^
--icon=keymaker_images\keymaker_logo.ico ^
--add-data "keymaker_images\*.png;keymaker_images" ^
--add-data "keymaker_images\*.ico;keymaker_images"

del /f /q *.spec
rmdir /s /q build
rename "dist" "keymaker"

echo =====================================
echo   Build abgeschlossen!
echo   EXE befindet sich in: keymaker\keymaker.exe
echo =====================================
pause

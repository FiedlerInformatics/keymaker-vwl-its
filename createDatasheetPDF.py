from fpdf import FPDF
from keepassObject import Key
from pathlib import Path
import os

mock_key = Key(
    password="testpass",
    database_path="testdb.kdbx",
    txt_path="bitlocker.txt",
    user="Max Mustermann",
    geraet="Laptop-123",
    serienNummer="SN987654",
    lehrstuhl="Informatik",
    date="2024-04-22",
    ivs="IVS123456",
    hiwi="Ja",
    id="ID-001",
    key="123456-654321-123456-654321-123456-654321-123456-654321"
)

def name_pdf(keyObject:Key) -> str:
    newFilename = "Bitlocker" + "_" + keyObject.date + "_" + keyObject.lehrstuhl + "_" + keyObject.user + "_SN-" + keyObject.serienNummer + "hiwi-" + keyObject.hiwi + ".pdf"
    newFilename = newFilename.replace("/"," ").replace("\\","").replace(":"," ").replace("?","").replace("*","").replace("<","").replace(">","")
    return newFilename

#def name_pdf(keyObject:Key) -> str:
#    return "bitlockerKey.pdf"

class PDF(FPDF):
    def header(self):
        self.set_y(10)
        self.set_font("helvetica", style="B" , size=17)
        self.cell(10)
        self.cell(170,20, "BitLocker Key", border=0, align="C")

    def device_info(self,keyObj:Key):
        self.set_y(35)
        self.set_font("helvetica", style="B", size=12 )
        info_text = (
            f"User: {keyObj.user}\n"
            f"Device: {keyObj.geraet}\n"
            f"Lehrstuhl: {keyObj.lehrstuhl}"
        )
        self.multi_cell(170, 10, info_text, border=1, align="L")

    def main(self, filepath):
        with open(filepath, "rb") as fh:
            txt = fh.read().decode("utf-16")

        self.set_auto_page_break(auto=False)  # Verhindert neue Seiten
        self.set_font("helvetica", size=12)

        # Höhe des Textblocks grob abschätzen
        num_lines = txt.count("\n") + 1
        line_height = 8  # etwas höher für bessere Lesbarkeit
        total_height = num_lines * line_height

        # Seite ist 297mm hoch (A4), rechne Y-Start aus
        y_start = (297 - total_height) / 2
        self.set_y(y_start)

        self.multi_cell(0, line_height, txt, align="L")

    def footer(self):
        self.set_y(-35)
        self.set_font("helvetica", size=12)
        self.set_text_color(255, 0, 0)  # Set font color to red
        self.cell(10)
        self.multi_cell(170,
                        12,
                        "Bewahren Sie das Gerät und den dazugehörigen Bitlocker-Key gertrennt auf."
                        + "\n" +
                        "Store this device and its respective Bitlocker-key seperately.",
                        border=0,
                        align="C")
       
def txt_to_pdf(keyObject:Key):
    print("Called from main")
    download_dir = Path.home() / "Downloads" / name_pdf(keyObject)
    pdf = PDF()
    pdf.add_page()
    pdf.main(keyObject.txt_path)
    pdf.device_info(keyObject)
    pdf.output(download_dir)

    os.remove(keyObject.txt_path)
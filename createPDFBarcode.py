from fpdf import FPDF
from keepassObject import Key
from pathlib import Path
import os
import barcode
from barcode.writer import ImageWriter

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
    id="F96D4444-63B9-54E8-B62A-F77777777777",
    key="111111-222222-333333-444444-555555-666666-777777-888888"
)


def create_id_barcode(keyobject:Key) -> str:
    EAN = barcode.get_barcode_class('code39')
    idIO = EAN(keyobject.id, writer=ImageWriter(),add_checksum = False)
    idIO.save("id_barcode")
    return("id_barcode.png")

def create_key_barcode(keyobject:Key) -> str:
    EAN = barcode.get_barcode_class('code39')
    idIO = EAN(keyobject.key, writer=ImageWriter(),add_checksum = False)
    idIO.save("key_barcode")
    return("key_barcode.png")

class PDF(FPDF):
    def header(self):
        self.set_y(10)
        self.set_font("helvetica", style="B" , size=17)
        self.cell(10)
        self.cell(170,20, "BitLocker Key", border=0, align="C")

    def device_info(self,keyObject):
        self.set_y(35)
        self.set_x(20)
        self.set_font("helvetica", style="B", size=12 )
        info_text = (
            f"User: {keyObject.user}\n"
            f"Device: {keyObject.geraet}\n"
            f"Lehrstuhl: {keyObject.lehrstuhl}"
        )
        self.multi_cell(170, 9, info_text, border=1, align="L")

    def bezeichner_txt(self):
        self.set_y(80)
        self.set_font("helvetica", size=12)
        self.cell(10)
        self.multi_cell(170,
                        8, #Spaltenabstand
                        "Wiederherstellungsschlüssel für die BitLocker-Laufwerkverschlüsselung"
                        + "\n" +
                        "Um zu überprüfen, ob es sich um den richtigen Wiederherstellungsschlüssel handelt,"
                        + "\n" +
                        "vergleichen Sie den Beginn des folgenden Bezeichners mit dem auf dem PC angezeigten Bezeichnerwert."
                        + "\n" + "\n" +
                        "Bezeichner:"
                        ,
                        border=0,
                        align="L")        

    def bezeichner_barcode(self,keyObject:Key) -> None:
        self.image(create_id_barcode(keyObject),30,135,150)

    def key_txt(self) -> None:
        self.set_y(170)
        self.set_font("helvetica", size=12)
        self.cell(10)
        self.multi_cell(170,
                        8, #Spaltenabstand
                        "Falls der obige Bezeichner mit dem auf dem PC angezeigten Bezeichner übereinstimmt," 
                        + "\n" +
                        "sollten Sie den folgenden Schlüssel zum Entsperren des Laufwerks verwenden."
                        + "\n" + "\n" +
                        "Wiederherstellungsschlüssel:"
                        ,
                        border=0,
                        align="L")  
    
    def key_barcode(self,keyObject:Key) -> None:
        self.image(create_key_barcode(keyObject),30,210,150)

    def footer(self):
        self.set_y(-45)
        self.set_font("helvetica", size=12)
        self.set_text_color(255, 0, 0)  # Set font color to red
        self.cell(10)
        self.multi_cell(170,
                        12,
                        "Bewahren Sie das Gerät und den dazugehörigen Bitlocker-Key gertrennt auf."
                        + "\n" +
                        "Store the device and the corresponding Bitlocker key separate.",
                        border=0,
                        align="C")        


pdf = PDF()
pdf.add_page()
pdf.header()
pdf.device_info(mock_key)
pdf.bezeichner_txt()
pdf.bezeichner_barcode(mock_key)
pdf.key_txt()
pdf.key_barcode(mock_key)
pdf.output('barcodeTest.pdf')
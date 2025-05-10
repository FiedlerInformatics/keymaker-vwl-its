from keepassObject import Key
from fpdf import FPDF
import barcode
from barcode.writer import SVGWriter

class PDF(FPDF):
        
        def create_id_barcode(keyobject:Key) -> str:
            EAN = barcode.get_barcode_class('code39')
            idIO = EAN(keyobject.id, writer=SVGWriter(), add_checksum=True)
            idIO.save("id_barcode")
            return "id_barcode.svg"

        def create_key_barcode(keyobject:Key) -> str:
            EAN = barcode.get_barcode_class('code128')
            idIO = EAN(keyobject.key.replace("-", ""), writer=SVGWriter())
            idIO.save("key_barcode")
            return "key_barcode.svg"

        def header(self):
            self.set_y(10)
            self.set_font("helvetica", style="B" , size=17)
            self.cell(10)
            self.cell(170,20, "Bit Locker Key", border=0, align="C")

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

        def print_bezeichner(self,keyObject:Key) -> None:
            self.set_y(127)
            self.set_font("helvetica", style="B" , size=12)
            self.cell(10)
            self.cell(170,20, keyObject.id, border=0, align="C")

        def key_txt(self) -> None:
            self.set_y(150)
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
            self.image(PDF.create_key_barcode(keyObject),17.5,175,175,25)

        def print_key(self,keyObject:Key) -> None:
            self.set_y(190)
            self.set_font("helvetica", style="B" , size=12)
            self.cell(10)
            self.cell(170,20, keyObject.key, border=0, align="C")

        def footer(self):
            self.set_y(-45)
            self.set_font("helvetica", size=12)
            self.set_text_color(255, 0, 0)  # Rote Schrift
            self.cell(10)
            self.multi_cell(170,
                            12,
                            "Bewahren Sie das Gerät und den dazugehörigen Bitlocker-Key gertrennt auf."
                            + "\n" +
                            "Store the device and the corresponding Bitlocker key separate.",
                            border=0,
                            align="C") 
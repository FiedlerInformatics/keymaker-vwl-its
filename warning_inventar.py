from warning import WARNING

class WARNING_INVENTAR(WARNING):
    
    def __init__(self):
        super().__init__()
        self.warning_text.config(
            text="Ein Eintrag mit dieser Inventarisierungsnummer existiert bereits.\nSollen neuen Daten verworfen- oder sollen der vorherige Eintrag überschrieben werden?"
        )
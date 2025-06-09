from warning import WARNING

class WARNING_SERIENNUMMER(WARNING):
    
    def __init__(self):
        super().__init__()
        self.warning_text.config(
            text="Ein Eintrag mit dieser Seriennummer existiert bereits.\nSollen die neuen Daten verworfen- oder der bestehende Eintrag überschrieben werden?"
        )
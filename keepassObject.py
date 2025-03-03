from dataclasses import dataclass
from datetime import datetime

@dataclass
class Key:
    password: str
    id: str
    key: str
    user: str
    geraet: str
    date: datetime
    lehrstuhl: str
    hiwi: str
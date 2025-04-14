from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import pykeepass

@dataclass
class Key:
    password: Optional[str] = None
    database_path: Optional[str] = None
    database = None
    id: Optional[str] = None
    key: Optional[str] = None
    user: Optional[str] = None
    geraet: Optional[str] = None
    serienNummer: Optional[str] = None
    ivs: Optional[str] = None
    date: Optional[datetime] = None
    lehrstuhl: Optional[str] = None
    hiwi: Optional[str] = None

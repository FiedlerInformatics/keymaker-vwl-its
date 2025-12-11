from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Key:
    password: Optional[str] = None
    database_path: Optional[str] = None

    txt_path: Optional[str] = None
    
    user: Optional[str] = None
    geraet: Optional[str] = None
    
    lehrstuhl: Optional[str] = None
    serienNummer: Optional[str] = None
    
    date: Optional[str] = None
    ivs: Optional[str] = None
    
    hiwi: Optional[str] = None
    
    id: Optional[str] = None
    
    key: Optional[str] = None

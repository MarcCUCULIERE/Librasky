from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class WhiskyBase(BaseModel):
    name: str
    distillery: str
    country: str
    region: str
    age: Optional[int] = None
    type: str
    personal_note: Optional[float] = None
    comments: Optional[str] = None
    price: Optional[float] = None
    volume: int
    alcohol_degree: float
    image: Optional[str] = None
    purchase_date: Optional[date] = None  # Ajout de la date d'achat

class WhiskyCreate(WhiskyBase):
    date_added: Optional[date] = None

class WhiskyUpdate(WhiskyBase):
    name: Optional[str] = None
    distillery: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    type: Optional[str] = None
    volume: Optional[int] = None
    alcohol_degree: Optional[float] = None
    purchase_date: Optional[date] = None  # Ajout de la date d'achat

class WhiskyResponse(WhiskyBase):
    id: int
    date_added: Optional[str] = None
    purchase_date: Optional[str] = None  # Ajout de la date d'achat

    class Config:
        orm_mode = True
from sqlalchemy.orm import Session
from app.models.whisky import Whisky
from typing import List, Optional
from datetime import date

def create_whisky(db: Session, whisky_data: dict) -> Whisky:
    db_whisky = Whisky(**whisky_data)
    db.add(db_whisky)
    db.commit()
    db.refresh(db_whisky)
    return db_whisky

def get_whisky(db: Session, whisky_id: int) -> Optional[Whisky]:
    return db.query(Whisky).filter(Whisky.id == whisky_id).first()

def get_whiskies(db: Session, skip: int = 0, limit: int = 100) -> List[Whisky]:
    return db.query(Whisky).offset(skip).limit(limit).all()

def update_whisky(db: Session, whisky_id: int, whisky_data: dict) -> Optional[Whisky]:
    db_whisky = db.query(Whisky).filter(Whisky.id == whisky_id).first()
    if db_whisky:
        for key, value in whisky_data.items():
            setattr(db_whisky, key, value)
        db.commit()
        db.refresh(db_whisky)
    return db_whisky

def delete_whisky(db: Session, whisky_id: int) -> bool:
    db_whisky = db.query(Whisky).filter(Whisky.id == whisky_id).first()
    if db_whisky:
        db.delete(db_whisky)
        db.commit()
        return True
    return False
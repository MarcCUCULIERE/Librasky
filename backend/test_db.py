import sys
import os

# Ajout du répertoire parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.crud.whisky import create_whisky
from datetime import date

def test_create_whisky():
    db = SessionLocal()
    try:
        test_whisky = {
            "name": "Test Whisky",
            "distillery": "Test Distillery",
            "country": "Scotland",
            "region": "Speyside",
            "age": 12,
            "type": "Single Malt",
            "personal_note": 4.5,
            "comments": "Test whisky",
            "image": None,
            "date_added": date.today(),
            "price": 50.0,
            "volume": 700,
            "alcohol_degree": 40.0
        }

        new_whisky = create_whisky(db, test_whisky)
        print(f"Whisky créé avec succès! ID: {new_whisky.id}")
        return new_whisky
    finally:
        db.close()

if __name__ == "__main__":
    test_create_whisky()
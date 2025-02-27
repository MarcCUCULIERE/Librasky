from sqlalchemy import Column, Integer, String, Float, Date, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
import base64
from datetime import date

Base = declarative_base()

class Whisky(Base):
    __tablename__ = "whiskies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    distillery = Column(String)
    country = Column(String)
    region = Column(String)
    age = Column(Integer)
    type = Column(String)
    personal_note = Column(Float)
    comments = Column(String)
    image = Column(LargeBinary, nullable=True)
    date_added = Column(Date, default=date.today)
    purchase_date = Column(Date, nullable=True)
    price = Column(Float)
    volume = Column(Integer)
    alcohol_degree = Column(Float)

    def to_dict(self):
        result = {
            "id": self.id,
            "name": self.name,
            "distillery": self.distillery,
            "country": self.country,
            "region": self.region,
            "age": self.age,
            "type": self.type,
            "personal_note": self.personal_note,
            "comments": self.comments,
            "date_added": str(self.date_added) if self.date_added else None,
            "purchase_date": str(self.purchase_date) if self.purchase_date else None,
            "price": self.price,
            "volume": self.volume,
            "alcohol_degree": self.alcohol_degree,
            "image": base64.b64encode(self.image).decode('utf-8') if self.image else None
        }
        return result

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Chargement des variables d'environnement
load_dotenv()

# Récupération de l'URL de la base de données depuis les variables d'environnement
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./librasky.db")

# Création du moteur SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarative pour les modèles
Base = declarative_base()

# Dependency pour obtenir la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Carica variabili d'ambiente
load_dotenv()

# URL del database (da variabile d'ambiente)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://smartdispo_user:password@smartdispo-db:5432/smartdispo"
)

# Crea engine SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crea SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class per i modelli
Base = declarative_base()

# Modello Item per il database
class ItemDB(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)

# Funzione per ottenere la sessione del database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crea le tabelle nel database
def init_db():
    Base.metadata.create_all(bind=engine)
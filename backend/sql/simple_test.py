"""Simple database list test"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Country

DB_FILE = os.path.join(os.path.dirname(__file__), "shipping_test.db")
engine = create_engine(f"sqlite:///{DB_FILE}", echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

countries = db.query(Country).all()
print(f"Countries: {[(c.id, c.name) for c in countries]}")
db.close()

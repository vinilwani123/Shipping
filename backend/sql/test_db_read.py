"""
Test database connectivity and list countries from SQLite database
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Country

# Database file path
DB_FILE = os.path.join(os.path.dirname(__file__), "shipping_test.db")

if not os.path.exists(DB_FILE):
    print(f"❌ Database file not found: {DB_FILE}")
    sys.exit(1)

# Create SQLite engine
DATABASE_URL = f"sqlite:///{DB_FILE}"
engine = create_engine(DATABASE_URL, echo=False)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

print("=" * 60)
print("Database Connectivity Test")
print("=" * 60)
print(f"Database: {os.path.abspath(DB_FILE)}\n")

try:
    # Query countries
    countries = db.query(Country).all()
    
    print("📋 Countries in database:")
    print("-" * 60)
    for country in countries:
        print(f"ID: {country.id:2d} | Name: {country.name:20s} | ISO: {country.iso_code}")
    print("-" * 60)
    print(f"\n✅ Successfully retrieved {len(countries)} countries")
    
    # Return as list of tuples
    country_list = [(c.id, c.name) for c in countries]
    print(f"\n📊 Countries list: {country_list}")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

print("=" * 60)

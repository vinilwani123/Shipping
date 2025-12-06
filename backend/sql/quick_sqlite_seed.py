"""
Quick SQLite Seed Script for Development Testing
Creates shipping_test.db with schema and seed data
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from app.database import Base
from app.models import User, Country, CountryRule, BannedItem, Order
from sqlalchemy.orm import sessionmaker

# Database file path
DB_FILE = os.path.join(os.path.dirname(__file__), "shipping_test.db")

print("=" * 60)
print("SQLite Database Seed Script")
print("=" * 60)

# Remove existing database file
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print(f"✅ Removed existing database file")

# Create SQLite engine
DATABASE_URL = f"sqlite:///{DB_FILE}"
engine = create_engine(DATABASE_URL, echo=False)

print(f"📁 Creating database: {DB_FILE}")

# Create all tables
Base.metadata.create_all(bind=engine)
print(f"✅ Created all tables using SQLAlchemy models")

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    # Insert Countries
    print("\n📍 Inserting countries...")
    india = Country(name="India", iso_code="IN")
    usa = Country(name="United States", iso_code="US")
    
    db.add(india)
    db.add(usa)
    db.commit()
    db.refresh(india)
    db.refresh(usa)
    
    print(f"   ✅ India (ID: {india.id})")
    print(f"   ✅ United States (ID: {usa.id})")
    
    # Insert Country Rules
    print("\n📏 Inserting country rules...")
    india_rule = CountryRule(
        country_id=india.id,
        max_weight_kg=50.0,
        max_size_cm=200.0,
        custom_duty_percent=5.0
    )
    usa_rule = CountryRule(
        country_id=usa.id,
        max_weight_kg=70.0,
        max_size_cm=220.0,
        custom_duty_percent=10.0
    )
    
    db.add(india_rule)
    db.add(usa_rule)
    db.commit()
    
    print(f"   ✅ India: max_weight=50kg, max_size=200cm, duty=5%")
    print(f"   ✅ USA: max_weight=70kg, max_size=220cm, duty=10%")
    
    # Insert Banned Items
    print("\n🚫 Inserting banned items...")
    
    # India banned items
    india_banned_1 = BannedItem(country_id=india.id, item_name="lithium battery")
    india_banned_2 = BannedItem(country_id=india.id, item_name="explosives")
    
    # USA banned items
    usa_banned = BannedItem(country_id=usa.id, item_name="firearms")
    
    db.add_all([india_banned_1, india_banned_2, usa_banned])
    db.commit()
    
    print(f"   ✅ India: lithium battery, explosives")
    print(f"   ✅ USA: firearms")
    
    print("\n" + "=" * 60)
    print("✅ Database seeded successfully!")
    print("=" * 60)
    
    # Verification: List all countries
    print("\n📋 Verification - Countries in database:")
    countries = db.query(Country).all()
    for country in countries:
        print(f"   ID: {country.id}, Name: {country.name}, ISO: {country.iso_code}")
    
    print(f"\n📊 Total countries: {len(countries)}")
    print(f"📁 Database location: {os.path.abspath(DB_FILE)}")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()

print("\n" + "=" * 60)
print("To use this database, set:")
print(f"DATABASE_URL=sqlite:///{os.path.abspath(DB_FILE)}")
print("=" * 60)

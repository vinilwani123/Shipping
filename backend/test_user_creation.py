"""
Test user creation directly using CRUD functions
"""
import sys
sys.path.insert(0, '.')

from app import crud, schemas
from app.database import SessionLocal

print("Testing user creation directly...")

db = SessionLocal()

try:
    # Test password hashing first
    print("\n1. Testing password hashing...")
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    test_password = "test123"
    hashed = pwd_context.hash(test_password)
    print(f"   ✅ Password hashed successfully: {hashed[:50]}...")
    
    # Test user creation
    print("\n2. Testing user creation...")
    import random
    user_data = schemas.UserCreate(
        email=f"test{random.randint(1000,9999)}@example.com",
        password="test123",
        name="Test User"
    )
    
    # Check if user exists
    existing = crud.get_user_by_email(db, user_data.email)
    if existing:
        print(f"   ⚠️ User already exists, deleting...")
        db.query(crud.models.User).filter(crud.models.User.email == user_data.email).delete()
        db.commit()
    
    # Create user
    created_user = crud.create_user(db, user_data)
    print(f"   ✅ User created successfully!")
    print(f"   ID: {created_user.id}")
    print(f"   Email: {created_user.email}")
    print(f"   Name: {created_user.name}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

"""
Seed MySQL database with schema and data
"""
import pymysql
import sys

print("=" * 60)
print("MySQL Database Seed Script")
print("=" * 60)

# Database connection parameters
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',  # Update if different
    'database': 'shipping_poc',
    'charset': 'utf8mb4'
}

try:
    # Connect to MySQL
    connection = pymysql.connect(**DB_CONFIG)
    cursor = connection.cursor()
    
    print(f"✅ Connected to MySQL database: {DB_CONFIG['database']}")
    
    # Drop existing tables
    print("\n🗑️  Dropping existing tables...")
    cursor.execute("DROP TABLE IF EXISTS orders")
    cursor.execute("DROP TABLE IF EXISTS banned_items")
    cursor.execute("DROP TABLE IF EXISTS country_rules")
    cursor.execute("DROP TABLE IF EXISTS countries")
    cursor.execute("DROP TABLE IF EXISTS users")
    print("   ✅ Existing tables dropped")
    
    # Create users table
    print("\n📊 Creating tables...")
    cursor.execute("""
        CREATE TABLE users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_email (email)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    print("   ✅ users")
    
    # Create countries table
    cursor.execute("""
        CREATE TABLE countries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            iso_code VARCHAR(10) NOT NULL,
            INDEX idx_name (name)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    print("   ✅ countries")
    
    # Create country_rules table
    cursor.execute("""
        CREATE TABLE country_rules (
            id INT AUTO_INCREMENT PRIMARY KEY,
            country_id INT UNIQUE NOT NULL,
            max_weight_kg FLOAT NOT NULL,
            max_size_cm FLOAT NOT NULL,
            custom_duty_percent FLOAT NOT NULL DEFAULT 0.0,
            FOREIGN KEY (country_id) REFERENCES countries(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    print("   ✅ country_rules")
    
    # Create banned_items table
    cursor.execute("""
        CREATE TABLE banned_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            country_id INT NOT NULL,
            item_name VARCHAR(255) NOT NULL,
            FOREIGN KEY (country_id) REFERENCES countries(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    print("   ✅ banned_items")
    
    # Create orders table
    cursor.execute("""
        CREATE TABLE orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            country_id INT NOT NULL,
            weight_kg FLOAT NOT NULL,
            size_cm FLOAT NOT NULL,
            item_description TEXT NOT NULL,
            shipping_charge FLOAT,
            status ENUM('PENDING', 'CONFIRMED', 'REJECTED') NOT NULL DEFAULT 'PENDING',
            rejection_reason TEXT,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (country_id) REFERENCES countries(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    print("   ✅ orders")
    
    # Insert seed data
    print("\n📍 Inserting countries...")
    cursor.execute("INSERT INTO countries (name, iso_code) VALUES ('India', 'IN')")
    cursor.execute("INSERT INTO countries (name, iso_code) VALUES ('United States', 'US')")
    print("   ✅ India (IN)")
    print("   ✅ United States (US)")
    
    # Insert country rules
    print("\n📏 Inserting country rules...")
    cursor.execute("""
        INSERT INTO country_rules (country_id, max_weight_kg, max_size_cm, custom_duty_percent)
        VALUES (1, 50.0, 200.0, 5.0)
    """)
    print("   ✅ India: max_weight=50kg, max_size=200cm, duty=5%")
    
    cursor.execute("""
        INSERT INTO country_rules (country_id, max_weight_kg, max_size_cm, custom_duty_percent)
        VALUES (2, 70.0, 220.0, 10.0)
    """)
    print("   ✅ USA: max_weight=70kg, max_size=220cm, duty=10%")
    
    # Insert banned items
    print("\n🚫 Inserting banned items...")
    cursor.execute("INSERT INTO banned_items (country_id, item_name) VALUES (1, 'lithium battery')")
    cursor.execute("INSERT INTO banned_items (country_id, item_name) VALUES (1, 'explosives')")
    cursor.execute("INSERT INTO banned_items (country_id, item_name) VALUES (2, 'firearms')")
    print("   ✅ India: lithium battery, explosives")
    print("   ✅ USA: firearms")
    
    # Commit changes
    connection.commit()
    
    # Verify data
    print("\n" + "=" * 60)
    print("📋 Verification - Countries in database:")
    cursor.execute("SELECT id, name, iso_code FROM countries")
    countries = cursor.fetchall()
    for country in countries:
        print(f"   ID: {country[0]}, Name: {country[1]}, ISO: {country[2]}")
    
    print("\n✅ Database seeded successfully!")
    print("=" * 60)
    
except pymysql.Error as e:
    print(f"\n❌ MySQL Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    if 'connection' in locals():
        cursor.close()
        connection.close()

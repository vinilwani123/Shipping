"""
Check if database tables exist and create if needed
"""
import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'shipping_poc',
}

print("Checking database tables...")

try:
    connection = pymysql.connect(**DB_CONFIG)
    cursor = connection.cursor()
    
    # Check existing tables
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    print(f"\nExisting tables in shipping_poc:")
    if tables:
        for table in tables:
            print(f"  ✅ {table[0]}")
    else:
        print("  ⚠️ No tables found!")
    
    print(f"\nTotal tables: {len(tables)}")
    
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f"❌ Error: {e}")

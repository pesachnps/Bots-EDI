import sqlite3

conn = sqlite3.connect(r'C:\Users\PGelfand\.bots\env\default\botssys\sqlitedb\botsdb')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [t[0] for t in cursor.fetchall()]

print("Tables in database:")
for table in tables:
    print(f"  - {table}")

# Check if Partner-related tables exist
partner_tables = [t for t in tables if 'partner' in t.lower()]
user_tables = [t for t in tables if 'user' in t.lower() or 'auth' in t.lower()]

print(f"\nPartner-related tables: {partner_tables if partner_tables else 'NONE'}")
print(f"User-related tables: {user_tables if user_tables else 'NONE'}")

conn.close()

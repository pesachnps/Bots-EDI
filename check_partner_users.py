import sqlite3

conn = sqlite3.connect(r'C:\Users\PGelfand\.bots\env\default\botssys\sqlitedb\botsdb')
cursor = conn.cursor()

# Check usersys_partner table structure and data
print("=== usersys_partner table ===")
cursor.execute("PRAGMA table_info(usersys_partner)")
columns = cursor.fetchall()
print("Columns:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

cursor.execute("SELECT COUNT(*) FROM usersys_partner")
count = cursor.fetchone()[0]
print(f"\nTotal partners: {count}")

if count > 0:
    cursor.execute("SELECT * FROM usersys_partner LIMIT 5")
    rows = cursor.fetchall()
    print("\nFirst 5 partners:")
    for row in rows:
        print(f"  {row}")

# Check if PartnerUser table exists
print("\n=== Checking for PartnerUser table ===")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%user%' AND name LIKE '%partner%'")
partner_user_tables = cursor.fetchall()
print(f"Partner-user related tables: {partner_user_tables if partner_user_tables else 'NONE FOUND'}")

# Check auth_user table
print("\n=== auth_user table ===")
cursor.execute("SELECT COUNT(*) FROM auth_user")
user_count = cursor.fetchone()[0]
print(f"Total users in auth_user: {user_count}")

if user_count > 0:
    cursor.execute("SELECT id, username, email, is_staff, is_active FROM auth_user LIMIT 10")
    users = cursor.fetchall()
    print("\nFirst 10 users:")
    for user in users:
        print(f"  ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Staff: {user[3]}, Active: {user[4]}")

conn.close()

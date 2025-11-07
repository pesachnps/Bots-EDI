#!/usr/bin/env python
"""Create the missing uniek table"""
import sqlite3

DB_PATH = r"C:\Users\USER\Projects\bots\env\botssys\sqlitedb\botsdb"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create uniek table based on Bots schema
cursor.execute('''
    CREATE TABLE IF NOT EXISTS uniek (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        domein VARCHAR(35) NOT NULL,
        nummer INTEGER NOT NULL DEFAULT 0,
        UNIQUE (domein)
    )
''')

conn.commit()
print("✅ Created uniek table successfully")

# Check if it was created
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='uniek'")
if cursor.fetchone():
    print("✅ Verified: uniek table exists")
else:
    print("❌ Error: uniek table was not created")

conn.close()

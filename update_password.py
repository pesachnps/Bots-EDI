#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
from django.contrib.auth.hashers import make_password

db_path = r'C:\Users\PGelfand\.bots\env\default\botssys\sqlitedb\botsdb'

# Generate Django password hash for 'bots'
password_hash = make_password('bots')

# Update the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("UPDATE auth_user SET password = ? WHERE username = 'bots'", (password_hash,))
conn.commit()

if cursor.rowcount > 0:
    print("✓ Password updated successfully")
    print("  Username: bots")
    print("  Password: bots")
else:
    print("✗ User 'bots' not found in database")

conn.close()

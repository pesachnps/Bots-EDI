#!/usr/bin/env python
"""Verify the ActivityLog table structure"""
import sqlite3
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_ROOT, 'env', 'botssys', 'sqlitedb', 'botsdb')

print(f"Connecting to database: {DB_PATH}")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Get table info
cursor.execute("PRAGMA table_info(usersys_activitylog)")
columns = cursor.fetchall()

print("\n=== usersys_activitylog table structure ===")
print(f"{'Column Name':<20} {'Type':<15} {'Not Null':<10} {'Default':<15}")
print("-" * 70)
for col in columns:
    col_id, name, dtype, not_null, default_val, pk = col
    print(f"{name:<20} {dtype:<15} {not_null:<10} {str(default_val):<15}")

# Get indexes
cursor.execute("PRAGMA index_list(usersys_activitylog)")
indexes = cursor.fetchall()

print("\n=== Indexes ===")
for idx in indexes:
    idx_seq, idx_name, idx_unique, idx_origin, idx_partial = idx
    print(f"  • {idx_name}")
    # Get index details
    cursor.execute(f"PRAGMA index_info({idx_name})")
    idx_columns = cursor.fetchall()
    for idx_col in idx_columns:
        seqno, cid, col_name = idx_col
        print(f"    - {col_name}")

# Test inserting a sample record
print("\n=== Testing insert ===")
try:
    from datetime import datetime
    cursor.execute('''
        INSERT INTO usersys_activitylog 
        (timestamp, user_type, user_id, user_name, action, resource_type, resource_id, details, ip_address, user_agent)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        'admin',
        1,
        'test_user',
        'test_action',
        'test_resource',
        '123',
        '{}',
        '127.0.0.1',
        'Test Agent'
    ))
    conn.commit()
    print("✅ Test record inserted successfully")
    
    # Read it back
    cursor.execute("SELECT * FROM usersys_activitylog ORDER BY id DESC LIMIT 1")
    record = cursor.fetchone()
    print(f"✅ Test record retrieved: {record}")
    
    # Clean up test record
    cursor.execute("DELETE FROM usersys_activitylog WHERE user_name = 'test_user'")
    conn.commit()
    print("✅ Test record cleaned up")
    
except Exception as e:
    print(f"❌ Error testing table: {e}")
    import traceback
    traceback.print_exc()

conn.close()
print("\n✅ Verification complete!")

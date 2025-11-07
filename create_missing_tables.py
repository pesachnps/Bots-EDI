#!/usr/bin/env python
"""Create all missing Bots EDI tables"""
import sqlite3
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get project root from environment or use script directory
PROJECT_ROOT = os.getenv('PROJECT_ROOT', os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, 'env', 'botssys', 'sqlitedb', 'botsdb')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create ta table (main transaction table)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ta (
        idta INTEGER PRIMARY KEY AUTOINCREMENT,
        statust INTEGER NOT NULL DEFAULT 0,
        status INTEGER NOT NULL DEFAULT 0,
        parent INTEGER,
        child INTEGER,
        script INTEGER NOT NULL DEFAULT 0,
        idroute VARCHAR(35) NOT NULL,
        fromchannel VARCHAR(35),
        tochannel VARCHAR(35),
        editype VARCHAR(35) NOT NULL,
        messagetype VARCHAR(35) NOT NULL,
        frompartner VARCHAR(70),
        topartner VARCHAR(70),
        filename VARCHAR(256),
        filesize INTEGER DEFAULT 0,
        nrmessages INTEGER DEFAULT 0,
        ts TIMESTAMP,
        confirmed INTEGER DEFAULT 0,
        confirmtype VARCHAR(35),
        confirmasked INTEGER DEFAULT 0,
        confirmidta INTEGER,
        retransmit INTEGER DEFAULT 0,
        frommail VARCHAR(256),
        tomail VARCHAR(256),
        charset VARCHAR(17),
        alt VARCHAR(70),
        merge INTEGER DEFAULT 0,
        rsrv INTEGER DEFAULT 0,
        botskey VARCHAR(70),
        cc VARCHAR(512),
        errortext VARCHAR(1024),
        processerrors INTEGER DEFAULT 0,
        lastopen TIMESTAMP,
        filedate TIMESTAMP,
        FOREIGN KEY (parent) REFERENCES ta(idta)
    )
''')

# Create indexes for ta table
cursor.execute('CREATE INDEX IF NOT EXISTS ta_parent ON ta(parent)')
cursor.execute('CREATE INDEX IF NOT EXISTS ta_child ON ta(child)')
cursor.execute('CREATE INDEX IF NOT EXISTS ta_statust ON ta(statust)')
cursor.execute('CREATE INDEX IF NOT EXISTS ta_status ON ta(status)')
cursor.execute('CREATE INDEX IF NOT EXISTS ta_ts ON ta(ts)')
cursor.execute('CREATE INDEX IF NOT EXISTS ta_idroute ON ta(idroute)')
cursor.execute('CREATE INDEX IF NOT EXISTS ta_botskey ON ta(botskey)')

# Create persist table (for persistent data)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS persist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        domein VARCHAR(35) NOT NULL,
        botskey VARCHAR(35) NOT NULL,
        ts TIMESTAMP,
        content TEXT,
        UNIQUE (domein, botskey)
    )
''')

# Create mutex table (for locking)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS mutex (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mutexk VARCHAR(35) NOT NULL UNIQUE,
        ts TIMESTAMP
    )
''')

conn.commit()
print("✅ Created all missing Bots EDI tables successfully")

# Verify tables were created
tables_to_check = ['ta', 'persist', 'mutex', 'uniek']
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
existing_tables = [row[0] for row in cursor.fetchall()]

print("\n✅ Verified tables:")
for table in tables_to_check:
    if table in existing_tables:
        print(f"  ✓ {table}")
    else:
        print(f"  ✗ {table} - MISSING!")

conn.close()

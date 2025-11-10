#!/usr/bin/env python
import os
import sys

# Set environment
os.environ['BOTSENV'] = 'default'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'env', 'default', 'config'))

# Import settings
from bots.botsinit import BotsConfig

# Read bots.ini
config = BotsConfig()
config_path = os.path.join(os.path.dirname(__file__), 'env', 'default', 'config', 'bots.ini')
config.read(config_path)

# Get BOTSSYS
BOTSSYS = config.get('directories', 'botssys', 'botssys')
print(f"BOTSSYS from bots.ini: {BOTSSYS}")

# Get database path
db_path = os.path.join(BOTSSYS, 'sqlitedb', 'botsdb')
print(f"Database path: {db_path}")

# Check if it exists
if os.path.exists(db_path):
    print(f"✓ Database file exists")
else:
    print(f"✗ Database file does NOT exist")
    
# Check our hardcoded path
our_path = r'C:\Users\PGelfand\.bots\env\default\botssys\sqlitedb\botsdb'
print(f"\nOur hardcoded path: {our_path}")
if os.path.exists(our_path):
    print(f"✓ Our database file exists")
else:
    print(f"✗ Our database file does NOT exist")

if db_path == our_path:
    print("\n✅ Paths match! Using the correct database.")
else:
    print(f"\n⚠️ Paths DO NOT match!")
    print(f"   App uses: {db_path}")
    print(f"   We modified: {our_path}")

#!/usr/bin/env python
"""Apply usersys migrations to create missing tables including ActivityLog"""
import os
import sys
import django

# Add the project to the Python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'env', 'default'))

# Set Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Setup Django
django.setup()

from django.core.management import call_command

print("Applying usersys migrations...")
try:
    # Show current migration status
    print("\n=== Current migration status ===")
    call_command('showmigrations', 'usersys')
    
    # Apply migrations
    print("\n=== Applying migrations ===")
    call_command('migrate', 'usersys', verbosity=2)
    
    print("\n✅ Migrations applied successfully!")
    
    # Verify the table was created
    print("\n=== Verifying tables ===")
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usersys_activitylog'")
    result = cursor.fetchone()
    
    if result:
        print("✅ usersys_activitylog table created successfully!")
    else:
        print("❌ usersys_activitylog table not found!")
    
    # Show all usersys tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'usersys_%' ORDER BY name")
    tables = cursor.fetchall()
    print("\n=== All usersys tables ===")
    for table in tables:
        print(f"  ✓ {table[0]}")
    
except Exception as e:
    print(f"❌ Error applying migrations: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

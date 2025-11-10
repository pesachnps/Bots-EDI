#!/usr/bin/env python
"""Create admin user directly in the database"""
import sqlite3
import os
import django
from django.conf import settings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Django settings
if not settings.configured:
    settings.configure(
        PASSWORD_HASHERS=[
            'django.contrib.auth.hashers.PBKDF2PasswordHasher',
        ]
    )
    django.setup()

# Import Django's password hasher
from django.contrib.auth.hashers import make_password as django_make_password

# Get project root from environment
PROJECT_ROOT = os.getenv('PROJECT_ROOT', os.path.dirname(os.path.abspath(__file__)))
# Use the actual database location
DB_PATH = r'C:\Users\PGelfand\.bots\env\default\botssys\sqlitedb\botsdb'

def create_superuser(username='admin', password='admin123', email='admin@bots.local'):
    """Create superuser in database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute('SELECT id FROM auth_user WHERE username = ?', (username,))
    if cursor.fetchone():
        print(f"User '{username}' already exists!")
        conn.close()
        return False
    
    # Create password hash using Django's hasher
    password_hash = django_make_password(password)
    
    # Insert user
    cursor.execute('''
        INSERT INTO auth_user (
            username, first_name, last_name, email, password,
            is_superuser, is_staff, is_active, date_joined
        ) VALUES (?, '', '', ?, ?, 1, 1, 1, datetime('now'))
    ''', (username, email, password_hash))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Superuser '{username}' created successfully!")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    print("   Login at: http://localhost:8080/admin")
    return True

if __name__ == "__main__":
    # Create both users from README
    print("Creating users from README...\n")
    create_superuser('edi_admin', 'Bots@2025!EDI', 'admin@bots.local')
    print()
    create_superuser('bots', 'bots', 'bots@bots.local')

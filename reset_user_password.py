#!/usr/bin/env python
"""Reset user password directly in the database"""
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

# Get database path - use the actual path where the database is located
DB_PATH = r'C:\Users\PGelfand\.bots\env\default\botssys\sqlitedb\botsdb'

def reset_password(username='bots', new_password='bots'):
    """Reset user password in database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute('SELECT id, username FROM auth_user WHERE username = ?', (username,))
    user = cursor.fetchone()
    
    if not user:
        print(f"✗ User '{username}' not found in database")
        conn.close()
        return False
    
    # Create password hash using Django's hasher
    password_hash = django_make_password(new_password)
    
    # Update password
    cursor.execute('UPDATE auth_user SET password = ? WHERE username = ?', 
                  (password_hash, username))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Password reset successfully for user '{username}'")
    print(f"   Username: {username}")
    print(f"   Password: {new_password}")
    print("   Login at: http://localhost:8080")
    return True

if __name__ == "__main__":
    print("Resetting passwords...\n")
    reset_password('bots', 'bots')
    print()
    reset_password('edi_admin', 'Bots@2025!EDI')

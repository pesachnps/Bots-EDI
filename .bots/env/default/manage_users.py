#!/usr/bin/env python
"""
Bots EDI User Management Script
This script helps manage Bots EDI web interface users.
"""

import os
import sys
import django
import bots.botsinit

def init_django():
    """Initialize Django environment"""
    bots.botsinit.generalinit()
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    django.setup()

def list_users():
    """List all users in the database"""
    from django.contrib.auth.models import User
    users = User.objects.all()
    
    print("\n=== Bots EDI Users ===")
    if not users:
        print("No users found in database.")
        return
    
    for user in users:
        print(f"Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Superuser: {user.is_superuser}")
        print(f"  Staff: {user.is_staff}")
        print(f"  Active: {user.is_active}")
        print("-" * 30)

def create_superuser(username, password, email=""):
    """Create a new superuser"""
    from django.contrib.auth.models import User
    
    if User.objects.filter(username=username).exists():
        print(f"User '{username}' already exists!")
        return False
    
    User.objects.create_superuser(username, email, password)
    print(f"Superuser '{username}' created successfully!")
    return True

def reset_password(username, new_password):
    """Reset password for existing user"""
    from django.contrib.auth.models import User
    
    try:
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()
        print(f"Password for user '{username}' has been reset to '{new_password}'")
        return True
    except User.DoesNotExist:
        print(f"User '{username}' does not exist!")
        return False

def main():
    """Main function"""
    init_django()
    
    if len(sys.argv) < 2:
        print("Bots EDI User Management")
        print("\nUsage:")
        print("  python manage_users.py list                    - List all users")
        print("  python manage_users.py create <user> <pass>    - Create superuser")
        print("  python manage_users.py reset <user> <pass>     - Reset password")
        print("\nDefault login credentials:")
        print("  Username: bots")
        print("  Password: bots")
        return
    
    command = sys.argv[1].lower()
    
    if command == "list":
        list_users()
    elif command == "create" and len(sys.argv) >= 4:
        username = sys.argv[2]
        password = sys.argv[3]
        email = sys.argv[4] if len(sys.argv) > 4 else f"{username}@bots.local"
        create_superuser(username, password, email)
    elif command == "reset" and len(sys.argv) >= 4:
        username = sys.argv[2]
        password = sys.argv[3]
        reset_password(username, password)
    else:
        print("Invalid command or missing arguments!")
        main()

if __name__ == "__main__":
    main()
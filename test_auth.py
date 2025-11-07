#!/usr/bin/env python
"""Test Django authentication"""
import os
import sys
import django
from dotenv import load_dotenv

# Set up project paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
ENV_DEFAULT = os.path.join(PROJECT_ROOT, 'env', 'default')

# Load environment variables
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

# Set environment variables for Django
os.environ['PROJECT_ROOT'] = PROJECT_ROOT
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Add to Python path - this allows Django to find settings
sys.path.insert(0, ENV_DEFAULT)

# Setup Django
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# List all users
print("All users in database:")
for user in User.objects.all():
    print(f"  {user.username} - Active: {user.is_active}, Staff: {user.is_staff}, Super: {user.is_superuser}")

print("\nTesting authentication...")

# Test edi_admin
print("\nTesting: edi_admin / Bots@2025!EDI")
user = authenticate(username='edi_admin', password='Bots@2025!EDI')
if user:
    print(f"✅ SUCCESS - {user.username} authenticated")
else:
    print("❌ FAILED - Authentication failed")
    # Check if user exists
    try:
        u = User.objects.get(username='edi_admin')
        print(f"   User exists: {u.username}")
        print(f"   Password hash: {u.password[:50]}...")
        print(f"   Check password: {u.check_password('Bots@2025!EDI')}")
    except User.DoesNotExist:
        print("   User does not exist!")

# Test bots
print("\nTesting: bots / bots")
user = authenticate(username='bots', password='bots')
if user:
    print(f"✅ SUCCESS - {user.username} authenticated")
else:
    print("❌ FAILED - Authentication failed")
    try:
        u = User.objects.get(username='bots')
        print(f"   User exists: {u.username}")
        print(f"   Password hash: {u.password[:50]}...")
        print(f"   Check password: {u.check_password('bots')}")
    except User.DoesNotExist:
        print("   User does not exist!")

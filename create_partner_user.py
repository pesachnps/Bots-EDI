#!/usr/bin/env python
"""Create test partner user for login testing"""
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

# Add to Python path
sys.path.insert(0, ENV_DEFAULT)

# Setup Django
django.setup()

from django.contrib.auth.hashers import make_password
from usersys.partner_models import Partner, PartnerUser

print("Creating test partner and user...")

# Create or get test partner
partner, created = Partner.objects.get_or_create(
    partner_id='TEST001',
    defaults={
        'name': 'Test Partner Company',
        'display_name': 'Test Partner',
        'contact_name': 'Test User',
        'contact_email': 'test@example.com',
        'status': 'active',
        'communication_method': 'both',
        'edi_format': 'X12',
    }
)

if created:
    print(f"✅ Created partner: {partner.name} ({partner.partner_id})")
else:
    print(f"ℹ️  Partner already exists: {partner.name} ({partner.partner_id})")

# Create or update test partner user
try:
    user = PartnerUser.objects.get(username='testpartner')
    user.password_hash = make_password('Test123!')
    user.is_active = True
    user.save()
    print(f"ℹ️  Updated existing user: {user.username}")
except PartnerUser.DoesNotExist:
    user = PartnerUser.objects.create(
        partner=partner,
        username='testpartner',
        email='testpartner@example.com',
        password_hash=make_password('Test123!'),
        first_name='Test',
        last_name='Partner',
        role='admin',
        is_active=True
    )
    print(f"✅ Created user: {user.username}")

print("\n" + "="*60)
print("TEST CREDENTIALS")
print("="*60)
print(f"Partner Login URL: http://localhost:8080/partner-portal/login")
print(f"Username: testpartner")
print(f"Password: Test123!")
print(f"Partner: {partner.name} ({partner.partner_id})")
print("="*60)

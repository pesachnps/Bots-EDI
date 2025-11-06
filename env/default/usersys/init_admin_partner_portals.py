#!/usr/bin/env python
"""
Initialize Admin Dashboard & Partner Portal
Setup script to configure the system for first use
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command
from usersys.partner_models import Partner, PartnerUser


def main():
    print("=" * 60)
    print("Admin Dashboard & Partner Portal - Initialization")
    print("=" * 60)
    print()
    
    # Step 1: Run migrations
    print("Step 1: Running database migrations...")
    try:
        call_command('migrate', 'usersys', verbosity=1)
        print("✓ Migrations complete")
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        return
    
    print()
    
    # Step 2: Initialize partner portal
    print("Step 2: Initializing partner portal...")
    try:
        call_command('init_partner_portal', verbosity=1)
        print("✓ Partner portal initialized")
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
    
    print()
    
    # Step 3: Check for partners
    print("Step 3: Checking partner configuration...")
    partner_count = Partner.objects.count()
    active_partners = Partner.objects.filter(status='active').count()
    
    print(f"  Total partners: {partner_count}")
    print(f"  Active partners: {active_partners}")
    
    if partner_count == 0:
        print()
        print("⚠ No partners found!")
        print("  Create partners using Django admin or the Modern EDI Interface")
        print("  URL: http://localhost:8080/admin/usersys/partner/")
    
    print()
    
    # Step 4: Check for partner users
    print("Step 4: Checking partner users...")
    user_count = PartnerUser.objects.count()
    active_users = PartnerUser.objects.filter(is_active=True).count()
    
    print(f"  Total partner users: {user_count}")
    print(f"  Active users: {active_users}")
    
    if user_count == 0:
        print()
        print("⚠ No partner users found!")
        print("  Create sample users with:")
        print("  python manage.py init_partner_portal --create-sample")
    
    print()
    
    # Step 5: Display access information
    print("=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print()
    print("Access URLs:")
    print("  Modern EDI Interface:  http://localhost:8080/modern-edi/")
    print("  Admin Dashboard:       http://localhost:8080/modern-edi/admin/")
    print("  Partner Portal:        http://localhost:8080/modern-edi/partner-portal/")
    print()
    print("API Endpoints:")
    print("  Admin API:             http://localhost:8080/modern-edi/api/v1/admin/")
    print("  Partner Portal API:    http://localhost:8080/modern-edi/api/v1/partner-portal/")
    print()
    print("Next Steps:")
    print("  1. Start the server: bots-webserver")
    print("  2. Create partners via Django admin")
    print("  3. Create partner users via admin dashboard")
    print("  4. Test partner portal login")
    print()
    print("For sample data:")
    print("  python manage.py init_partner_portal --create-sample")
    print()


if __name__ == '__main__':
    main()

#!/usr/bin/env python
"""
Initialize Modern EDI Interface
Creates directory structure and runs database migrations
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command
from django.conf import settings


def create_directory_structure():
    """Create the modern-edi folder structure"""
    
    # Get botssys directory from settings
    botssys_dir = getattr(settings, 'BOTSSYS', 'botssys')
    modern_edi_base = os.path.join(botssys_dir, 'modern-edi')
    
    folders = ['inbox', 'received', 'outbox', 'sent', 'deleted']
    
    print("Creating Modern EDI directory structure...")
    
    for folder in folders:
        folder_path = os.path.join(modern_edi_base, folder)
        os.makedirs(folder_path, exist_ok=True)
        print(f"  ✓ Created {folder_path}")
    
    # Set appropriate permissions (read/write for owner, read for group)
    try:
        for folder in folders:
            folder_path = os.path.join(modern_edi_base, folder)
            os.chmod(folder_path, 0o750)
    except Exception as e:
        print(f"  Warning: Could not set permissions: {e}")
    
    print("✓ Directory structure created successfully")


def run_migrations():
    """Run database migrations for modern EDI models"""
    
    print("\nRunning database migrations...")
    
    try:
        call_command('migrate', 'usersys', verbosity=1)
        print("✓ Migrations completed successfully")
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        return False
    
    return True


def verify_setup():
    """Verify the setup is complete"""
    
    print("\nVerifying setup...")
    
    # Check if models are accessible
    try:
        from usersys.modern_edi_models import EDITransaction, TransactionHistory
        print("  ✓ Models imported successfully")
    except ImportError as e:
        print(f"  ✗ Could not import models: {e}")
        return False
    
    # Check if directories exist
    botssys_dir = getattr(settings, 'BOTSSYS', 'botssys')
    modern_edi_base = os.path.join(botssys_dir, 'modern-edi')
    
    folders = ['inbox', 'received', 'outbox', 'sent', 'deleted']
    for folder in folders:
        folder_path = os.path.join(modern_edi_base, folder)
        if not os.path.exists(folder_path):
            print(f"  ✗ Directory missing: {folder_path}")
            return False
    
    print("  ✓ All directories exist")
    print("\n✓ Setup verification complete")
    
    return True


def main():
    """Main initialization function"""
    
    print("=" * 60)
    print("Modern EDI Interface Initialization")
    print("=" * 60)
    
    # Create directory structure
    create_directory_structure()
    
    # Run migrations
    if not run_migrations():
        print("\n✗ Initialization failed during migrations")
        sys.exit(1)
    
    # Verify setup
    if not verify_setup():
        print("\n✗ Initialization failed during verification")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✓ Modern EDI Interface initialized successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Start the Bots webserver: bots-webserver")
    print("  2. Access the modern interface at: http://localhost:8080/modern-edi/")
    print("=" * 60)


if __name__ == '__main__':
    main()

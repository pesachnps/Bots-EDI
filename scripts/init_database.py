#!/usr/bin/env python
"""
Initialize Bots EDI database and create default users
"""

import os
import sys
import django

# Add env/default to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'env', 'default'))

def init_django():
    """Initialize Django environment"""
    import bots.botsinit
    bots.botsinit.generalinit()
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    django.setup()

def run_migrations():
    """Run Django migrations"""
    from django.core.management import call_command
    
    print("Running database migrations...")
    try:
        call_command('migrate', verbosity=1)
        print("✅ Migrations completed successfully")
        return True
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def create_superuser(username='admin', password='admin123', email='admin@bots.local'):
    """Create default superuser"""
    from django.contrib.auth.models import User
    
    if User.objects.filter(username=username).exists():
        print(f"ℹ️  User '{username}' already exists")
        return False
    
    User.objects.create_superuser(username, email, password)
    print(f"✅ Superuser '{username}' created")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    print("   ⚠️  CHANGE THIS PASSWORD IN PRODUCTION!")
    return True

def initialize_api_permissions():
    """Initialize default API permissions"""
    from usersys.api_models import APIPermission
    
    default_permissions = [
        ('file_upload', 'Upload EDI Files', 'Allow uploading EDI files to the system'),
        ('file_download', 'Download EDI Files', 'Allow downloading processed EDI files'),
        ('file_list', 'List Files', 'Allow listing available files'),
        ('file_delete', 'Delete Files', 'Allow deleting files'),
        ('route_execute', 'Execute Routes', 'Allow executing Bots routes'),
        ('route_list', 'List Routes', 'Allow listing available routes'),
        ('report_view', 'View Reports', 'Allow viewing translation reports'),
        ('report_download', 'Download Reports', 'Allow downloading reports'),
        ('partner_view', 'View Partners', 'Allow viewing trading partners'),
        ('partner_manage', 'Manage Partners', 'Allow managing trading partners'),
        ('translate_view', 'View Translations', 'Allow viewing translation status'),
        ('channel_view', 'View Channels', 'Allow viewing communication channels'),
        ('admin_access', 'Full Admin Access', 'Full administrative access to all API functions'),
    ]
    
    created_count = 0
    for code, name, description in default_permissions:
        perm, created = APIPermission.objects.get_or_create(
            code=code,
            defaults={'name': name, 'description': description, 'is_active': True}
        )
        if created:
            created_count += 1
    
    print(f"✅ Initialized {created_count} API permissions")
    return True

def create_default_api_key(username='admin'):
    """Create default API key for admin user"""
    from django.contrib.auth.models import User
    from usersys.api_models import APIKey, APIPermission
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        print(f"❌ User '{username}' not found")
        return False
    
    # Check if user already has an API key
    if APIKey.objects.filter(user=user).exists():
        print(f"ℹ️  User '{username}' already has API key(s)")
        return False
    
    # Create API key with all permissions
    api_key = APIKey.objects.create(
        name=f'{username} Default API Key',
        user=user,
        is_active=True,
        rate_limit=1000
    )
    
    # Add all permissions
    permissions = APIPermission.objects.all()
    api_key.permissions.set(permissions)
    
    print(f"✅ API key created for '{username}'")
    print(f"   Key: {api_key.key}")
    print("   ⚠️  SAVE THIS KEY SECURELY - IT WON'T BE SHOWN AGAIN!")
    return True

def main():
    """Main initialization function"""
    print("=" * 60)
    print("Bots EDI Database Initialization")
    print("=" * 60)
    print()
    
    # Initialize Django
    init_django()
    
    # Run migrations
    if not run_migrations():
        print("\n❌ Database initialization failed")
        sys.exit(1)
    
    print()
    
    # Create superuser
    create_superuser()
    
    print()
    
    # Initialize API permissions
    initialize_api_permissions()
    
    print()
    
    # Create default API key
    create_default_api_key()
    
    print()
    print("=" * 60)
    print("✅ Database initialization complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Change the default admin password")
    print("2. Start the webserver: bots-webserver")
    print("3. Access the admin interface: http://localhost:8080/admin")
    print()

if __name__ == "__main__":
    main()

#!/usr/bin/env python
"""
Bots EDI API Management Script
Command-line tool for managing API keys and permissions
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

def list_api_keys():
    """List all API keys"""
    from usersys.api_models import APIKey
    
    keys = APIKey.objects.all()
    
    print("\n=== Bots EDI API Keys ===")
    if not keys:
        print("No API keys found.")
        return
    
    for key in keys:
        status = "✅ Active" if key.is_active else "❌ Inactive"
        print(f"\n{status} {key.name}")
        print(f"  Key: {key.key}")
        print(f"  User: {key.user.username}")
        print(f"  Rate Limit: {key.current_usage}/{key.rate_limit} per hour")
        print(f"  Permissions: {', '.join([p.code for p in key.permissions.all()])}")
        print(f"  Created: {key.created_at}")
        if key.last_used:
            print(f"  Last Used: {key.last_used}")
        print("-" * 60)

def create_api_key(name, username, permissions_list=None):
    """Create a new API key"""
    from django.contrib.auth.models import User
    from usersys.api_models import APIKey, APIPermission
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        print(f"❌ Error: User '{username}' does not exist!")
        return False
    
    # Create API key
    api_key = APIKey.objects.create(
        name=name,
        user=user,
        is_active=True,
        rate_limit=1000
    )
    
    # Add permissions
    if permissions_list:
        for perm_code in permissions_list:
            try:
                permission = APIPermission.objects.get(code=perm_code)
                api_key.permissions.add(permission)
            except APIPermission.DoesNotExist:
                print(f"⚠️  Warning: Permission '{perm_code}' does not exist, skipping...")
    
    print(f"\n✅ API Key created successfully!")
    print(f"   Name: {api_key.name}")
    print(f"   Key: {api_key.key}")
    print(f"   User: {api_key.user.username}")
    print("\n⚠️  IMPORTANT: Save this API key securely. It won't be shown again!")
    return True

def list_permissions():
    """List all available permissions"""
    from usersys.api_models import APIPermission
    
    permissions = APIPermission.objects.all()
    
    print("\n=== Available API Permissions ===")
    if not permissions:
        print("No permissions found. Run 'initialize_permissions' first.")
        return
    
    for perm in permissions:
        status = "✅" if perm.is_active else "❌"
        print(f"{status} {perm.code}: {perm.name}")
        if perm.description:
            print(f"   {perm.description}")

def initialize_permissions():
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
            print(f"✅ Created permission: {code}")
    
    print(f"\n✅ Initialized {created_count} permissions")

def revoke_api_key(key_value):
    """Revoke (deactivate) an API key"""
    from usersys.api_models import APIKey
    
    try:
        api_key = APIKey.objects.get(key=key_value)
        api_key.is_active = False
        api_key.save()
        print(f"✅ API key '{api_key.name}' has been revoked")
        return True
    except APIKey.DoesNotExist:
        print(f"❌ Error: API key not found")
        return False

def view_audit_logs(limit=50):
    """View recent API audit logs"""
    from usersys.api_models import APIAuditLog
    
    logs = APIAuditLog.objects.all().order_by('-timestamp')[:limit]
    
    print(f"\n=== Recent API Activity (Last {limit} requests) ===")
    if not logs:
        print("No audit logs found.")
        return
    
    for log in logs:
        status_icon = "✅" if log.response_status == 'success' else "❌"
        print(f"\n{status_icon} {log.timestamp}")
        print(f"   API Key: {log.api_key.name if log.api_key else 'Unknown'}")
        print(f"   Endpoint: {log.method} {log.endpoint}")
        print(f"   Status: {log.response_status} ({log.response_code})")
        print(f"   IP: {log.ip_address}")
        print(f"   Duration: {log.duration_ms}ms")

def main():
    """Main function"""
    init_django()
    
    if len(sys.argv) < 2:
        print("🔐 Bots EDI API Management Tool")
        print("\nUsage:")
        print("  python api_management.py list                          - List all API keys")
        print("  python api_management.py create <name> <user>          - Create API key")
        print("  python api_management.py permissions                   - List permissions")
        print("  python api_management.py init_permissions              - Initialize default permissions")
        print("  python api_management.py revoke <api_key>              - Revoke API key")
        print("  python api_management.py audit [limit]                 - View audit logs")
        print("\nExamples:")
        print("  python api_management.py create \"Production API\" edi_admin")
        print("  python api_management.py audit 100")
        return
    
    command = sys.argv[1].lower()
    
    if command == "list":
        list_api_keys()
    elif command == "create" and len(sys.argv) >= 4:
        name = sys.argv[2]
        username = sys.argv[3]
        permissions = sys.argv[4:] if len(sys.argv) > 4 else []
        create_api_key(name, username, permissions)
    elif command == "permissions":
        list_permissions()
    elif command == "init_permissions":
        initialize_permissions()
    elif command == "revoke" and len(sys.argv) >= 3:
        key_value = sys.argv[2]
        revoke_api_key(key_value)
    elif command == "audit":
        limit = int(sys.argv[2]) if len(sys.argv) >= 3 else 50
        view_audit_logs(limit)
    else:
        print("❌ Invalid command or missing arguments!")
        main()

if __name__ == "__main__":
    main()

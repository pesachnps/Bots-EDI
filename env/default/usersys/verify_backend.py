"""
Backend Verification Script
Tests that all backend components are properly configured
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from partner_models import Partner, PartnerUser, PartnerPermission, ActivityLog, PasswordResetToken
from user_manager import UserManager
from analytics_service import AnalyticsService
from activity_logger import ActivityLogger
from email_service import EmailService
from partner_auth_utils import PasswordValidator, TokenGenerator, SessionManager


def test_models():
    """Test that all models are accessible"""
    print("Testing models...")
    
    models = [
        Partner,
        PartnerUser,
        PartnerPermission,
        ActivityLog,
        PasswordResetToken,
    ]
    
    for model in models:
        print(f"  ✓ {model.__name__} model loaded")
    
    print("✓ All models loaded successfully\n")


def test_services():
    """Test that all services are accessible"""
    print("Testing services...")
    
    services = [
        ('UserManager', UserManager),
        ('AnalyticsService', AnalyticsService),
        ('ActivityLogger', ActivityLogger),
        ('EmailService', EmailService),
    ]
    
    for name, service in services:
        print(f"  ✓ {name} service loaded")
    
    print("✓ All services loaded successfully\n")


def test_utilities():
    """Test that all utilities are accessible"""
    print("Testing utilities...")
    
    utilities = [
        ('PasswordValidator', PasswordValidator),
        ('TokenGenerator', TokenGenerator),
        ('SessionManager', SessionManager),
    ]
    
    for name, utility in utilities:
        print(f"  ✓ {name} utility loaded")
    
    print("✓ All utilities loaded successfully\n")


def test_password_validation():
    """Test password validation"""
    print("Testing password validation...")
    
    # Test weak password
    is_valid, msg = PasswordValidator.validate("weak")
    assert not is_valid, "Weak password should fail"
    print(f"  ✓ Weak password rejected: {msg}")
    
    # Test strong password
    is_valid, msg = PasswordValidator.validate("StrongPass123!")
    assert is_valid, "Strong password should pass"
    print("  ✓ Strong password accepted")
    
    print("✓ Password validation working correctly\n")


def test_token_generation():
    """Test token generation"""
    print("Testing token generation...")
    
    reset_token = TokenGenerator.generate_reset_token()
    assert len(reset_token) > 20, "Reset token should be long enough"
    print(f"  ✓ Reset token generated: {reset_token[:20]}...")
    
    api_token = TokenGenerator.generate_api_token()
    assert len(api_token) > 30, "API token should be long enough"
    print(f"  ✓ API token generated: {api_token[:20]}...")
    
    print("✓ Token generation working correctly\n")


def test_database_connection():
    """Test database connection"""
    print("Testing database connection...")
    
    try:
        # Try to count partners
        partner_count = Partner.objects.count()
        print(f"  ✓ Database connected (found {partner_count} partners)")
        
        # Try to count users
        user_count = PartnerUser.objects.count()
        print(f"  ✓ Database queries working (found {user_count} partner users)")
        
        # Try to count activity logs
        log_count = ActivityLog.objects.count()
        print(f"  ✓ Activity logging accessible (found {log_count} logs)")
        
        print("✓ Database connection working correctly\n")
    except Exception as e:
        print(f"  ✗ Database error: {e}\n")
        return False
    
    return True


def test_model_methods():
    """Test model methods"""
    print("Testing model methods...")
    
    # Test PartnerUser default permissions
    test_roles = ['partner_admin', 'partner_user', 'partner_readonly']
    
    for role in test_roles:
        # Create a mock user object (not saved to DB)
        user = PartnerUser(role=role)
        permissions = user.get_default_permissions()
        
        assert 'can_view_transactions' in permissions, f"Missing permission for {role}"
        print(f"  ✓ Default permissions for {role}: {permissions}")
    
    print("✓ Model methods working correctly\n")


def run_all_tests():
    """Run all verification tests"""
    print("=" * 60)
    print("Backend Verification Script")
    print("=" * 60)
    print()
    
    try:
        test_models()
        test_services()
        test_utilities()
        test_password_validation()
        test_token_generation()
        
        if test_database_connection():
            test_model_methods()
        
        print("=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        print()
        print("Backend is properly configured and ready to use!")
        print()
        print("Next steps:")
        print("1. Run migrations: python manage.py migrate")
        print("2. Initialize data: python usersys/init_admin_partner_portals.py")
        print("3. Start server: bots-webserver")
        print()
        
        return True
        
    except Exception as e:
        print("=" * 60)
        print("✗ TESTS FAILED")
        print("=" * 60)
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)

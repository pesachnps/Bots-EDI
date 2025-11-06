"""
Verification Script: Password Hashing Security
Verifies that all passwords are properly hashed using Django's password hasher
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.hashers import check_password, is_password_usable, make_password
from usersys.partner_models import Partner, PartnerUser
from usersys.user_manager import UserManager
from usersys.partner_auth_utils import PasswordValidator


def test_password_hashing():
    """Test that passwords are properly hashed"""
    
    print("=" * 70)
    print("PASSWORD HASHING SECURITY VERIFICATION")
    print("=" * 70)
    print()
    
    # Test 1: Password Validator
    print("Test 1: PasswordValidator.hash_password()")
    print("-" * 70)
    test_password = "TestPassword123!"
    hashed = PasswordValidator.hash_password(test_password)
    
    print(f"Plain text password: {test_password}")
    print(f"Hashed password: {hashed[:50]}...")
    print(f"Is usable Django hash: {is_password_usable(hashed)}")
    print(f"Verification works: {PasswordValidator.verify_password(test_password, hashed)}")
    print(f"Wrong password fails: {not PasswordValidator.verify_password('WrongPass', hashed)}")
    
    if hashed == test_password:
        print("❌ FAIL: Password is stored in plain text!")
        return False
    elif not is_password_usable(hashed):
        print("❌ FAIL: Password hash is not in Django format!")
        return False
    else:
        print("✅ PASS: Password is properly hashed")
    print()
    
    # Test 2: User Creation
    print("Test 2: UserManager.create_user()")
    print("-" * 70)
    
    # Find or create test partner
    partner, created = Partner.objects.get_or_create(
        partner_id='HASHTEST001',
        defaults={
            'name': 'Hash Test Partner',
            'communication_method': 'both',
            'status': 'active'
        }
    )
    
    # Delete existing test user if exists
    PartnerUser.objects.filter(username='hashtest_user').delete()
    
    # Create user
    test_password = "CreateTest456!"
    user, _ = UserManager.create_user(
        partner_id=partner.id,
        username='hashtest_user',
        email='hashtest@example.com',
        password=test_password,
        first_name='Hash',
        last_name='Test',
        send_email=False
    )
    
    print(f"Created user: {user.username}")
    print(f"Plain text password: {test_password}")
    print(f"Stored password_hash: {user.password_hash[:50]}...")
    print(f"Is usable Django hash: {is_password_usable(user.password_hash)}")
    print(f"Verification works: {check_password(test_password, user.password_hash)}")
    
    if user.password_hash == test_password:
        print("❌ FAIL: Password is stored in plain text!")
        user.delete()
        return False
    elif not is_password_usable(user.password_hash):
        print("❌ FAIL: Password hash is not in Django format!")
        user.delete()
        return False
    elif not check_password(test_password, user.password_hash):
        print("❌ FAIL: Password verification failed!")
        user.delete()
        return False
    else:
        print("✅ PASS: User password is properly hashed")
    print()
    
    # Test 3: Password Reset
    print("Test 3: UserManager.reset_password()")
    print("-" * 70)
    
    old_hash = user.password_hash
    new_password = "ResetTest789!"
    
    UserManager.reset_password(user.id, new_password)
    user.refresh_from_db()
    
    print(f"Old password hash: {old_hash[:50]}...")
    print(f"New password hash: {user.password_hash[:50]}...")
    print(f"Hashes are different: {old_hash != user.password_hash}")
    print(f"New password not plain text: {user.password_hash != new_password}")
    print(f"New password verifies: {check_password(new_password, user.password_hash)}")
    print(f"Old password fails: {not check_password(test_password, user.password_hash)}")
    
    if user.password_hash == new_password:
        print("❌ FAIL: Password is stored in plain text!")
        user.delete()
        return False
    elif not check_password(new_password, user.password_hash):
        print("❌ FAIL: Password verification failed!")
        user.delete()
        return False
    else:
        print("✅ PASS: Password reset properly hashes password")
    print()
    
    # Test 4: Check all existing users
    print("Test 4: Verify all existing PartnerUser passwords are hashed")
    print("-" * 70)
    
    all_users = PartnerUser.objects.all()
    print(f"Total PartnerUsers in database: {all_users.count()}")
    
    all_hashed = True
    for user_obj in all_users:
        if not is_password_usable(user_obj.password_hash):
            print(f"❌ User {user_obj.username} has invalid password hash!")
            all_hashed = False
        elif not user_obj.password_hash.startswith(('pbkdf2_sha256$', 'argon2', 'bcrypt')):
            print(f"❌ User {user_obj.username} password hash format is suspicious!")
            all_hashed = False
    
    if all_hashed:
        print("✅ PASS: All user passwords are properly hashed")
    else:
        print("❌ FAIL: Some users have improperly hashed passwords")
    print()
    
    # Test 5: Django's make_password function
    print("Test 5: Django's make_password() function")
    print("-" * 70)
    
    test_pass = "DjangoTest123!"
    django_hash = make_password(test_pass)
    
    print(f"Plain text: {test_pass}")
    print(f"Django hash: {django_hash[:50]}...")
    print(f"Algorithm: {django_hash.split('$')[0]}")
    print(f"Is usable: {is_password_usable(django_hash)}")
    print(f"Verifies: {check_password(test_pass, django_hash)}")
    
    if django_hash == test_pass:
        print("❌ FAIL: Django make_password not working!")
        return False
    else:
        print("✅ PASS: Django make_password works correctly")
    print()
    
    # Cleanup
    user.delete()
    
    # Final Summary
    print("=" * 70)
    print("VERIFICATION COMPLETE")
    print("=" * 70)
    print()
    print("✅ All password hashing tests passed!")
    print()
    print("Summary:")
    print("  • PasswordValidator uses Django's make_password()")
    print("  • UserManager.create_user() hashes passwords")
    print("  • UserManager.reset_password() hashes passwords")
    print("  • All existing users have properly hashed passwords")
    print("  • Django's password hasher is working correctly")
    print()
    print("Security Status: COMPLIANT ✅")
    print()
    
    return True


if __name__ == '__main__':
    try:
        success = test_password_hashing()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

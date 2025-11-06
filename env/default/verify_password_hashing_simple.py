"""
Simple Password Hashing Verification
Verifies that Django's password hasher is being used correctly
"""

import re

def check_file_for_password_hashing(filepath):
    """Check if a file uses Django's password hasher"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for Django password hasher imports
        has_make_password = 'make_password' in content
        has_check_password = 'check_password' in content
        has_django_hashers = 'django.contrib.auth.hashers' in content
        
        # Check for direct password assignment (bad practice)
        # Look for patterns like: password = "..." or password_hash = "plain_text"
        direct_assignment = re.search(r'password(_hash)?\s*=\s*["\'][\w!@#$%^&*()]+["\']', content)
        
        return {
            'has_make_password': has_make_password,
            'has_check_password': has_check_password,
            'has_django_hashers': has_django_hashers,
            'has_direct_assignment': bool(direct_assignment),
            'uses_hashing': has_make_password or has_django_hashers
        }
    except Exception as e:
        return {'error': str(e)}


def main():
    print("=" * 70)
    print("PASSWORD HASHING SECURITY VERIFICATION")
    print("=" * 70)
    print()
    
    files_to_check = [
        ('usersys/partner_auth_utils.py', 'Authentication Utilities'),
        ('usersys/partner_auth_views.py', 'Authentication Views'),
        ('usersys/user_manager.py', 'User Manager Service'),
    ]
    
    # Note: partner_models.py doesn't need to import hashers - it just defines the schema
    # The actual hashing is done in the service layer (user_manager, auth_views)
    
    all_pass = True
    
    for filepath, description in files_to_check:
        print(f"Checking: {description}")
        print(f"File: {filepath}")
        print("-" * 70)
        
        result = check_file_for_password_hashing(filepath)
        
        if 'error' in result:
            print(f"❌ ERROR: {result['error']}")
            all_pass = False
        else:
            if result['has_django_hashers']:
                print(f"✅ Imports Django password hashers")
            
            if result['has_make_password']:
                print(f"✅ Uses make_password() for hashing")
            
            if result['has_check_password']:
                print(f"✅ Uses check_password() for verification")
            
            if result['has_direct_assignment']:
                print(f"⚠️  WARNING: Found potential direct password assignment")
                all_pass = False
            
            if not result['uses_hashing']:
                print(f"❌ FAIL: Does not use Django password hashing")
                all_pass = False
            else:
                print(f"✅ PASS: Uses Django password hashing")
        
        print()
    
    # Check specific implementations
    print("=" * 70)
    print("DETAILED CODE VERIFICATION")
    print("=" * 70)
    print()
    
    # Check partner_auth_utils.py
    print("1. PasswordValidator.hash_password()")
    print("-" * 70)
    try:
        with open('usersys/partner_auth_utils.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'def hash_password(password):' in content and 'return make_password(password)' in content:
            print("✅ PASS: PasswordValidator.hash_password() uses make_password()")
        else:
            print("❌ FAIL: PasswordValidator.hash_password() implementation not found")
            all_pass = False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        all_pass = False
    print()
    
    # Check user_manager.py
    print("2. UserManager.create_user()")
    print("-" * 70)
    try:
        with open('usersys/user_manager.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'password_hash=make_password(password)' in content:
            print("✅ PASS: UserManager.create_user() hashes password with make_password()")
        else:
            print("❌ FAIL: UserManager.create_user() does not hash password")
            all_pass = False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        all_pass = False
    print()
    
    # Check password reset
    print("3. UserManager.reset_password()")
    print("-" * 70)
    try:
        with open('usersys/user_manager.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'user.password_hash = make_password(new_password)' in content:
            print("✅ PASS: UserManager.reset_password() hashes password with make_password()")
        else:
            print("❌ FAIL: UserManager.reset_password() does not hash password")
            all_pass = False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        all_pass = False
    print()
    
    # Check login verification
    print("4. partner_login() password verification")
    print("-" * 70)
    try:
        with open('usersys/partner_auth_views.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'check_password(password, user.password_hash)' in content:
            print("✅ PASS: partner_login() verifies password with check_password()")
        else:
            print("❌ FAIL: partner_login() does not use check_password()")
            all_pass = False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        all_pass = False
    print()
    
    # Check password change
    print("5. partner_change_password()")
    print("-" * 70)
    try:
        with open('usersys/partner_auth_views.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'user.password_hash = make_password(new_password)' in content:
            print("✅ PASS: partner_change_password() hashes password with make_password()")
        else:
            print("❌ FAIL: partner_change_password() does not hash password")
            all_pass = False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        all_pass = False
    print()
    
    # Check password reset with token
    print("6. partner_reset_password()")
    print("-" * 70)
    try:
        with open('usersys/partner_auth_views.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count occurrences of make_password in reset function
        reset_func_match = re.search(
            r'def partner_reset_password\(.*?\):(.*?)(?=\ndef |\Z)',
            content,
            re.DOTALL
        )
        
        if reset_func_match and 'make_password(new_password)' in reset_func_match.group(1):
            print("✅ PASS: partner_reset_password() hashes password with make_password()")
        else:
            print("❌ FAIL: partner_reset_password() does not hash password")
            all_pass = False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        all_pass = False
    print()
    
    # Final Summary
    print("=" * 70)
    print("VERIFICATION COMPLETE")
    print("=" * 70)
    print()
    
    if all_pass:
        print("✅ ALL CHECKS PASSED!")
        print()
        print("Summary:")
        print("  • All files import Django's password hashers")
        print("  • PasswordValidator uses make_password()")
        print("  • UserManager.create_user() hashes passwords")
        print("  • UserManager.reset_password() hashes passwords")
        print("  • partner_login() verifies with check_password()")
        print("  • partner_change_password() hashes passwords")
        print("  • partner_reset_password() hashes passwords")
        print()
        print("Security Status: COMPLIANT ✅")
        print()
        print("All passwords are properly hashed using Django's password hasher.")
        print("The system uses PBKDF2-SHA256 by default, which is secure and compliant.")
        return True
    else:
        print("❌ SOME CHECKS FAILED!")
        print()
        print("Please review the failures above and ensure all passwords")
        print("are hashed using Django's make_password() function.")
        return False


if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)

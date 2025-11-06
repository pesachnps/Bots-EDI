# Password Security Guide for Developers

## Quick Reference

When working with passwords in this system, always follow these guidelines:

## ✅ DO: Use Django's Password Hasher

### Hashing Passwords

```python
from django.contrib.auth.hashers import make_password

# Hash a password before storing
hashed_password = make_password(plain_text_password)
user.password_hash = hashed_password
user.save()
```

### Verifying Passwords

```python
from django.contrib.auth.hashers import check_password

# Verify a password
if check_password(plain_text_password, user.password_hash):
    # Password is correct
    print("Login successful")
else:
    # Password is incorrect
    print("Invalid password")
```

### Using PasswordValidator Utility

```python
from usersys.partner_auth_utils import PasswordValidator

# Hash a password
hashed = PasswordValidator.hash_password(plain_password)

# Verify a password
is_valid = PasswordValidator.verify_password(plain_password, hashed)

# Validate password complexity
is_valid, error_msg = PasswordValidator.validate(plain_password)
if not is_valid:
    print(f"Password validation failed: {error_msg}")
```

## ❌ DON'T: Store Plain Text Passwords

### Never Do This

```python
# ❌ WRONG - Plain text password
user.password = "MyPassword123!"
user.save()

# ❌ WRONG - Direct comparison
if user.password == input_password:
    login_user()

# ❌ WRONG - Storing in logs
logger.info(f"User logged in with password: {password}")
```

### Always Do This

```python
# ✅ CORRECT - Hash before storing
user.password_hash = make_password("MyPassword123!")
user.save()

# ✅ CORRECT - Use check_password
if check_password(input_password, user.password_hash):
    login_user()

# ✅ CORRECT - Never log passwords
logger.info(f"User {username} logged in successfully")
```

## Common Scenarios

### 1. Creating a New User

```python
from usersys.user_manager import UserManager

# Use UserManager - it handles hashing automatically
user, password = UserManager.create_user(
    partner_id=partner.id,
    username='newuser',
    email='user@example.com',
    password='SecurePass123!',  # Will be hashed automatically
    first_name='John',
    last_name='Doe',
    send_email=False
)

# Password is now hashed in user.password_hash
```

### 2. Resetting a Password

```python
from usersys.user_manager import UserManager

# Use UserManager - it handles hashing automatically
UserManager.reset_password(
    user_id=user.id,
    new_password='NewSecurePass456!'  # Will be hashed automatically
)
```

### 3. Changing Password (User-Initiated)

```python
from django.contrib.auth.hashers import check_password, make_password

# Verify current password
if not check_password(current_password, user.password_hash):
    return JsonResponse({'error': 'Current password is incorrect'}, status=400)

# Hash and save new password
user.password_hash = make_password(new_password)
user.save(update_fields=['password_hash'])
```

### 4. Login Authentication

```python
from django.contrib.auth.hashers import check_password

# Get user
user = PartnerUser.objects.get(username=username)

# Verify password
if not check_password(password, user.password_hash):
    user.increment_failed_attempts()
    return JsonResponse({'error': 'Invalid credentials'}, status=401)

# Password is correct - proceed with login
user.reset_failed_attempts()
create_session(request, user)
```

## Password Complexity Requirements

All passwords must meet these requirements:

- ✅ Minimum 8 characters
- ✅ At least one uppercase letter (A-Z)
- ✅ At least one lowercase letter (a-z)
- ✅ At least one number (0-9)
- ✅ At least one special character (!@#$%^&*(),.?":{}|<>)

### Validating Password Complexity

```python
from usersys.partner_auth_utils import PasswordValidator

is_valid, error_msg = PasswordValidator.validate(password)
if not is_valid:
    raise ValidationError(error_msg)
```

## Security Best Practices

### 1. Never Log Passwords

```python
# ❌ WRONG
logger.info(f"User {username} logged in with password {password}")

# ✅ CORRECT
logger.info(f"User {username} logged in successfully")
```

### 2. Never Return Passwords in API Responses

```python
# ❌ WRONG
return JsonResponse({
    'user': {
        'username': user.username,
        'password': user.password_hash  # Never expose this
    }
})

# ✅ CORRECT
return JsonResponse({
    'user': {
        'username': user.username,
        'email': user.email,
        'role': user.role
        # No password field
    }
})
```

### 3. Use Timing-Safe Comparisons

Django's `check_password()` already uses timing-safe comparison, so always use it:

```python
# ✅ CORRECT - Timing-safe
if check_password(password, user.password_hash):
    login_user()

# ❌ WRONG - Vulnerable to timing attacks
if user.password_hash == hash_function(password):
    login_user()
```

### 4. Implement Account Lockout

```python
from usersys.partner_auth_utils import AccountLockoutManager

# Check if account is locked
if AccountLockoutManager.is_locked(user):
    return JsonResponse({'error': 'Account is locked'}, status=403)

# Increment failed attempts on wrong password
if not check_password(password, user.password_hash):
    AccountLockoutManager.increment_failed_attempts(user)
    return JsonResponse({'error': 'Invalid credentials'}, status=401)

# Reset failed attempts on successful login
AccountLockoutManager.reset_failed_attempts(user)
```

## Testing Password Security

### Unit Test Example

```python
from django.test import TestCase
from django.contrib.auth.hashers import check_password, is_password_usable

class PasswordSecurityTest(TestCase):
    def test_password_is_hashed(self):
        plain_password = 'TestPass123!'
        
        user, _ = UserManager.create_user(
            partner_id=partner.id,
            username='testuser',
            email='test@example.com',
            password=plain_password,
            first_name='Test',
            last_name='User',
            send_email=False
        )
        
        # Password should not be stored in plain text
        self.assertNotEqual(user.password_hash, plain_password)
        
        # Password hash should be usable
        self.assertTrue(is_password_usable(user.password_hash))
        
        # Should verify correctly
        self.assertTrue(check_password(plain_password, user.password_hash))
```

## Troubleshooting

### Problem: Password verification always fails

**Cause**: Password might not be hashed correctly

**Solution**: Ensure you're using `make_password()` when storing:

```python
# Check if password is hashed
from django.contrib.auth.hashers import is_password_usable

if not is_password_usable(user.password_hash):
    print("Password is not properly hashed!")
    # Re-hash the password
    user.password_hash = make_password(correct_password)
    user.save()
```

### Problem: Getting "Invalid hash" error

**Cause**: Password hash format is incorrect

**Solution**: Password hash should start with algorithm identifier:

```python
# Valid hash format
pbkdf2_sha256$260000$salt$hash

# Check hash format
if not user.password_hash.startswith('pbkdf2_sha256$'):
    print("Invalid hash format!")
```

## Migration from Plain Text

If you have existing plain text passwords (you shouldn't!), migrate them:

```python
from django.contrib.auth.hashers import make_password

# Migrate all users (DO NOT RUN IN PRODUCTION WITHOUT BACKUP!)
for user in PartnerUser.objects.all():
    if not is_password_usable(user.password_hash):
        # This is a plain text password - hash it
        # NOTE: You'll need to know the plain text password
        user.password_hash = make_password(user.password_hash)
        user.save()
```

**WARNING**: You cannot migrate plain text passwords without knowing them. If you find plain text passwords, you must:
1. Force password reset for all affected users
2. Send password reset emails
3. Never store plain text passwords again

## Verification

Run the verification script to ensure all passwords are properly hashed:

```bash
cd env/default
python verify_password_hashing_simple.py
```

Expected output:
```
✅ ALL CHECKS PASSED!
Security Status: COMPLIANT ✅
```

## References

- [Django Password Management](https://docs.djangoproject.com/en/stable/topics/auth/passwords/)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [NIST Digital Identity Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)

## Summary

**Always remember:**
1. ✅ Use `make_password()` to hash passwords
2. ✅ Use `check_password()` to verify passwords
3. ❌ Never store plain text passwords
4. ❌ Never log passwords
5. ❌ Never return passwords in API responses
6. ✅ Validate password complexity
7. ✅ Implement account lockout
8. ✅ Use timing-safe comparisons

**When in doubt, use the provided utilities:**
- `PasswordValidator.hash_password()`
- `PasswordValidator.verify_password()`
- `UserManager.create_user()`
- `UserManager.reset_password()`

These utilities handle all the security details for you!

"""
Tests for Partner User Password Security
Verifies that all passwords are properly hashed using Django's password hasher
"""

import pytest
from django.contrib.auth.hashers import check_password, is_password_usable
from django.core.exceptions import ValidationError
from django.test import TestCase, RequestFactory
from django.utils import timezone
import json

# Import models and services
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'env', 'default'))

from usersys.partner_models import Partner, PartnerUser, PasswordResetToken
from usersys.user_manager import UserManager
from usersys.partner_auth_utils import PasswordValidator
from usersys.partner_auth_views import (
    partner_login, 
    partner_reset_password, 
    partner_change_password
)


class PasswordHashingTestCase(TestCase):
    """Test that all passwords are properly hashed"""
    
    def setUp(self):
        """Set up test data"""
        # Create a test partner
        self.partner = Partner.objects.create(
            partner_id='TEST001',
            name='Test Partner',
            communication_method='both',
            status='active'
        )
        
        self.factory = RequestFactory()
    
    def test_user_creation_hashes_password(self):
        """Test that creating a user hashes the password"""
        plain_password = 'TestPass123!'
        
        user, _ = UserManager.create_user(
            partner_id=self.partner.id,
            username='testuser',
            email='test@example.com',
            password=plain_password,
            first_name='Test',
            last_name='User',
            send_email=False
        )
        
        # Password should be hashed, not stored in plain text
        self.assertNotEqual(user.password_hash, plain_password)
        
        # Password hash should be usable (Django format)
        self.assertTrue(is_password_usable(user.password_hash))
        
        # Should be able to verify the password
        self.assertTrue(check_password(plain_password, user.password_hash))
        
        # Wrong password should not verify
        self.assertFalse(check_password('WrongPassword', user.password_hash))
    
    def test_password_reset_hashes_password(self):
        """Test that password reset hashes the new password"""
        # Create user
        user, _ = UserManager.create_user(
            partner_id=self.partner.id,
            username='resetuser',
            email='reset@example.com',
            password='OldPass123!',
            first_name='Reset',
            last_name='User',
            send_email=False
        )
        
        old_hash = user.password_hash
        new_password = 'NewPass456!'
        
        # Reset password
        UserManager.reset_password(user.id, new_password)
        
        # Reload user
        user.refresh_from_db()
        
        # Password hash should have changed
        self.assertNotEqual(user.password_hash, old_hash)
        
        # New password should not be in plain text
        self.assertNotEqual(user.password_hash, new_password)
        
        # Should be able to verify new password
        self.assertTrue(check_password(new_password, user.password_hash))
        
        # Old password should not work
        self.assertFalse(check_password('OldPass123!', user.password_hash))
    
    def test_password_validator_utility(self):
        """Test that PasswordValidator properly hashes passwords"""
        plain_password = 'SecurePass789!'
        
        # Hash password
        hashed = PasswordValidator.hash_password(plain_password)
        
        # Should not be plain text
        self.assertNotEqual(hashed, plain_password)
        
        # Should be usable Django hash
        self.assertTrue(is_password_usable(hashed))
        
        # Should verify correctly
        self.assertTrue(PasswordValidator.verify_password(plain_password, hashed))
        self.assertFalse(PasswordValidator.verify_password('WrongPass', hashed))
    
    def test_login_verifies_hashed_password(self):
        """Test that login properly verifies hashed passwords"""
        plain_password = 'LoginPass123!'
        
        # Create user
        user, _ = UserManager.create_user(
            partner_id=self.partner.id,
            username='loginuser',
            email='login@example.com',
            password=plain_password,
            first_name='Login',
            last_name='User',
            send_email=False
        )
        
        # Attempt login with correct password
        request = self.factory.post(
            '/api/v1/partner-portal/auth/login',
            data=json.dumps({
                'username': 'loginuser',
                'password': plain_password
            }),
            content_type='application/json'
        )
        request.session = {}
        
        response = partner_login(request)
        self.assertEqual(response.status_code, 200)
        
        # Attempt login with wrong password
        request = self.factory.post(
            '/api/v1/partner-portal/auth/login',
            data=json.dumps({
                'username': 'loginuser',
                'password': 'WrongPassword'
            }),
            content_type='application/json'
        )
        request.session = {}
        
        response = partner_login(request)
        self.assertEqual(response.status_code, 401)
    
    def test_password_change_hashes_new_password(self):
        """Test that password change properly hashes the new password"""
        old_password = 'OldPass123!'
        new_password = 'NewPass456!'
        
        # Create user
        user, _ = UserManager.create_user(
            partner_id=self.partner.id,
            username='changeuser',
            email='change@example.com',
            password=old_password,
            first_name='Change',
            last_name='User',
            send_email=False
        )
        
        old_hash = user.password_hash
        
        # Change password via API
        request = self.factory.post(
            '/api/v1/partner-portal/auth/change-password',
            data=json.dumps({
                'current_password': old_password,
                'new_password': new_password
            }),
            content_type='application/json'
        )
        request.session = {'partner_user_id': user.id}
        
        response = partner_change_password(request)
        self.assertEqual(response.status_code, 200)
        
        # Reload user
        user.refresh_from_db()
        
        # Password hash should have changed
        self.assertNotEqual(user.password_hash, old_hash)
        
        # New password should be hashed
        self.assertNotEqual(user.password_hash, new_password)
        self.assertTrue(is_password_usable(user.password_hash))
        
        # Should verify with new password
        self.assertTrue(check_password(new_password, user.password_hash))
        self.assertFalse(check_password(old_password, user.password_hash))
    
    def test_password_reset_token_flow_hashes_password(self):
        """Test that password reset via token properly hashes password"""
        old_password = 'OldPass123!'
        new_password = 'NewPass789!'
        
        # Create user
        user, _ = UserManager.create_user(
            partner_id=self.partner.id,
            username='tokenuser',
            email='token@example.com',
            password=old_password,
            first_name='Token',
            last_name='User',
            send_email=False
        )
        
        # Create reset token
        reset_token = PasswordResetToken.objects.create(
            user=user,
            token='test-token-123',
            expires_at=timezone.now() + timezone.timedelta(hours=24)
        )
        
        old_hash = user.password_hash
        
        # Reset password via token
        request = self.factory.post(
            '/api/v1/partner-portal/auth/reset-password',
            data=json.dumps({
                'token': 'test-token-123',
                'new_password': new_password
            }),
            content_type='application/json'
        )
        
        response = partner_reset_password(request)
        self.assertEqual(response.status_code, 200)
        
        # Reload user
        user.refresh_from_db()
        
        # Password hash should have changed
        self.assertNotEqual(user.password_hash, old_hash)
        
        # New password should be hashed
        self.assertNotEqual(user.password_hash, new_password)
        self.assertTrue(is_password_usable(user.password_hash))
        
        # Should verify with new password
        self.assertTrue(check_password(new_password, user.password_hash))
    
    def test_no_plain_text_passwords_in_database(self):
        """Test that no plain text passwords exist in database"""
        test_passwords = [
            'TestPass1!',
            'SecurePass2@',
            'StrongPass3#',
        ]
        
        # Create multiple users
        for i, password in enumerate(test_passwords):
            UserManager.create_user(
                partner_id=self.partner.id,
                username=f'user{i}',
                email=f'user{i}@example.com',
                password=password,
                first_name='Test',
                last_name=f'User{i}',
                send_email=False
            )
        
        # Check all users
        users = PartnerUser.objects.all()
        for user in users:
            # Password hash should not match any plain text password
            for plain_password in test_passwords:
                self.assertNotEqual(user.password_hash, plain_password)
            
            # Password hash should be usable Django format
            self.assertTrue(is_password_usable(user.password_hash))
            
            # Password hash should start with algorithm identifier
            # Django uses pbkdf2_sha256 by default
            self.assertTrue(
                user.password_hash.startswith('pbkdf2_sha256$') or
                user.password_hash.startswith('argon2') or
                user.password_hash.startswith('bcrypt')
            )
    
    def test_password_hash_format(self):
        """Test that password hashes use proper Django format"""
        plain_password = 'FormatTest123!'
        
        user, _ = UserManager.create_user(
            partner_id=self.partner.id,
            username='formatuser',
            email='format@example.com',
            password=plain_password,
            first_name='Format',
            last_name='User',
            send_email=False
        )
        
        # Django password hash format: algorithm$iterations$salt$hash
        # Example: pbkdf2_sha256$260000$salt$hash
        parts = user.password_hash.split('$')
        
        # Should have at least 3 parts (algorithm, iterations/salt, hash)
        self.assertGreaterEqual(len(parts), 3)
        
        # First part should be algorithm
        self.assertIn(parts[0], ['pbkdf2_sha256', 'pbkdf2_sha1', 'argon2', 'bcrypt', 'bcrypt_sha256'])
        
        # Should be verifiable
        self.assertTrue(check_password(plain_password, user.password_hash))


class PasswordSecurityComplianceTestCase(TestCase):
    """Test password security compliance"""
    
    def setUp(self):
        """Set up test data"""
        self.partner = Partner.objects.create(
            partner_id='SEC001',
            name='Security Test Partner',
            communication_method='both',
            status='active'
        )
    
    def test_password_complexity_enforced(self):
        """Test that password complexity requirements are enforced"""
        # Test weak passwords are rejected
        weak_passwords = [
            'short',  # Too short
            'nouppercase123!',  # No uppercase
            'NOLOWERCASE123!',  # No lowercase
            'NoNumbers!',  # No numbers
            'NoSpecial123',  # No special characters
        ]
        
        for weak_password in weak_passwords:
            with self.assertRaises(ValidationError):
                UserManager.create_user(
                    partner_id=self.partner.id,
                    username=f'user_{weak_password[:5]}',
                    email=f'{weak_password[:5]}@example.com',
                    password=weak_password,
                    first_name='Test',
                    last_name='User',
                    send_email=False
                )
    
    def test_password_not_stored_in_logs(self):
        """Test that passwords are not stored in activity logs"""
        from usersys.partner_models import ActivityLog
        
        plain_password = 'LogTest123!'
        
        # Create user
        user, _ = UserManager.create_user(
            partner_id=self.partner.id,
            username='loguser',
            email='log@example.com',
            password=plain_password,
            first_name='Log',
            last_name='User',
            send_email=False
        )
        
        # Check activity logs
        logs = ActivityLog.objects.all()
        for log in logs:
            # Password should not appear in details
            details_str = json.dumps(log.details)
            self.assertNotIn(plain_password, details_str)
            self.assertNotIn('password', details_str.lower())


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

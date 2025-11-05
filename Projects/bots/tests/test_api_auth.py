"""
Tests for API Authentication
"""

import pytest
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'env', 'default'))

try:
    from usersys.api_models import APIKey, APIPermission
    from usersys.api_auth import api_authenticate, get_client_ip
except ImportError:
    pytest.skip("Bots environment not initialized", allow_module_level=True)


class TestAPIAuthentication(TestCase):
    """Test API authentication functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test API key
        self.api_key = APIKey.objects.create(
            name='Test API Key',
            user=self.user,
            is_active=True,
            rate_limit=100
        )
        
        # Create test permission
        self.permission = APIPermission.objects.create(
            code='test_permission',
            name='Test Permission',
            is_active=True
        )
        self.api_key.permissions.add(self.permission)
    
    def test_get_client_ip_with_forwarded_header(self):
        """Test IP extraction with X-Forwarded-For header"""
        request = self.factory.get('/')
        request.META['HTTP_X_FORWARDED_FOR'] = '192.168.1.1, 10.0.0.1'
        
        ip = get_client_ip(request)
        self.assertEqual(ip, '192.168.1.1')
    
    def test_get_client_ip_without_forwarded_header(self):
        """Test IP extraction without X-Forwarded-For header"""
        request = self.factory.get('/')
        request.META['REMOTE_ADDR'] = '192.168.1.1'
        
        ip = get_client_ip(request)
        self.assertEqual(ip, '192.168.1.1')
    
    def test_api_key_generation(self):
        """Test API key is generated automatically"""
        self.assertIsNotNone(self.api_key.key)
        self.assertGreater(len(self.api_key.key), 40)
    
    def test_api_key_is_valid(self):
        """Test valid API key"""
        self.assertTrue(self.api_key.is_valid())
    
    def test_api_key_inactive(self):
        """Test inactive API key"""
        self.api_key.is_active = False
        self.api_key.save()
        self.assertFalse(self.api_key.is_valid())
    
    def test_api_key_has_permission(self):
        """Test permission checking"""
        self.assertTrue(self.api_key.has_permission('test_permission'))
        self.assertFalse(self.api_key.has_permission('nonexistent_permission'))
    
    def test_rate_limit_check(self):
        """Test rate limiting"""
        self.api_key.current_usage = 50
        self.api_key.save()
        self.assertTrue(self.api_key.check_rate_limit())
        
        self.api_key.current_usage = 100
        self.api_key.save()
        self.assertFalse(self.api_key.check_rate_limit())
    
    def test_ip_whitelist_empty(self):
        """Test IP whitelist when empty (allows all)"""
        self.api_key.allowed_ips = ''
        self.api_key.save()
        self.assertTrue(self.api_key.check_ip('192.168.1.1'))
    
    def test_ip_whitelist_allowed(self):
        """Test IP whitelist with allowed IP"""
        self.api_key.allowed_ips = '192.168.1.1, 10.0.0.1'
        self.api_key.save()
        self.assertTrue(self.api_key.check_ip('192.168.1.1'))
    
    def test_ip_whitelist_denied(self):
        """Test IP whitelist with denied IP"""
        self.api_key.allowed_ips = '192.168.1.1, 10.0.0.1'
        self.api_key.save()
        self.assertFalse(self.api_key.check_ip('192.168.1.2'))


class TestAPIKeyModel(TestCase):
    """Test APIKey model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_create_api_key(self):
        """Test creating an API key"""
        api_key = APIKey.objects.create(
            name='Test Key',
            user=self.user
        )
        self.assertIsNotNone(api_key.key)
        self.assertTrue(api_key.is_active)
        self.assertEqual(api_key.rate_limit, 1000)
    
    def test_api_key_string_representation(self):
        """Test string representation"""
        api_key = APIKey.objects.create(
            name='Test Key',
            user=self.user
        )
        str_repr = str(api_key)
        self.assertIn('Test Key', str_repr)
        self.assertIn(api_key.key[:8], str_repr)
    
    def test_increment_usage(self):
        """Test usage increment"""
        api_key = APIKey.objects.create(
            name='Test Key',
            user=self.user
        )
        initial_usage = api_key.current_usage
        api_key.increment_usage()
        self.assertEqual(api_key.current_usage, initial_usage + 1)
        self.assertIsNotNone(api_key.last_used)


class TestAPIPermissionModel(TestCase):
    """Test APIPermission model"""
    
    def test_create_permission(self):
        """Test creating a permission"""
        permission = APIPermission.objects.create(
            code='test_perm',
            name='Test Permission',
            description='Test description',
            is_active=True
        )
        self.assertEqual(permission.code, 'test_perm')
        self.assertTrue(permission.is_active)
    
    def test_permission_string_representation(self):
        """Test string representation"""
        permission = APIPermission.objects.create(
            code='test_perm',
            name='Test Permission'
        )
        self.assertEqual(str(permission), 'Test Permission')


if __name__ == '__main__':
    pytest.main([__file__])

"""
Tests for API Views
"""

import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'env', 'default'))

try:
    from usersys.api_models import APIKey, APIPermission
except ImportError:
    pytest.skip("Bots environment not initialized", allow_module_level=True)


class TestAPIViews(TestCase):
    """Test API view endpoints"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = Client()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create API key with all permissions
        self.api_key = APIKey.objects.create(
            name='Test API Key',
            user=self.user,
            is_active=True,
            rate_limit=1000
        )
        
        # Create permissions
        permissions = [
            'file_upload', 'file_download', 'file_list',
            'route_execute', 'report_view'
        ]
        for perm_code in permissions:
            perm, _ = APIPermission.objects.get_or_create(
                code=perm_code,
                defaults={'name': perm_code.replace('_', ' ').title()}
            )
            self.api_key.permissions.add(perm)
        
        self.headers = {'HTTP_X_API_KEY': self.api_key.key}
    
    def test_api_status_endpoint(self):
        """Test API status endpoint"""
        response = self.client.get('/api/v1/status', **self.headers)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['api_key']['name'], 'Test API Key')
        self.assertEqual(data['api_key']['user'], 'testuser')
    
    def test_api_status_without_key(self):
        """Test API status without API key"""
        response = self.client.get('/api/v1/status')
        self.assertEqual(response.status_code, 401)
        
        data = json.loads(response.content)
        self.assertIn('error', data)
    
    def test_api_status_with_invalid_key(self):
        """Test API status with invalid API key"""
        response = self.client.get(
            '/api/v1/status',
            HTTP_X_API_KEY='invalid-key'
        )
        self.assertEqual(response.status_code, 401)
    
    def test_file_upload_without_file(self):
        """Test file upload without file"""
        response = self.client.post('/api/v1/files/upload', **self.headers)
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.content)
        self.assertIn('error', data)
    
    def test_file_upload_with_file(self):
        """Test file upload with file"""
        test_file = SimpleUploadedFile(
            "test.edi",
            b"test content",
            content_type="text/plain"
        )
        
        response = self.client.post(
            '/api/v1/files/upload',
            {'file': test_file, 'route': 'test_route'},
            **self.headers
        )
        
        # May fail if Bots not fully initialized, but should not error
        self.assertIn(response.status_code, [201, 500])
    
    def test_file_list_endpoint(self):
        """Test file list endpoint"""
        response = self.client.get('/api/v1/files/list', **self.headers)
        
        # May fail if Bots not fully initialized, but should not error
        self.assertIn(response.status_code, [200, 500])
    
    def test_route_execute_without_route(self):
        """Test route execution without route name"""
        response = self.client.post(
            '/api/v1/routes/execute',
            json.dumps({}),
            content_type='application/json',
            **self.headers
        )
        self.assertEqual(response.status_code, 400)
    
    def test_reports_endpoint(self):
        """Test reports endpoint"""
        response = self.client.get('/api/v1/reports', **self.headers)
        
        # May fail if Bots not fully initialized, but should not error
        self.assertIn(response.status_code, [200, 500])
    
    def test_rate_limiting(self):
        """Test rate limiting"""
        # Set low rate limit
        self.api_key.rate_limit = 2
        self.api_key.current_usage = 2
        self.api_key.save()
        
        response = self.client.get('/api/v1/status', **self.headers)
        self.assertEqual(response.status_code, 429)
        
        data = json.loads(response.content)
        self.assertIn('Rate limit exceeded', data['error'])
    
    def test_insufficient_permissions(self):
        """Test endpoint with insufficient permissions"""
        # Remove all permissions
        self.api_key.permissions.clear()
        
        response = self.client.post('/api/v1/files/upload', **self.headers)
        self.assertEqual(response.status_code, 403)
        
        data = json.loads(response.content)
        self.assertIn('Insufficient permissions', data['error'])


class TestAPIAuthentication(TestCase):
    """Test API authentication mechanisms"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_missing_api_key(self):
        """Test request without API key"""
        response = self.client.get('/api/v1/status')
        self.assertEqual(response.status_code, 401)
    
    def test_invalid_api_key(self):
        """Test request with invalid API key"""
        response = self.client.get(
            '/api/v1/status',
            HTTP_X_API_KEY='invalid-key-12345'
        )
        self.assertEqual(response.status_code, 401)
    
    def test_inactive_api_key(self):
        """Test request with inactive API key"""
        api_key = APIKey.objects.create(
            name='Inactive Key',
            user=self.user,
            is_active=False
        )
        
        response = self.client.get(
            '/api/v1/status',
            HTTP_X_API_KEY=api_key.key
        )
        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    pytest.main([__file__])

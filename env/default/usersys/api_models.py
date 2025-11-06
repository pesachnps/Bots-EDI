"""
Bots EDI API Models
Manages API authentication, permissions, and access control
"""

import secrets
import hashlib
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class APIKey(models.Model):
    """API Key model for authentication"""
    
    # Basic Information
    name = models.CharField(max_length=255, help_text="Descriptive name for this API key")
    key = models.CharField(max_length=64, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    
    # Status and Permissions
    is_active = models.BooleanField(default=True, help_text="Enable/disable this API key")
    permissions = models.ManyToManyField('APIPermission', blank=True, related_name='api_keys')
    
    # Rate Limiting
    rate_limit = models.IntegerField(default=1000, help_text="Requests per hour")
    current_usage = models.IntegerField(default=0, editable=False)
    usage_reset_time = models.DateTimeField(default=timezone.now, editable=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True, help_text="Optional expiration date")
    
    # IP Whitelist
    allowed_ips = models.TextField(
        blank=True, 
        help_text="Comma-separated list of allowed IP addresses (leave blank for all)"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"
        app_label = 'usersys'
    
    def __str__(self):
        return f"{self.name} ({self.key[:8]}...)"
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_key():
        """Generate a secure random API key"""
        return secrets.token_urlsafe(48)
    
    def is_valid(self):
        """Check if API key is valid and not expired"""
        if not self.is_active:
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True
    
    def check_rate_limit(self):
        """Check if rate limit has been exceeded"""
        now = timezone.now()
        
        # Reset counter if hour has passed
        if now > self.usage_reset_time:
            self.current_usage = 0
            self.usage_reset_time = now + timedelta(hours=1)
            self.save()
        
        return self.current_usage < self.rate_limit
    
    def increment_usage(self):
        """Increment usage counter"""
        self.current_usage += 1
        self.last_used = timezone.now()
        self.save()
    
    def check_ip(self, ip_address):
        """Check if IP address is allowed"""
        if not self.allowed_ips:
            return True
        allowed = [ip.strip() for ip in self.allowed_ips.split(',')]
        return ip_address in allowed
    
    def has_permission(self, permission_code):
        """Check if API key has specific permission"""
        return self.permissions.filter(code=permission_code, is_active=True).exists()


class APIPermission(models.Model):
    """API Permission model for granular access control"""
    
    PERMISSION_TYPES = [
        ('file_upload', 'Upload EDI Files'),
        ('file_download', 'Download EDI Files'),
        ('file_list', 'List Files'),
        ('file_delete', 'Delete Files'),
        ('route_execute', 'Execute Routes'),
        ('route_list', 'List Routes'),
        ('report_view', 'View Reports'),
        ('report_download', 'Download Reports'),
        ('partner_view', 'View Partners'),
        ('partner_manage', 'Manage Partners'),
        ('translate_view', 'View Translations'),
        ('channel_view', 'View Channels'),
        ('admin_access', 'Full Admin Access'),
    ]
    
    code = models.CharField(max_length=50, unique=True, choices=PERMISSION_TYPES)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "API Permission"
        verbose_name_plural = "API Permissions"
        app_label = 'usersys'
    
    def __str__(self):
        return self.name


class APIAuditLog(models.Model):
    """API Audit Log for tracking all API requests"""
    
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('denied', 'Access Denied'),
        ('rate_limited', 'Rate Limited'),
    ]
    
    api_key = models.ForeignKey(APIKey, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    
    request_data = models.TextField(blank=True, help_text="Request parameters (sanitized)")
    response_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    response_code = models.IntegerField()
    response_message = models.TextField(blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    duration_ms = models.IntegerField(help_text="Request duration in milliseconds")
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "API Audit Log"
        verbose_name_plural = "API Audit Logs"
        app_label = 'usersys'
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['api_key', '-timestamp']),
            models.Index(fields=['response_status']),
        ]
    
    def __str__(self):
        return f"{self.method} {self.endpoint} - {self.response_status} ({self.timestamp})"

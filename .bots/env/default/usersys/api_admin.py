"""
Bots EDI API Admin Interface
Django admin configuration for API management
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .api_models import APIKey, APIPermission, APIAuditLog


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'key_display', 'is_active', 'rate_limit', 'usage_display', 'last_used', 'created_at']
    list_filter = ['is_active', 'created_at', 'last_used']
    search_fields = ['name', 'key', 'user__username']
    filter_horizontal = ['permissions']
    readonly_fields = ['key', 'created_at', 'last_used', 'current_usage', 'usage_reset_time']
    
    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'user', 'key', 'is_active']
        }),
        ('Permissions', {
            'fields': ['permissions']
        }),
        ('Rate Limiting', {
            'fields': ['rate_limit', 'current_usage', 'usage_reset_time']
        }),
        ('Security', {
            'fields': ['allowed_ips', 'expires_at']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'last_used']
        }),
    ]
    
    def key_display(self, obj):
        return format_html(
            '<code style="background:#f5f5f5;padding:2px 5px;border-radius:3px;">{}</code>',
            obj.key[:16] + '...'
        )
    key_display.short_description = 'API Key'
    
    def usage_display(self, obj):
        percentage = (obj.current_usage / obj.rate_limit * 100) if obj.rate_limit > 0 else 0
        color = 'green' if percentage < 70 else 'orange' if percentage < 90 else 'red'
        return format_html(
            '<span style="color:{};">{}/{}</span>',
            color, obj.current_usage, obj.rate_limit
        )
    usage_display.short_description = 'Usage'
    
    def save_model(self, request, obj, form, change):
        if not change:  # New object
            if not obj.user:
                obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(APIPermission)
class APIPermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['created_at']


@admin.register(APIAuditLog)
class APIAuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'api_key_display', 'method', 'endpoint', 'status_display', 'response_code', 'duration_ms', 'ip_address']
    list_filter = ['response_status', 'method', 'timestamp']
    search_fields = ['endpoint', 'ip_address', 'api_key__name']
    readonly_fields = ['timestamp', 'duration_ms']
    date_hierarchy = 'timestamp'
    
    def api_key_display(self, obj):
        if obj.api_key:
            return obj.api_key.name
        return 'Unknown'
    api_key_display.short_description = 'API Key'
    
    def status_display(self, obj):
        colors = {
            'success': 'green',
            'failed': 'red',
            'denied': 'orange',
            'rate_limited': 'purple'
        }
        color = colors.get(obj.response_status, 'gray')
        return format_html(
            '<span style="color:{};">{}</span>',
            color, obj.response_status.upper()
        )
    status_display.short_description = 'Status'
    
    def has_add_permission(self, request):
        return False  # Logs are created automatically
    
    def has_change_permission(self, request, obj=None):
        return False  # Logs are read-only

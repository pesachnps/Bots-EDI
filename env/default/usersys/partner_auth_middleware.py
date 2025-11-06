"""
Partner Portal Authentication Middleware
Handles session validation, permission checks, and session timeout
"""

from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta, datetime

from .partner_models import PartnerUser


class PartnerAuthMiddleware:
    """Middleware for partner portal authentication"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Session timeout in seconds (30 minutes)
        self.session_timeout = 1800
    
    def __call__(self, request):
        # Check if request is for partner portal API
        if request.path.startswith('/modern-edi/api/v1/partner-portal/'):
            # Skip auth check for login and password reset endpoints
            public_endpoints = [
                '/modern-edi/api/v1/partner-portal/auth/login',
                '/modern-edi/api/v1/partner-portal/auth/forgot-password',
                '/modern-edi/api/v1/partner-portal/auth/reset-password',
            ]
            
            if request.path not in public_endpoints:
                # Verify partner session exists
                partner_user_id = request.session.get('partner_user_id')
                
                if not partner_user_id:
                    return JsonResponse({
                        'error': 'Not authenticated',
                        'code': 'NOT_AUTHENTICATED'
                    }, status=401)
                
                # Check session timeout
                last_activity_str = request.session.get('last_activity')
                if last_activity_str:
                    try:
                        last_activity = datetime.fromisoformat(last_activity_str)
                        if timezone.is_naive(last_activity):
                            last_activity = timezone.make_aware(last_activity)
                        
                        time_since_activity = (timezone.now() - last_activity).total_seconds()
                        
                        if time_since_activity > self.session_timeout:
                            request.session.flush()
                            return JsonResponse({
                                'error': 'Session expired',
                                'code': 'SESSION_EXPIRED'
                            }, status=401)
                    except (ValueError, TypeError):
                        pass
                
                # Load partner user
                try:
                    partner_user = PartnerUser.objects.select_related('partner', 'permissions').get(
                        id=partner_user_id,
                        is_active=True
                    )
                    
                    # Check account lockout
                    if partner_user.is_locked():
                        return JsonResponse({
                            'error': 'Account is locked',
                            'code': 'ACCOUNT_LOCKED',
                            'locked_until': partner_user.locked_until.isoformat() if partner_user.locked_until else None
                        }, status=403)
                    
                    # Attach user to request
                    request.partner_user = partner_user
                    request.partner = partner_user.partner
                    
                    # Update last activity
                    request.session['last_activity'] = timezone.now().isoformat()
                    
                except PartnerUser.DoesNotExist:
                    request.session.flush()
                    return JsonResponse({
                        'error': 'Invalid session',
                        'code': 'INVALID_SESSION'
                    }, status=401)
        
        response = self.get_response(request)
        return response


class PartnerPermissionMiddleware:
    """Middleware for checking partner permissions"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check permissions for partner portal endpoints
        if request.path.startswith('/modern-edi/api/v1/partner-portal/'):
            # Skip permission check for auth endpoints
            auth_endpoints = [
                '/modern-edi/api/v1/partner-portal/auth/',
            ]
            
            skip_check = any(request.path.startswith(ep) for ep in auth_endpoints)
            
            if not skip_check and hasattr(request, 'partner_user'):
                user = request.partner_user
                permissions = user.permissions if hasattr(user, 'permissions') else None
                
                # If no permissions object, create default based on role
                if not permissions:
                    from .partner_models import PartnerPermission
                    defaults = user.get_default_permissions()
                    permissions = PartnerPermission.objects.create(
                        user=user,
                        **defaults
                    )
                    user.permissions = permissions
                
                # Check permissions based on endpoint
                if '/files/upload' in request.path and request.method == 'POST':
                    if not permissions.can_upload_files:
                        return JsonResponse({
                            'error': 'Permission denied',
                            'code': 'PERMISSION_DENIED',
                            'required_permission': 'can_upload_files'
                        }, status=403)
                
                elif '/files/download' in request.path and request.method in ['GET', 'POST']:
                    if not permissions.can_download_files:
                        return JsonResponse({
                            'error': 'Permission denied',
                            'code': 'PERMISSION_DENIED',
                            'required_permission': 'can_download_files'
                        }, status=403)
                
                elif '/transactions' in request.path and request.method == 'GET':
                    if not permissions.can_view_transactions:
                        return JsonResponse({
                            'error': 'Permission denied',
                            'code': 'PERMISSION_DENIED',
                            'required_permission': 'can_view_transactions'
                        }, status=403)
                
                elif '/settings' in request.path and request.method in ['PUT', 'PATCH', 'POST']:
                    if not permissions.can_manage_settings:
                        return JsonResponse({
                            'error': 'Permission denied',
                            'code': 'PERMISSION_DENIED',
                            'required_permission': 'can_manage_settings'
                        }, status=403)
                
                # Attach permissions to request for easy access
                request.partner_permissions = permissions
        
        response = self.get_response(request)
        return response


class AdminAuthMiddleware:
    """Middleware for admin dashboard authentication"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if request is for admin dashboard API
        if request.path.startswith('/modern-edi/api/v1/admin/'):
            # Verify user is authenticated and is staff
            if not request.user.is_authenticated:
                return JsonResponse({
                    'error': 'Authentication required',
                    'code': 'NOT_AUTHENTICATED'
                }, status=401)
            
            if not request.user.is_staff:
                return JsonResponse({
                    'error': 'Admin access required',
                    'code': 'ADMIN_REQUIRED'
                }, status=403)
        
        response = self.get_response(request)
        return response

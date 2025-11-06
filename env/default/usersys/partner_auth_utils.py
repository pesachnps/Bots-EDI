"""
Partner Authentication Utilities
Helper functions for password management, token generation, and session handling
"""

import secrets
import re
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from datetime import timedelta


class PasswordValidator:
    """Validate password strength"""
    
    @staticmethod
    def validate(password):
        """
        Validate password meets complexity requirements
        
        Requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number
        - At least one special character
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character"
        
        return True, ""
    
    @staticmethod
    def hash_password(password):
        """Hash a password using Django's password hasher"""
        return make_password(password)
    
    @staticmethod
    def verify_password(password, password_hash):
        """Verify a password against its hash"""
        return check_password(password, password_hash)


class TokenGenerator:
    """Generate secure tokens for password reset and other purposes"""
    
    @staticmethod
    def generate_reset_token():
        """Generate a secure password reset token"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def generate_api_token():
        """Generate a secure API token"""
        return secrets.token_urlsafe(48)
    
    @staticmethod
    def generate_session_token():
        """Generate a secure session token"""
        return secrets.token_urlsafe(24)


class SessionManager:
    """Manage partner user sessions"""
    
    @staticmethod
    def create_session(request, user):
        """
        Create a new session for a partner user
        
        Args:
            request: Django request object
            user: PartnerUser instance
        """
        request.session['partner_user_id'] = user.id
        request.session['partner_id'] = str(user.partner.id)
        request.session['last_activity'] = timezone.now().isoformat()
        request.session['created_at'] = timezone.now().isoformat()
        
        # Update user's last login
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
    
    @staticmethod
    def destroy_session(request):
        """Destroy the current session"""
        request.session.flush()
    
    @staticmethod
    def is_session_valid(request, timeout_seconds=1800):
        """
        Check if session is valid and not expired
        
        Args:
            request: Django request object
            timeout_seconds: Session timeout in seconds (default: 30 minutes)
        
        Returns:
            tuple: (is_valid, reason)
        """
        partner_user_id = request.session.get('partner_user_id')
        
        if not partner_user_id:
            return False, 'no_session'
        
        last_activity_str = request.session.get('last_activity')
        if not last_activity_str:
            return False, 'no_activity'
        
        try:
            from datetime import datetime
            last_activity = datetime.fromisoformat(last_activity_str)
            if timezone.is_naive(last_activity):
                last_activity = timezone.make_aware(last_activity)
            
            time_since_activity = (timezone.now() - last_activity).total_seconds()
            
            if time_since_activity > timeout_seconds:
                return False, 'expired'
            
            return True, 'valid'
            
        except (ValueError, TypeError):
            return False, 'invalid_format'
    
    @staticmethod
    def update_activity(request):
        """Update last activity timestamp"""
        request.session['last_activity'] = timezone.now().isoformat()
    
    @staticmethod
    def get_session_info(request):
        """Get information about the current session"""
        return {
            'partner_user_id': request.session.get('partner_user_id'),
            'partner_id': request.session.get('partner_id'),
            'last_activity': request.session.get('last_activity'),
            'created_at': request.session.get('created_at'),
        }


class IPAddressHelper:
    """Helper for extracting and validating IP addresses"""
    
    @staticmethod
    def get_client_ip(request):
        """
        Get the client's IP address from the request
        
        Args:
            request: Django request object
        
        Returns:
            str: IP address
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # Take the first IP in the chain
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        return ip
    
    @staticmethod
    def get_user_agent(request):
        """
        Get the user agent string from the request
        
        Args:
            request: Django request object
        
        Returns:
            str: User agent string (truncated to 500 chars)
        """
        return request.META.get('HTTP_USER_AGENT', '')[:500]


class AccountLockoutManager:
    """Manage account lockout for failed login attempts"""
    
    @staticmethod
    def increment_failed_attempts(user):
        """
        Increment failed login attempts and lock account if threshold reached
        
        Args:
            user: PartnerUser instance
        """
        user.failed_login_attempts += 1
        
        # Lock account after 5 failed attempts for 15 minutes
        if user.failed_login_attempts >= 5:
            user.locked_until = timezone.now() + timedelta(minutes=15)
        
        user.save(update_fields=['failed_login_attempts', 'locked_until'])
    
    @staticmethod
    def reset_failed_attempts(user):
        """
        Reset failed login attempts counter
        
        Args:
            user: PartnerUser instance
        """
        user.failed_login_attempts = 0
        user.locked_until = None
        user.save(update_fields=['failed_login_attempts', 'locked_until'])
    
    @staticmethod
    def is_locked(user):
        """
        Check if account is currently locked
        
        Args:
            user: PartnerUser instance
        
        Returns:
            bool: True if locked, False otherwise
        """
        if user.locked_until and user.locked_until > timezone.now():
            return True
        return False
    
    @staticmethod
    def get_lockout_info(user):
        """
        Get lockout information for a user
        
        Args:
            user: PartnerUser instance
        
        Returns:
            dict: Lockout information
        """
        is_locked = AccountLockoutManager.is_locked(user)
        
        return {
            'is_locked': is_locked,
            'failed_attempts': user.failed_login_attempts,
            'locked_until': user.locked_until.isoformat() if user.locked_until else None,
            'remaining_attempts': max(0, 5 - user.failed_login_attempts) if not is_locked else 0,
        }


def require_partner_auth(view_func):
    """
    Decorator to require partner authentication for a view
    
    Usage:
        @require_partner_auth
        def my_view(request):
            # request.partner_user will be available
            pass
    """
    def wrapper(request, *args, **kwargs):
        from django.http import JsonResponse
        
        if not hasattr(request, 'partner_user'):
            return JsonResponse({
                'error': 'Authentication required',
                'code': 'NOT_AUTHENTICATED'
            }, status=401)
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def require_partner_permission(permission_name):
    """
    Decorator to require a specific permission for a view
    
    Usage:
        @require_partner_permission('can_upload_files')
        def upload_view(request):
            pass
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            from django.http import JsonResponse
            
            if not hasattr(request, 'partner_user'):
                return JsonResponse({
                    'error': 'Authentication required',
                    'code': 'NOT_AUTHENTICATED'
                }, status=401)
            
            permissions = request.partner_permissions if hasattr(request, 'partner_permissions') else None
            
            if not permissions:
                return JsonResponse({
                    'error': 'Permission denied',
                    'code': 'PERMISSION_DENIED'
                }, status=403)
            
            if not getattr(permissions, permission_name, False):
                return JsonResponse({
                    'error': 'Permission denied',
                    'code': 'PERMISSION_DENIED',
                    'required_permission': permission_name
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    
    return decorator

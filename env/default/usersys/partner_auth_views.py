"""
Partner Portal Authentication Views
Handles login, logout, password reset for partner users
"""

import secrets
from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from .partner_models import PartnerUser, PasswordResetToken
from .activity_logger import ActivityLogger
from .email_service import EmailService


@csrf_exempt
@require_http_methods(["POST"])
def partner_login(request):
    """
    Partner user login endpoint
    POST /api/v1/partner-portal/auth/login
    Body: {"username": "user", "password": "pass"}
    """
    import json
    
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return JsonResponse({
                'error': 'Username and password are required'
            }, status=400)
        
        # Get user
        try:
            user = PartnerUser.objects.select_related('partner', 'permissions').get(
                username=username
            )
        except PartnerUser.DoesNotExist:
            return JsonResponse({
                'error': 'Invalid credentials'
            }, status=401)
        
        # Check if account is active
        if not user.is_active:
            ActivityLogger.log(
                user_type='partner',
                user_id=user.id,
                user_name=user.username,
                action='login_failed',
                details={'reason': 'account_inactive'},
                request=request
            )
            return JsonResponse({
                'error': 'Account is inactive'
            }, status=403)
        
        # Check if account is locked
        if user.is_locked():
            ActivityLogger.log(
                user_type='partner',
                user_id=user.id,
                user_name=user.username,
                action='login_failed',
                details={'reason': 'account_locked'},
                request=request
            )
            return JsonResponse({
                'error': 'Account is locked. Please try again later.',
                'locked_until': user.locked_until.isoformat() if user.locked_until else None
            }, status=403)
        
        # Verify password
        if not check_password(password, user.password_hash):
            user.increment_failed_attempts()
            ActivityLogger.log(
                user_type='partner',
                user_id=user.id,
                user_name=user.username,
                action='login_failed',
                details={'reason': 'invalid_password', 'attempts': user.failed_login_attempts},
                request=request
            )
            return JsonResponse({
                'error': 'Invalid credentials'
            }, status=401)
        
        # Successful login
        user.reset_failed_attempts()
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        # Create session
        request.session['partner_user_id'] = user.id
        request.session['partner_id'] = str(user.partner.id)
        request.session['last_activity'] = timezone.now().isoformat()
        
        # Log successful login
        ActivityLogger.log(
            user_type='partner',
            user_id=user.id,
            user_name=user.username,
            action='login',
            details={'partner': user.partner.name},
            request=request
        )
        
        # Return user info
        return JsonResponse({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'full_name': user.get_full_name(),
                'role': user.role,
                'partner': {
                    'id': str(user.partner.id),
                    'partner_id': user.partner.partner_id,
                    'name': user.partner.name,
                    'display_name': user.partner.get_display_name(),
                },
                'permissions': user.permissions.to_dict() if hasattr(user, 'permissions') else user.get_default_permissions(),
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def partner_logout(request):
    """
    Partner user logout endpoint
    POST /api/v1/partner-portal/auth/logout
    """
    partner_user_id = request.session.get('partner_user_id')
    
    if partner_user_id:
        try:
            user = PartnerUser.objects.get(id=partner_user_id)
            ActivityLogger.log(
                user_type='partner',
                user_id=user.id,
                user_name=user.username,
                action='logout',
                request=request
            )
        except PartnerUser.DoesNotExist:
            pass
    
    # Clear session
    request.session.flush()
    
    return JsonResponse({'success': True})


@require_http_methods(["GET"])
def partner_me(request):
    """
    Get current partner user info
    GET /api/v1/partner-portal/auth/me
    """
    partner_user_id = request.session.get('partner_user_id')
    
    if not partner_user_id:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    try:
        user = PartnerUser.objects.select_related('partner', 'permissions').get(
            id=partner_user_id,
            is_active=True
        )
        
        return JsonResponse({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'full_name': user.get_full_name(),
                'role': user.role,
                'partner': {
                    'id': str(user.partner.id),
                    'partner_id': user.partner.partner_id,
                    'name': user.partner.name,
                    'display_name': user.partner.get_display_name(),
                },
                'permissions': user.permissions.to_dict() if hasattr(user, 'permissions') else user.get_default_permissions(),
                'last_login': user.last_login.isoformat() if user.last_login else None,
            }
        })
        
    except PartnerUser.DoesNotExist:
        request.session.flush()
        return JsonResponse({'error': 'User not found'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def partner_forgot_password(request):
    """
    Request password reset
    POST /api/v1/partner-portal/auth/forgot-password
    Body: {"email": "user@example.com"}
    """
    import json
    
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
        
        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)
        
        # Find user by email
        try:
            user = PartnerUser.objects.get(email__iexact=email, is_active=True)
        except PartnerUser.DoesNotExist:
            # Don't reveal if email exists or not
            return JsonResponse({
                'success': True,
                'message': 'If an account exists with this email, a password reset link has been sent.'
            })
        
        # Generate reset token
        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(hours=24)
        
        reset_token = PasswordResetToken.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )
        
        # Send password reset email
        EmailService.send_password_reset_email(user, reset_token)
        
        # Log activity
        ActivityLogger.log(
            user_type='partner',
            user_id=user.id,
            user_name=user.username,
            action='password_reset_requested',
            request=request
        )
        
        return JsonResponse({
            'success': True,
            'message': 'If an account exists with this email, a password reset link has been sent.'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def partner_reset_password(request):
    """
    Reset password with token
    POST /api/v1/partner-portal/auth/reset-password
    Body: {"token": "...", "new_password": "..."}
    """
    import json
    
    try:
        data = json.loads(request.body)
        token = data.get('token', '').strip()
        new_password = data.get('new_password', '')
        
        if not token or not new_password:
            return JsonResponse({'error': 'Token and new password are required'}, status=400)
        
        # Validate password strength
        if len(new_password) < 8:
            return JsonResponse({'error': 'Password must be at least 8 characters'}, status=400)
        
        # Find valid token
        try:
            reset_token = PasswordResetToken.objects.select_related('user').get(token=token)
        except PasswordResetToken.DoesNotExist:
            return JsonResponse({'error': 'Invalid or expired token'}, status=400)
        
        if not reset_token.is_valid():
            return JsonResponse({'error': 'Invalid or expired token'}, status=400)
        
        # Update password
        user = reset_token.user
        user.password_hash = make_password(new_password)
        user.save(update_fields=['password_hash'])
        
        # Mark token as used
        reset_token.mark_as_used()
        
        # Log activity
        ActivityLogger.log(
            user_type='partner',
            user_id=user.id,
            user_name=user.username,
            action='password_reset',
            request=request
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Password has been reset successfully'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def partner_change_password(request):
    """
    Change password for logged-in user
    POST /api/v1/partner-portal/auth/change-password
    Body: {"current_password": "...", "new_password": "..."}
    """
    import json
    
    partner_user_id = request.session.get('partner_user_id')
    if not partner_user_id:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    try:
        data = json.loads(request.body)
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        
        if not current_password or not new_password:
            return JsonResponse({'error': 'Current and new password are required'}, status=400)
        
        # Validate password strength
        if len(new_password) < 8:
            return JsonResponse({'error': 'Password must be at least 8 characters'}, status=400)
        
        # Get user
        user = PartnerUser.objects.get(id=partner_user_id, is_active=True)
        
        # Verify current password
        if not check_password(current_password, user.password_hash):
            ActivityLogger.log(
                user_type='partner',
                user_id=user.id,
                user_name=user.username,
                action='password_change_failed',
                details={'reason': 'invalid_current_password'},
                request=request
            )
            return JsonResponse({'error': 'Current password is incorrect'}, status=400)
        
        # Update password
        user.password_hash = make_password(new_password)
        user.save(update_fields=['password_hash'])
        
        # Log activity
        ActivityLogger.log(
            user_type='partner',
            user_id=user.id,
            user_name=user.username,
            action='password_changed',
            request=request
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Password has been changed successfully'
        })
        
    except PartnerUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

"""
Activity Logger Service
Logs all user actions for audit trail
"""

from functools import wraps
from django.utils import timezone
from datetime import timedelta

from .partner_models import ActivityLog


class ActivityLogger:
    """Service for logging user activities"""
    
    @staticmethod
    def log(user_type, user_id, user_name, action, resource_type='', resource_id='', details=None, request=None):
        """
        Log a user activity
        
        Args:
            user_type: 'admin' or 'partner'
            user_id: ID of the user
            user_name: Username for display
            action: Action performed (login, upload, download, etc.)
            resource_type: Type of resource (transaction, partner, user, etc.)
            resource_id: ID of the resource
            details: Additional details (dict)
            request: Django request object (for IP and user agent)
        """
        ip_address = None
        user_agent = ''
        
        if request:
            # Get IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0].strip()
            else:
                ip_address = request.META.get('REMOTE_ADDR')
            
            # Get user agent
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
        
        try:
            ActivityLog.objects.create(
                user_type=user_type,
                user_id=user_id,
                user_name=user_name,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                details=details or {},
                ip_address=ip_address,
                user_agent=user_agent
            )
        except Exception as e:
            # Don't let logging errors break the application
            print(f"Failed to log activity: {e}")
    
    @staticmethod
    def log_admin(user, action, resource_type='', resource_id='', details=None, request=None):
        """Log an admin user activity"""
        ActivityLogger.log(
            user_type='admin',
            user_id=user.id,
            user_name=user.username,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            request=request
        )
    
    @staticmethod
    def log_partner(user, action, resource_type='', resource_id='', details=None, request=None):
        """Log a partner user activity"""
        ActivityLogger.log(
            user_type='partner',
            user_id=user.id,
            user_name=user.username,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            request=request
        )
    
    @staticmethod
    def cleanup_old_logs(days=90):
        """
        Delete activity logs older than specified days
        
        Args:
            days: Number of days to retain logs (default: 90)
        
        Returns:
            int: Number of logs deleted
        """
        cutoff_date = timezone.now() - timedelta(days=days)
        deleted_count, _ = ActivityLog.objects.filter(timestamp__lt=cutoff_date).delete()
        return deleted_count
    
    @staticmethod
    def get_user_activity(user_type, user_id, limit=100):
        """
        Get recent activity for a specific user
        
        Args:
            user_type: 'admin' or 'partner'
            user_id: User ID
            limit: Maximum number of logs to return
        
        Returns:
            QuerySet: Activity logs
        """
        return ActivityLog.objects.filter(
            user_type=user_type,
            user_id=user_id
        ).order_by('-timestamp')[:limit]
    
    @staticmethod
    def get_resource_activity(resource_type, resource_id, limit=100):
        """
        Get recent activity for a specific resource
        
        Args:
            resource_type: Type of resource
            resource_id: Resource ID
            limit: Maximum number of logs to return
        
        Returns:
            QuerySet: Activity logs
        """
        return ActivityLog.objects.filter(
            resource_type=resource_type,
            resource_id=resource_id
        ).order_by('-timestamp')[:limit]
    
    @staticmethod
    def get_action_count(action, user_type=None, days=30):
        """
        Get count of specific action in the last N days
        
        Args:
            action: Action to count
            user_type: Optional filter by user type
            days: Number of days to look back
        
        Returns:
            int: Count of actions
        """
        cutoff_date = timezone.now() - timedelta(days=days)
        query = ActivityLog.objects.filter(
            action=action,
            timestamp__gte=cutoff_date
        )
        
        if user_type:
            query = query.filter(user_type=user_type)
        
        return query.count()


def log_activity(action, resource_type='', get_resource_id=None):
    """
    Decorator to automatically log activity for a view
    
    Usage:
        @log_activity('file_upload', resource_type='transaction')
        def upload_view(request):
            pass
        
        @log_activity('transaction_view', resource_type='transaction', get_resource_id=lambda kwargs: kwargs.get('id'))
        def transaction_detail(request, id):
            pass
    
    Args:
        action: Action name to log
        resource_type: Type of resource being acted upon
        get_resource_id: Function to extract resource_id from view kwargs
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Execute the view
            response = view_func(request, *args, **kwargs)
            
            # Log the activity after successful execution
            try:
                # Determine user type and info
                if hasattr(request, 'partner_user'):
                    user_type = 'partner'
                    user_id = request.partner_user.id
                    user_name = request.partner_user.username
                elif request.user.is_authenticated:
                    user_type = 'admin'
                    user_id = request.user.id
                    user_name = request.user.username
                else:
                    # No authenticated user, skip logging
                    return response
                
                # Get resource ID if function provided
                resource_id = ''
                if get_resource_id and callable(get_resource_id):
                    resource_id = str(get_resource_id(kwargs))
                
                # Log the activity
                ActivityLogger.log(
                    user_type=user_type,
                    user_id=user_id,
                    user_name=user_name,
                    action=action,
                    resource_type=resource_type,
                    resource_id=resource_id,
                    details={
                        'method': request.method,
                        'path': request.path,
                        'status_code': response.status_code if hasattr(response, 'status_code') else None,
                    },
                    request=request
                )
            except Exception as e:
                # Don't let logging errors break the view
                print(f"Failed to log activity in decorator: {e}")
            
            return response
        
        return wrapper
    
    return decorator


def log_model_change(action, model_name):
    """
    Decorator to log model changes (create, update, delete)
    
    Usage:
        @log_model_change('partner_created', 'Partner')
        def create_partner(request):
            partner = Partner.objects.create(...)
            return partner
    
    Args:
        action: Action name (e.g., 'partner_created', 'user_updated')
        model_name: Name of the model being changed
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Execute the view
            result = view_func(request, *args, **kwargs)
            
            # Log the change
            try:
                if hasattr(request, 'partner_user'):
                    user_type = 'partner'
                    user_id = request.partner_user.id
                    user_name = request.partner_user.username
                elif request.user.is_authenticated:
                    user_type = 'admin'
                    user_id = request.user.id
                    user_name = request.user.username
                else:
                    return result
                
                # Try to get resource ID from result
                resource_id = ''
                if hasattr(result, 'id'):
                    resource_id = str(result.id)
                elif isinstance(result, dict) and 'id' in result:
                    resource_id = str(result['id'])
                
                ActivityLogger.log(
                    user_type=user_type,
                    user_id=user_id,
                    user_name=user_name,
                    action=action,
                    resource_type=model_name.lower(),
                    resource_id=resource_id,
                    request=request
                )
            except Exception as e:
                print(f"Failed to log model change: {e}")
            
            return result
        
        return wrapper
    
    return decorator

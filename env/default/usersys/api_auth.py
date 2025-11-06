"""
Bots EDI API Authentication
Token-based authentication and permission checking
"""

import time
from django.http import JsonResponse
from django.utils import timezone
from functools import wraps


def get_client_ip(request):
    """Extract client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def api_authenticate(required_permissions=None):
    """
    Decorator for API authentication and permission checking
    
    Usage:
        @api_authenticate(['file_upload', 'file_download'])
        def my_api_view(request):
            ...
    """
    if required_permissions is None:
        required_permissions = []
    
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            from .api_models import APIKey, APIAuditLog
            
            start_time = time.time()
            
            # Extract API key from header
            api_key_value = request.META.get('HTTP_X_API_KEY') or request.GET.get('api_key')
            
            if not api_key_value:
                return log_and_respond(
                    request, None, 'denied', 401,
                    {'error': 'API key required', 'message': 'Provide API key in X-API-Key header'},
                    start_time
                )
            
            # Validate API key
            try:
                api_key = APIKey.objects.get(key=api_key_value)
            except APIKey.DoesNotExist:
                return log_and_respond(
                    request, None, 'denied', 401,
                    {'error': 'Invalid API key'},
                    start_time
                )
            
            # Check if key is valid
            if not api_key.is_valid():
                return log_and_respond(
                    request, api_key, 'denied', 403,
                    {'error': 'API key expired or disabled'},
                    start_time
                )
            
            # Check IP whitelist
            client_ip = get_client_ip(request)
            if not api_key.check_ip(client_ip):
                return log_and_respond(
                    request, api_key, 'denied', 403,
                    {'error': 'IP address not allowed', 'ip': client_ip},
                    start_time
                )
            
            # Check rate limit
            if not api_key.check_rate_limit():
                return log_and_respond(
                    request, api_key, 'rate_limited', 429,
                    {
                        'error': 'Rate limit exceeded',
                        'limit': api_key.rate_limit,
                        'reset_time': api_key.usage_reset_time.isoformat()
                    },
                    start_time
                )
            
            # Check permissions
            for permission in required_permissions:
                if not api_key.has_permission(permission):
                    return log_and_respond(
                        request, api_key, 'denied', 403,
                        {
                            'error': 'Insufficient permissions',
                            'required': permission
                        },
                        start_time
                    )
            
            # Increment usage
            api_key.increment_usage()
            
            # Attach API key to request for use in view
            request.api_key = api_key
            request.api_start_time = start_time
            
            # Call the actual view
            try:
                response = view_func(request, *args, **kwargs)
                
                # Log successful request
                log_audit(
                    request, api_key, 'success',
                    response.status_code if hasattr(response, 'status_code') else 200,
                    '', start_time
                )
                
                return response
                
            except Exception as e:
                return log_and_respond(
                    request, api_key, 'failed', 500,
                    {'error': 'Internal server error', 'message': str(e)},
                    start_time
                )
        
        return wrapped_view
    return decorator


def log_and_respond(request, api_key, status, code, response_data, start_time):
    """Log the request and return JSON response"""
    log_audit(request, api_key, status, code, response_data.get('error', ''), start_time)
    return JsonResponse(response_data, status=code)


def log_audit(request, api_key, status, code, message, start_time):
    """Create audit log entry"""
    from .api_models import APIAuditLog
    
    duration = int((time.time() - start_time) * 1000)  # Convert to milliseconds
    
    APIAuditLog.objects.create(
        api_key=api_key,
        endpoint=request.path,
        method=request.method,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
        request_data=str(request.GET.dict())[:1000],  # Sanitized
        response_status=status,
        response_code=code,
        response_message=str(message)[:500],
        duration_ms=duration
    )

"""
Modern EDI Interface Middleware
Rate limiting and security middleware
"""

import time
from django.core.cache import cache
from django.http import JsonResponse
from django.conf import settings


class RateLimitMiddleware:
    """
    Rate limiting middleware for Modern EDI API
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Requests per minute per user
        self.rate_limit = getattr(settings, 'MODERN_EDI_RATE_LIMIT', 60)
        self.rate_window = 60  # seconds
    
    def __call__(self, request):
        # Only apply to Modern EDI API endpoints
        if not request.path.startswith('/modern-edi/api/'):
            return self.get_response(request)
        
        # Skip rate limiting for unauthenticated requests (will be handled by auth)
        if not request.user.is_authenticated:
            return self.get_response(request)
        
        # Check rate limit
        if not self.check_rate_limit(request):
            return JsonResponse({
                'error': 'Rate limit exceeded',
                'message': f'Maximum {self.rate_limit} requests per minute allowed'
            }, status=429)
        
        response = self.get_response(request)
        return response
    
    def check_rate_limit(self, request):
        """Check if user has exceeded rate limit"""
        user_id = request.user.id
        cache_key = f'modern_edi_rate_limit_{user_id}'
        
        # Get current request count
        request_count = cache.get(cache_key, 0)
        
        if request_count >= self.rate_limit:
            return False
        
        # Increment counter
        cache.set(cache_key, request_count + 1, self.rate_window)
        
        return True


class SecurityHeadersMiddleware:
    """
    Add security headers to Modern EDI API responses
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Only apply to Modern EDI API endpoints
        if request.path.startswith('/modern-edi/api/'):
            # Add security headers
            response['X-Content-Type-Options'] = 'nosniff'
            response['X-Frame-Options'] = 'DENY'
            response['X-XSS-Protection'] = '1; mode=block'
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            
            # CORS headers (adjust as needed for your frontend)
            if hasattr(settings, 'MODERN_EDI_ALLOWED_ORIGINS'):
                origin = request.META.get('HTTP_ORIGIN')
                if origin in settings.MODERN_EDI_ALLOWED_ORIGINS:
                    response['Access-Control-Allow-Origin'] = origin
                    response['Access-Control-Allow-Credentials'] = 'true'
                    response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
                    response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        
        return response


class AuditLoggingMiddleware:
    """
    Log all API requests for audit purposes
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Only apply to Modern EDI API endpoints
        if not request.path.startswith('/modern-edi/api/'):
            return self.get_response(request)
        
        # Record start time
        start_time = time.time()
        
        # Process request
        response = self.get_response(request)
        
        # Calculate duration
        duration_ms = int((time.time() - start_time) * 1000)
        
        # Log request (in production, this would go to a proper logging system)
        if request.user.is_authenticated:
            log_data = {
                'user': request.user.username,
                'method': request.method,
                'path': request.path,
                'status_code': response.status_code,
                'duration_ms': duration_ms,
                'ip_address': self.get_client_ip(request),
                'user_agent': request.META.get('HTTP_USER_AGENT', '')[:200],
            }
            
            # In production, log to database or logging service
            # For now, we'll just use Django's logging
            import logging
            logger = logging.getLogger('modern_edi.api')
            logger.info(f"API Request: {log_data}")
        
        return response
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

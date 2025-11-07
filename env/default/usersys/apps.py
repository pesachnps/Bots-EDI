"""
Usersys Django App Configuration
"""

from django.apps import AppConfig


class UsersysConfig(AppConfig):
    """Configuration for the usersys Django app"""
    
    name = 'usersys'
    verbose_name = 'User System and Modern EDI Interface'
    
    def ready(self):
        """Import models when app is ready"""
        # Import models to ensure they're registered
        from . import api_models
        from . import modern_edi_models
        
        # Register custom URLs with bots
        # Disabled for now - URLs need to be registered differently
        # self._register_urls()

    
    def _register_urls(self):
        """Register custom URLs with the bots URL configuration"""
        try:
            from django.urls import URLResolver
            from django.conf import settings
            import importlib
            
            # Get the root URL configuration module
            urlconf_module = importlib.import_module(settings.ROOT_URLCONF)
            
            # Import our custom URLs
            from . import urls as usersys_urls
            
            # Add our URL patterns to the root configuration
            if hasattr(urlconf_module, 'urlpatterns'):
                # Check if our URLs are already registered (avoid duplicates)
                existing_patterns = [str(p.pattern) for p in urlconf_module.urlpatterns if hasattr(p, 'pattern')]
                
                for pattern in usersys_urls.urlpatterns:
                    pattern_str = str(pattern.pattern)
                    if pattern_str not in existing_patterns:
                        urlconf_module.urlpatterns.append(pattern)
        except Exception as e:
            # Log error but don't fail app initialization
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to register custom URLs: {e}")

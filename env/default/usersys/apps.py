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

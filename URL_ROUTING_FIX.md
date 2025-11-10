# URL Routing Fix

## Problem
The modern EDI interface and admin/partner portal URLs are not being registered with the Django URL configuration. The frontend is calling `/modern-edi/api/v1/folders/` but getting a 404 error.

## Root Cause
The bots system uses a custom configuration directory structure where:
- Config files are in `C:\Users\PGelfand\.bots\env\default\config\`
- Code files should be in `C:\Users\PGelfand\.bots\env\default\usersys\`

The URL patterns defined in `usersys/modern_edi_urls.py`, `usersys/admin_urls.py`, and `usersys/partner_portal_urls.py` need to be registered with the main bots URL configuration.

## Solution

### Option 1: Manual URL Registration (Recommended)
Create a file `C:\Users\PGelfand\.bots\env\default\usersys\url_extensions.py`:

```python
"""
URL Extensions for Modern EDI Interface
This file is automatically loaded by the usersys app to extend bots URLs
"""

def register_urls():
    """Register custom URLs with bots"""
    try:
        from django.conf import settings
        import importlib
        
        # Get the root URL configuration
        urlconf_module = importlib.import_module(settings.ROOT_URLCONF)
        
        # Import our URL patterns
        from django.urls import path, include
        
        # Add our patterns
        new_patterns = [
            path('modern-edi/', include('usersys.modern_edi_urls')),
            path('modern-edi/api/v1/admin/', include('usersys.admin_urls')),
            path('api/v1/partner/', include('usersys.partner_portal_urls')),
        ]
        
        # Append to existing patterns
        if hasattr(urlconf_module, 'urlpatterns'):
            for pattern in new_patterns:
                if pattern not in urlconf_module.urlpatterns:
                    urlconf_module.urlpatterns.append(pattern)
                    
        return True
    except Exception as e:
        print(f"Failed to register URLs: {e}")
        return False
```

Then update `C:\Users\PGelfand\.bots\env\default\usersys\apps.py` to call this function in the `ready()` method.

### Option 2: Direct Bots URLs Modification
Modify the bots package's `urls.py` file directly (not recommended as it affects the installed package).

### Option 3: Use Django's URL Configuration Override
Set `ROOT_URLCONF` in settings.py to point to a custom URLs file that includes both bots URLs and our custom URLs.

## Files to Copy
Ensure these files are in `C:\Users\PGelfand\.bots\env\default\usersys\`:
- `modern_edi_urls.py`
- `admin_urls.py`
- `partner_portal_urls.py`
- `modern_edi_views.py`
- `admin_views.py`
- `partner_portal_views.py`
- `apps.py` (with URL registration code)
- All supporting files (models, services, etc.)

## Testing
After implementing the fix, test with:
```bash
curl http://localhost:8080/modern-edi/api/v1/folders/
```

Should return JSON with folder list instead of 404.

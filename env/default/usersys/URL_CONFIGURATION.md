# URL Configuration Guide

## Overview

This document explains how to integrate the Admin Dashboard and Partner Portal URLs into your Django project.

## URL Structure

```
/modern-edi/
├── api/v1/                          # Existing Modern EDI API
│   ├── transactions/                # Transaction endpoints
│   ├── folders/                     # Folder endpoints
│   └── ...
│
├── api/v1/admin/                    # NEW: Admin Dashboard API
│   ├── dashboard/metrics            # Dashboard metrics
│   ├── dashboard/charts             # Chart data
│   ├── partners                     # Partner management
│   ├── users/<id>                   # User management
│   ├── analytics/                   # Analytics endpoints
│   └── activity-logs                # Activity logs
│
└── api/v1/partner-portal/           # NEW: Partner Portal API
    ├── auth/login                   # Authentication
    ├── dashboard/metrics            # Partner dashboard
    ├── transactions                 # Partner transactions
    ├── files/upload                 # File upload
    ├── files/download               # File download
    └── settings                     # Partner settings
```

## Integration Steps

### Step 1: Update Main URLs File

Add these includes to your main `urls.py` file (typically in `env/default/config/urls.py` or similar):

```python
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    # ... existing patterns ...
    
    # Modern EDI Interface (existing)
    path('modern-edi/', include('usersys.modern_edi_urls')),
    
    # NEW: Admin Dashboard API
    path('modern-edi/api/v1/admin/', include('usersys.admin_urls')),
    
    # NEW: Partner Portal API
    path('modern-edi/api/v1/partner-portal/', include('usersys.partner_portal_urls')),
    
    # Serve React SPA (catch-all for client-side routing)
    re_path(r'^modern-edi/.*', TemplateView.as_view(template_name='modern-edi/index.html')),
]
```

### Step 2: Update Middleware Settings

Add the new middleware to your `settings.py`:

```python
MIDDLEWARE = [
    # ... existing middleware ...
    'usersys.partner_auth_middleware.AdminAuthMiddleware',
    'usersys.partner_auth_middleware.PartnerAuthMiddleware',
    'usersys.partner_auth_middleware.PartnerPermissionMiddleware',
]
```

### Step 3: Update Installed Apps

Ensure 'usersys' is in your INSTALLED_APPS:

```python
INSTALLED_APPS = [
    # ... other apps ...
    'usersys',
]
```

## API Endpoints Reference

### Admin Dashboard Endpoints

**Dashboard:**
- `GET /modern-edi/api/v1/admin/dashboard/metrics?days=30`
- `GET /modern-edi/api/v1/admin/dashboard/charts?days=30`

**Partner Management:**
- `GET /modern-edi/api/v1/admin/partners?search=&status=&page=1`
- `GET /modern-edi/api/v1/admin/partners/<uuid>/analytics?days=30`
- `GET /modern-edi/api/v1/admin/partners/<uuid>/users`
- `POST /modern-edi/api/v1/admin/partners/<uuid>/users`

**User Management:**
- `PUT /modern-edi/api/v1/admin/users/<id>`
- `DELETE /modern-edi/api/v1/admin/users/<id>`
- `POST /modern-edi/api/v1/admin/users/<id>/reset-password`
- `PUT /modern-edi/api/v1/admin/users/<id>/permissions`

**Analytics:**
- `GET /modern-edi/api/v1/admin/analytics/transactions?days=30`
- `GET /modern-edi/api/v1/admin/analytics/partners?days=30`
- `GET /modern-edi/api/v1/admin/analytics/documents?days=30`

**Activity Logs:**
- `GET /modern-edi/api/v1/admin/activity-logs?search=&user_type=&action=&page=1`
- `GET /modern-edi/api/v1/admin/activity-logs/export`

### Partner Portal Endpoints

**Authentication:**
- `POST /modern-edi/api/v1/partner-portal/auth/login`
- `POST /modern-edi/api/v1/partner-portal/auth/logout`
- `GET /modern-edi/api/v1/partner-portal/auth/me`
- `POST /modern-edi/api/v1/partner-portal/auth/forgot-password`
- `POST /modern-edi/api/v1/partner-portal/auth/reset-password`
- `POST /modern-edi/api/v1/partner-portal/auth/change-password`

**Dashboard:**
- `GET /modern-edi/api/v1/partner-portal/dashboard/metrics?days=30`

**Transactions:**
- `GET /modern-edi/api/v1/partner-portal/transactions?search=&status=&type=&page=1`
- `GET /modern-edi/api/v1/partner-portal/transactions/<uuid>`

**Files:**
- `POST /modern-edi/api/v1/partner-portal/files/upload`
- `GET /modern-edi/api/v1/partner-portal/files/download`
- `GET /modern-edi/api/v1/partner-portal/files/download/<uuid>`
- `POST /modern-edi/api/v1/partner-portal/files/download/bulk`

**Settings:**
- `GET /modern-edi/api/v1/partner-portal/settings`
- `PUT /modern-edi/api/v1/partner-portal/settings/contact`
- `POST /modern-edi/api/v1/partner-portal/settings/test-connection`

## Authentication

### Admin Dashboard
- Uses Django's built-in session authentication
- Requires `is_staff=True` on user account
- Checked by `AdminAuthMiddleware`

### Partner Portal
- Uses custom session authentication
- Session key: `partner_user_id`
- Checked by `PartnerAuthMiddleware`
- Permissions checked by `PartnerPermissionMiddleware`

## Testing Endpoints

### Test Admin Endpoint
```bash
curl -X GET http://localhost:8080/modern-edi/api/v1/admin/dashboard/metrics \
  -H "Cookie: sessionid=<your-session-id>"
```

### Test Partner Portal Endpoint
```bash
# Login first
curl -X POST http://localhost:8080/modern-edi/api/v1/partner-portal/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'

# Then use returned session
curl -X GET http://localhost:8080/modern-edi/api/v1/partner-portal/dashboard/metrics \
  -H "Cookie: sessionid=<session-from-login>"
```

## Troubleshooting

### 404 Not Found
- Check that URLs are included in main urls.py
- Verify URL patterns match exactly
- Check that middleware is installed

### 401 Unauthorized
- Verify user is logged in
- Check session cookie is being sent
- For admin: ensure user has `is_staff=True`
- For partner: ensure partner_user_id is in session

### 403 Forbidden
- Check user permissions
- For admin: verify `is_staff=True`
- For partner: check PartnerPermission settings

### 500 Internal Server Error
- Check Django logs
- Verify database migrations are run
- Ensure all models are imported correctly

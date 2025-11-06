# Admin Dashboard & Partner Portal - Deployment Guide

## Quick Start

### 1. Run Database Migrations

```bash
cd env/default
python manage.py makemigrations usersys
python manage.py migrate usersys
```

### 2. Initialize Partner Portal

```bash
python manage.py init_partner_portal
```

Or with sample data for testing:

```bash
python manage.py init_partner_portal --create-sample
```

### 3. Configure URLs

Add to your main `urls.py` (or `config/urls.py`):

```python
from django.urls import path, include

urlpatterns = [
    # Existing patterns...
    
    # Admin Dashboard API
    path('modern-edi/api/v1/admin/', include('usersys.admin_urls')),
    
    # Partner Portal API
    path('modern-edi/api/v1/partner-portal/', include('usersys.partner_portal_urls')),
]
```

### 4. Configure Middleware

Add to `settings.py`:

```python
MIDDLEWARE = [
    # ... existing middleware ...
    'usersys.partner_auth_middleware.AdminAuthMiddleware',
    'usersys.partner_auth_middleware.PartnerAuthMiddleware',
    'usersys.partner_auth_middleware.PartnerPermissionMiddleware',
]
```

### 5. Configure Email (Optional)

For password reset functionality, add to `settings.py` or `.env`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-password'
DEFAULT_FROM_EMAIL = 'noreply@example.com'
SITE_URL = 'http://localhost:8080'
```

### 6. Start Server

```bash
cd env/default
bots-webserver
```

## Access Points

- **Modern EDI Interface:** http://localhost:8080/modern-edi/
- **Admin Dashboard:** http://localhost:8080/modern-edi/admin/
- **Partner Portal:** http://localhost:8080/modern-edi/partner-portal/

## Creating Your First Partner User

### Option 1: Django Shell

```python
python manage.py shell

from usersys.user_manager import UserManager
from usersys.partner_models import Partner

# Get a partner
partner = Partner.objects.first()

# Create user
user = UserManager.create_user(
    partner_id=partner.id,
    username='testuser',
    email='test@example.com',
    password='Test123!@#',
    first_name='Test',
    last_name='User',
    role='partner_admin'
)

print(f"Created user: {user.username}")
```

### Option 2: Sample Data Command

```bash
python manage.py init_partner_portal --create-sample
```

This creates 3 users for the first active partner:
- `{partner_id}_admin` (password: Admin123!@#)
- `{partner_id}_user` (password: User123!@#)
- `{partner_id}_readonly` (password: Read123!@#)

## Testing the Backend

### Test Partner Login

```bash
curl -X POST http://localhost:8080/modern-edi/api/v1/partner-portal/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "Test123!@#"}'
```

### Test Dashboard Metrics

```bash
# Get session cookie from login response, then:
curl -X GET http://localhost:8080/modern-edi/api/v1/partner-portal/dashboard/metrics \
  -H "Cookie: sessionid=<your-session-id>"
```

### Test Admin Endpoints

```bash
# Login as Django admin first, then:
curl -X GET http://localhost:8080/modern-edi/api/v1/admin/dashboard/metrics \
  -H "Cookie: sessionid=<admin-session-id>"
```

## Maintenance Commands

### Cleanup Old Activity Logs

```bash
# Delete logs older than 90 days
python manage.py cleanup_activity_logs --days 90

# Dry run to see what would be deleted
python manage.py cleanup_activity_logs --days 90 --dry-run
```

### Check Partner Users

```python
python manage.py shell

from usersys.partner_models import PartnerUser

# List all users
for user in PartnerUser.objects.all():
    print(f"{user.username} - {user.partner.name} - {user.role}")
```

## Security Checklist

- [ ] Change default passwords for sample users
- [ ] Configure email for password reset
- [ ] Set up HTTPS in production
- [ ] Configure SESSION_COOKIE_SECURE = True in production
- [ ] Set strong SECRET_KEY in settings
- [ ] Enable CSRF protection
- [ ] Configure allowed hosts
- [ ] Set up regular activity log cleanup
- [ ] Review and customize permission defaults
- [ ] Test account lockout functionality

## Troubleshooting

### Migrations Fail

```bash
# Check migration status
python manage.py showmigrations usersys

# If needed, fake the migration
python manage.py migrate usersys --fake 0004
```

### Import Errors

Ensure all new files are in the `usersys` directory and Python can import them:

```python
python manage.py shell
from usersys import partner_models, user_manager, analytics_service
```

### Session Issues

Clear sessions if having authentication problems:

```python
python manage.py shell
from django.contrib.sessions.models import Session
Session.objects.all().delete()
```

### Permission Errors

Recreate permissions for all users:

```bash
python manage.py init_partner_portal
```

## Production Deployment

### 1. Environment Variables

Create `.env` file with:

```
DEBUG=False
SECRET_KEY=<generate-strong-key>
ALLOWED_HOSTS=yourdomain.com
DATABASE_ENGINE=postgresql
DATABASE_NAME=bots_db
DATABASE_USER=bots_user
DATABASE_PASSWORD=<strong-password>
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Email
EMAIL_HOST=smtp.yourdomain.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=<email-password>
SITE_URL=https://yourdomain.com

# Partner Portal
PARTNER_SESSION_TIMEOUT=1800
PARTNER_MAX_UPLOAD_SIZE=10485760
PARTNER_FAILED_LOGIN_LOCKOUT=5
PARTNER_LOCKOUT_DURATION=900
```

### 2. Database Setup

```bash
# Create PostgreSQL database
createdb bots_db

# Run migrations
python manage.py migrate

# Initialize
python init_admin_partner_portals.py
```

### 3. Security Settings

Update `settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
```

### 4. Static Files

```bash
python manage.py collectstatic
```

### 5. Start Server

```bash
bots-webserver
```

## Monitoring

### Activity Log Monitoring

```python
from usersys.partner_models import ActivityLog

# Recent failed logins
ActivityLog.objects.filter(action='login_failed').order_by('-timestamp')[:10]

# Recent file uploads
ActivityLog.objects.filter(action='file_uploaded').order_by('-timestamp')[:10]
```

### User Statistics

```python
from usersys.user_manager import UserManager

# Get user stats
stats = UserManager.get_user_stats(user_id)
print(stats)
```

## Summary

The Admin Dashboard & Partner Portal backend is fully implemented and ready for deployment. Follow this guide to set up the system, create users, and begin testing.

For frontend development, refer to `FRONTEND_IMPLEMENTATION_GUIDE.md`.

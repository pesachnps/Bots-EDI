# Backend Deployment Checklist

## Overview

This checklist ensures all backend components for the Admin Dashboard and Partner Portal are properly deployed and configured.

## Pre-Deployment Verification

### 1. Environment Setup

- [ ] Python 3.8+ installed
- [ ] Django 3.2+ installed
- [ ] All dependencies from requirements.txt installed
- [ ] Database (SQLite/PostgreSQL/MySQL) configured
- [ ] .env file created from .env.example
- [ ] SECRET_KEY set to unique value
- [ ] DEBUG=False in production

### 2. Database Configuration

- [ ] Database migrations created
- [ ] Run: `python manage.py makemigrations usersys`
- [ ] Run: `python manage.py migrate`
- [ ] Verify migrations applied: `python manage.py showmigrations`

### 3. Email Configuration

- [ ] EMAIL_HOST configured in .env
- [ ] EMAIL_PORT configured in .env
- [ ] DEFAULT_FROM_EMAIL set
- [ ] SITE_URL set (for email links)
- [ ] SITE_NAME set
- [ ] Test email sending (optional)

### 4. Partner Portal Settings

- [ ] PARTNER_SESSION_TIMEOUT configured (default: 1800 seconds)
- [ ] PARTNER_MAX_UPLOAD_SIZE configured (default: 10MB)
- [ ] PARTNER_FAILED_LOGIN_LOCKOUT configured (default: 5)
- [ ] PARTNER_LOCKOUT_DURATION configured (default: 900 seconds)
- [ ] PARTNER_PASSWORD_MIN_LENGTH configured (default: 8)

## Backend Component Verification

### 5. Models

Run verification script:
```bash
cd env/default
python usersys/verify_backend.py
```

Verify all models exist:
- [ ] Partner model
- [ ] PartnerSFTPConfig model
- [ ] PartnerAPIConfig model
- [ ] PartnerUser model
- [ ] PartnerPermission model
- [ ] ActivityLog model
- [ ] PasswordResetToken model

### 6. Services

Verify all services are accessible:
- [ ] UserManager service
- [ ] AnalyticsService service
- [ ] ActivityLogger service
- [ ] EmailService service

### 7. Utilities

Verify all utilities are accessible:
- [ ] PasswordValidator
- [ ] TokenGenerator
- [ ] SessionManager
- [ ] IPAddressHelper
- [ ] AccountLockoutManager

### 8. Middleware

Verify middleware is configured in settings.py:
- [ ] PartnerAuthMiddleware added to MIDDLEWARE
- [ ] Middleware order is correct (after SessionMiddleware)

### 9. URL Configuration

Verify URL patterns are configured:
- [ ] Admin dashboard URLs included
- [ ] Partner portal URLs included
- [ ] Modern EDI URLs included
- [ ] Catch-all route for React SPA configured

## Data Initialization

### 10. Initialize System Data

Run initialization script:
```bash
cd env/default
python usersys/init_admin_partner_portals.py
```

This will:
- [ ] Create default permission sets
- [ ] Set up activity log retention policy
- [ ] Create sample data (if requested)

### 11. Create Admin User

```bash
cd env/default
python manage_users.py create admin YourSecurePassword123!
```

- [ ] Admin user created
- [ ] Admin user can log in to Django admin
- [ ] Admin user has staff status

### 12. Create Test Partner (Optional)

For testing purposes:
- [ ] Create test partner via Django admin
- [ ] Create test partner user
- [ ] Verify test user can log in to partner portal

## API Endpoint Verification

### 13. Admin Dashboard Endpoints

Test these endpoints (requires admin authentication):

**Dashboard:**
- [ ] GET /modern-edi/api/v1/admin/dashboard/metrics
- [ ] GET /modern-edi/api/v1/admin/dashboard/charts

**Partner Management:**
- [ ] GET /modern-edi/api/v1/admin/partners/
- [ ] GET /modern-edi/api/v1/admin/partners/<id>/analytics
- [ ] GET /modern-edi/api/v1/admin/partners/<id>/users
- [ ] POST /modern-edi/api/v1/admin/partners/<id>/users

**User Management:**
- [ ] PUT /modern-edi/api/v1/admin/users/<id>
- [ ] DELETE /modern-edi/api/v1/admin/users/<id>
- [ ] POST /modern-edi/api/v1/admin/users/<id>/reset-password
- [ ] PUT /modern-edi/api/v1/admin/users/<id>/permissions

**Analytics:**
- [ ] GET /modern-edi/api/v1/admin/analytics/transactions
- [ ] GET /modern-edi/api/v1/admin/analytics/partners
- [ ] GET /modern-edi/api/v1/admin/analytics/documents

**Activity Logs:**
- [ ] GET /modern-edi/api/v1/admin/activity-logs
- [ ] GET /modern-edi/api/v1/admin/activity-logs/export

### 14. Partner Portal Endpoints

Test these endpoints (requires partner authentication):

**Authentication:**
- [ ] POST /modern-edi/api/v1/partner-portal/auth/login
- [ ] POST /modern-edi/api/v1/partner-portal/auth/logout
- [ ] GET /modern-edi/api/v1/partner-portal/auth/me
- [ ] POST /modern-edi/api/v1/partner-portal/auth/forgot-password
- [ ] POST /modern-edi/api/v1/partner-portal/auth/reset-password
- [ ] POST /modern-edi/api/v1/partner-portal/auth/change-password

**Dashboard:**
- [ ] GET /modern-edi/api/v1/partner-portal/dashboard/metrics

**Transactions:**
- [ ] GET /modern-edi/api/v1/partner-portal/transactions
- [ ] GET /modern-edi/api/v1/partner-portal/transactions/<id>

**File Operations:**
- [ ] POST /modern-edi/api/v1/partner-portal/files/upload
- [ ] GET /modern-edi/api/v1/partner-portal/files/download
- [ ] GET /modern-edi/api/v1/partner-portal/files/download/<id>
- [ ] POST /modern-edi/api/v1/partner-portal/files/download/bulk

**Settings:**
- [ ] GET /modern-edi/api/v1/partner-portal/settings
- [ ] PUT /modern-edi/api/v1/partner-portal/settings/contact
- [ ] POST /modern-edi/api/v1/partner-portal/settings/test-connection

## Security Verification

### 15. Authentication & Authorization

- [ ] Admin endpoints require staff authentication
- [ ] Partner endpoints require partner authentication
- [ ] Permission checks are enforced
- [ ] Partner data isolation is working (partners see only their data)
- [ ] Account lockout works after 5 failed attempts
- [ ] Session timeout works (30 minutes)

### 16. Password Security

- [ ] Passwords are hashed (never stored in plain text)
- [ ] Password complexity requirements enforced
- [ ] Password reset tokens expire after 24 hours
- [ ] Password reset tokens are single-use

### 17. Activity Logging

- [ ] All login attempts are logged
- [ ] All file operations are logged
- [ ] All user management actions are logged
- [ ] All permission changes are logged
- [ ] IP addresses are captured
- [ ] User agents are captured

### 18. Data Validation

- [ ] File upload size limits enforced (10 MB)
- [ ] File type validation working
- [ ] Email format validation working
- [ ] Username uniqueness enforced
- [ ] SQL injection prevention (using ORM)

## Performance Verification

### 19. Database Performance

- [ ] Indexes created on frequently queried fields
- [ ] Query performance acceptable (<100ms for most queries)
- [ ] Pagination working for large result sets
- [ ] select_related and prefetch_related used where appropriate

### 20. Caching

- [ ] Dashboard metrics cached (60-second TTL)
- [ ] Chart data cached (5-minute TTL)
- [ ] Cache invalidation working on data changes

## Monitoring & Maintenance

### 21. Logging

- [ ] Application logs configured
- [ ] Error logs configured
- [ ] Log rotation configured
- [ ] Log level appropriate for environment (INFO in production)

### 22. Activity Log Cleanup

Set up cron job for activity log cleanup:
```bash
# Run daily at 2 AM
0 2 * * * cd /path/to/env/default && python manage.py cleanup_activity_logs
```

- [ ] Cron job configured
- [ ] Activity log retention period set (default: 90 days)

### 23. Backup

- [ ] Database backup strategy in place
- [ ] Backup schedule configured
- [ ] Backup restoration tested

## Production Deployment

### 24. Web Server Configuration

- [ ] Bots webserver configured
- [ ] Port configured (default: 8080)
- [ ] ALLOWED_HOSTS configured in settings
- [ ] Static files collected: `python manage.py collectstatic`

### 25. HTTPS/SSL

- [ ] SSL certificate installed
- [ ] HTTPS enforced
- [ ] Secure cookies enabled (SECURE_SSL_REDIRECT=True)
- [ ] HSTS configured

### 26. Firewall

- [ ] Firewall rules configured
- [ ] Only necessary ports open
- [ ] Database port not exposed externally

## Post-Deployment Testing

### 27. Smoke Tests

- [ ] Admin can log in to Django admin
- [ ] Admin can access admin dashboard
- [ ] Partner user can log in to partner portal
- [ ] Partner user can view transactions
- [ ] Partner user can upload file
- [ ] Partner user can download file
- [ ] Email notifications working
- [ ] Activity logging working

### 28. Load Testing (Optional)

- [ ] Test with expected concurrent users
- [ ] Test file upload under load
- [ ] Test database query performance under load
- [ ] Monitor memory usage
- [ ] Monitor CPU usage

## Documentation

### 29. User Documentation

- [ ] Admin Dashboard Guide available
- [ ] Partner Portal Guide available
- [ ] User Management Guide available
- [ ] API Documentation available

### 30. Technical Documentation

- [ ] Deployment guide available
- [ ] Architecture documentation available
- [ ] Troubleshooting guide available
- [ ] Runbook for common operations

## Final Checklist

- [ ] All backend components deployed
- [ ] All endpoints tested and working
- [ ] Security measures in place
- [ ] Monitoring configured
- [ ] Backups configured
- [ ] Documentation complete
- [ ] Stakeholders notified
- [ ] Training provided (if needed)

## Rollback Plan

In case of issues:

1. **Database Rollback:**
   ```bash
   python manage.py migrate usersys <previous_migration_number>
   ```

2. **Code Rollback:**
   - Revert to previous Git commit
   - Restart web server

3. **Data Restore:**
   - Restore database from backup
   - Verify data integrity

## Support Contacts

- **System Administrator:** [contact info]
- **Database Administrator:** [contact info]
- **Development Team:** [contact info]

## Notes

- Date Deployed: _______________
- Deployed By: _______________
- Version: _______________
- Issues Encountered: _______________
- Resolution: _______________

# Backend Operations Guide

## Quick Reference for Common Backend Operations

### User Management

#### Create Partner User

```python
from usersys.user_manager import UserManager

# Create user with email notification
user, password = UserManager.create_user(
    partner_id='<partner-uuid>',
    username='john_doe',
    email='john@example.com',
    password='TempPass123!',
    first_name='John',
    last_name='Doe',
    role='partner_user',  # or 'partner_admin', 'partner_readonly'
    phone='+1-555-0123',
    send_email=True  # Sends welcome email
)
print(f"User created: {user.username}")
print(f"Temporary password: {password}")
```

#### Update Partner User

```python
from usersys.user_manager import UserManager

user = UserManager.update_user(
    user_id=123,
    email='newemail@example.com',
    first_name='Jane',
    role='partner_admin',
    is_active=True
)
```

#### Reset User Password

```python
from usersys.user_manager import UserManager

user = UserManager.reset_password(
    user_id=123,
    new_password='NewSecurePass123!'
)
```

#### Deactivate User

```python
from usersys.user_manager import UserManager

user = UserManager.deactivate_user(user_id=123)
```

### Activity Logging

#### Log Admin Action

```python
from usersys.activity_logger import ActivityLogger

ActivityLogger.log_admin(
    admin_user=request.user,
    action='partner_created',
    resource_type='partner',
    resource_id='partner-uuid',
    details={'name': 'Acme Corp'},
    request=request
)
```

#### Log Partner Action

```python
from usersys.activity_logger import ActivityLogger

ActivityLogger.log_partner(
    partner_user=request.partner_user,
    action='file_uploaded',
    resource_type='transaction',
    resource_id='transaction-id',
    details={'filename': 'invoice.edi', 'size': 2048},
    request=request
)
```

#### Query Activity Logs

```python
from usersys.partner_models import ActivityLog
from datetime import timedelta
from django.utils import timezone

# Get logs from last 7 days
seven_days_ago = timezone.now() - timedelta(days=7)
recent_logs = ActivityLog.objects.filter(
    timestamp__gte=seven_days_ago
).order_by('-timestamp')

# Get logs for specific user
user_logs = ActivityLog.objects.filter(
    user_type='partner',
    user_id=123
).order_by('-timestamp')

# Get logs for specific action
login_logs = ActivityLog.objects.filter(
    action='login'
).order_by('-timestamp')
```

### Analytics

#### Get Dashboard Metrics

```python
from usersys.analytics_service import AnalyticsService

# Get metrics for last 30 days
metrics = AnalyticsService.get_dashboard_metrics(days=30)

print(f"Total Partners: {metrics['total_partners']}")
print(f"Total Transactions: {metrics['total_transactions']}")
print(f"Success Rate: {metrics['success_rate']}%")
```

#### Get Partner Analytics

```python
from usersys.analytics_service import AnalyticsService

# Get analytics for specific partner
analytics = AnalyticsService.get_partner_analytics(
    partner_id='partner-uuid',
    days=30
)

print(f"Sent: {analytics['sent_count']}")
print(f"Received: {analytics['received_count']}")
print(f"Success Rate: {analytics['success_rate']}%")
```

#### Get Transaction Volume Data

```python
from usersys.analytics_service import AnalyticsService

# Get transaction volume for charts
volume_data = AnalyticsService.get_transaction_volume(days=30)

for day_data in volume_data:
    print(f"{day_data['date']}: {day_data['count']} transactions")
```

### Email Notifications

#### Send Password Reset Email

```python
from usersys.email_service import EmailService
from usersys.partner_models import PartnerUser, PasswordResetToken
from datetime import timedelta
from django.utils import timezone
import secrets

# Get user
user = PartnerUser.objects.get(email='user@example.com')

# Create reset token
token = secrets.token_urlsafe(32)
reset_token = PasswordResetToken.objects.create(
    user=user,
    token=token,
    expires_at=timezone.now() + timedelta(hours=24)
)

# Send email
EmailService.send_password_reset_email(user, reset_token)
```

#### Send Account Created Email

```python
from usersys.email_service import EmailService

# Send welcome email with credentials
EmailService.send_account_created_email(
    user=user,
    temporary_password='TempPass123!'
)
```

### Password Management

#### Validate Password

```python
from usersys.partner_auth_utils import PasswordValidator

is_valid, error_msg = PasswordValidator.validate('MyPassword123!')

if is_valid:
    print("Password is valid")
else:
    print(f"Password invalid: {error_msg}")
```

#### Hash Password

```python
from usersys.partner_auth_utils import PasswordValidator

password_hash = PasswordValidator.hash_password('MyPassword123!')
```

#### Verify Password

```python
from usersys.partner_auth_utils import PasswordValidator

is_correct = PasswordValidator.verify_password(
    'MyPassword123!',
    password_hash
)
```

### Session Management

#### Check Session Validity

```python
from usersys.partner_auth_utils import SessionManager

is_valid, reason = SessionManager.is_session_valid(
    request,
    timeout_seconds=1800  # 30 minutes
)

if is_valid:
    print("Session is valid")
else:
    print(f"Session invalid: {reason}")
```

#### Update Session Activity

```python
from usersys.partner_auth_utils import SessionManager

SessionManager.update_activity(request)
```

#### Destroy Session

```python
from usersys.partner_auth_utils import SessionManager

SessionManager.destroy_session(request)
```

### Account Lockout

#### Check if Account is Locked

```python
from usersys.partner_auth_utils import AccountLockoutManager

is_locked = AccountLockoutManager.is_locked(user)

if is_locked:
    print(f"Account locked until: {user.locked_until}")
```

#### Get Lockout Info

```python
from usersys.partner_auth_utils import AccountLockoutManager

info = AccountLockoutManager.get_lockout_info(user)

print(f"Is Locked: {info['is_locked']}")
print(f"Failed Attempts: {info['failed_attempts']}")
print(f"Remaining Attempts: {info['remaining_attempts']}")
```

#### Reset Failed Attempts

```python
from usersys.partner_auth_utils import AccountLockoutManager

AccountLockoutManager.reset_failed_attempts(user)
```

### Partner Management

#### Create Partner

```python
from usersys.partner_models import Partner

partner = Partner.objects.create(
    partner_id='ACME001',
    name='Acme Corporation',
    display_name='Acme Corp',
    contact_name='John Smith',
    contact_email='john@acme.com',
    contact_phone='+1-555-0123',
    communication_method='both',  # 'sftp', 'api', 'both', 'manual'
    status='active',
    edi_format='X12',
    sender_id='ACME',
    receiver_id='SYSTEM'
)
```

#### Get Partner Users

```python
from usersys.user_manager import UserManager

users = UserManager.get_partner_users(partner_id='partner-uuid')

for user in users:
    print(f"{user.username} - {user.role} - Active: {user.is_active}")
```

#### Update Partner Status

```python
from usersys.partner_models import Partner

partner = Partner.objects.get(partner_id='ACME001')
partner.status = 'suspended'  # 'active', 'inactive', 'testing', 'suspended'
partner.save()
```

### Permission Management

#### Get User Permissions

```python
from usersys.partner_models import PartnerUser

user = PartnerUser.objects.select_related('permissions').get(id=123)

if hasattr(user, 'permissions'):
    perms = user.permissions.to_dict()
    print(f"Can upload files: {perms['can_upload_files']}")
    print(f"Can download files: {perms['can_download_files']}")
    print(f"Can view transactions: {perms['can_view_transactions']}")
    print(f"Can view reports: {perms['can_view_reports']}")
    print(f"Can manage settings: {perms['can_manage_settings']}")
```

#### Update User Permissions

```python
from usersys.partner_models import PartnerUser

user = PartnerUser.objects.select_related('permissions').get(id=123)

if hasattr(user, 'permissions'):
    user.permissions.can_upload_files = True
    user.permissions.can_download_files = True
    user.permissions.can_manage_settings = False
    user.permissions.save()
```

### Database Queries

#### Get Active Partners

```python
from usersys.partner_models import Partner

active_partners = Partner.objects.filter(status='active')

for partner in active_partners:
    print(f"{partner.partner_id}: {partner.name}")
```

#### Get Recent Transactions for Partner

```python
from usersys.modern_edi_models import EDITransaction

transactions = EDITransaction.objects.filter(
    partner_id='partner-uuid'
).order_by('-created_at')[:10]

for txn in transactions:
    print(f"{txn.filename} - {txn.folder} - {txn.created_at}")
```

#### Get Failed Transactions

```python
from usersys.modern_edi_models import EDITransaction

failed_txns = EDITransaction.objects.filter(
    folder='error'
).order_by('-created_at')

for txn in failed_txns:
    print(f"{txn.partner_name}: {txn.filename} - {txn.created_at}")
```

### Maintenance Operations

#### Clean Up Old Activity Logs

```bash
# Via management command
cd env/default
python manage.py cleanup_activity_logs

# Or via Python
from usersys.activity_logger import ActivityLogger
ActivityLogger.cleanup_old_logs(days=90)
```

#### Clean Up Expired Password Reset Tokens

```python
from usersys.partner_models import PasswordResetToken
from django.utils import timezone

# Delete expired tokens
expired_tokens = PasswordResetToken.objects.filter(
    expires_at__lt=timezone.now()
)
count = expired_tokens.count()
expired_tokens.delete()
print(f"Deleted {count} expired tokens")
```

#### Unlock All Locked Accounts

```python
from usersys.partner_models import PartnerUser
from django.utils import timezone

# Find locked accounts
locked_users = PartnerUser.objects.filter(
    locked_until__gt=timezone.now()
)

# Unlock them
for user in locked_users:
    user.failed_login_attempts = 0
    user.locked_until = None
    user.save()
    print(f"Unlocked: {user.username}")
```

### Debugging

#### Check User Authentication

```python
from usersys.partner_models import PartnerUser
from django.contrib.auth.hashers import check_password

user = PartnerUser.objects.get(username='john_doe')

# Check password
is_correct = check_password('password', user.password_hash)
print(f"Password correct: {is_correct}")

# Check account status
print(f"Is active: {user.is_active}")
print(f"Is locked: {user.is_locked()}")
print(f"Failed attempts: {user.failed_login_attempts}")
```

#### View Session Data

```python
# In a view or shell with request object
session_data = {
    'partner_user_id': request.session.get('partner_user_id'),
    'partner_id': request.session.get('partner_id'),
    'last_activity': request.session.get('last_activity'),
}
print(session_data)
```

#### Test Email Configuration

```python
from django.core.mail import send_mail
from django.conf import settings

try:
    send_mail(
        subject='Test Email',
        message='This is a test email from the EDI system.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['test@example.com'],
        fail_silently=False,
    )
    print("Email sent successfully")
except Exception as e:
    print(f"Email failed: {e}")
```

## Django Shell

Access Django shell for interactive operations:

```bash
cd env/default
python manage.py shell
```

Then import and use any of the above code snippets.

## Common Issues

### Issue: User Cannot Login

**Check:**
1. Is account active? `user.is_active`
2. Is account locked? `user.is_locked()`
3. Is password correct? `check_password(password, user.password_hash)`
4. Is partner active? `user.partner.status == 'active'`

### Issue: Permissions Not Working

**Check:**
1. Does user have permissions object? `hasattr(user, 'permissions')`
2. Are permissions set correctly? `user.permissions.to_dict()`
3. Is middleware configured? Check settings.py MIDDLEWARE

### Issue: Activity Logs Not Recording

**Check:**
1. Is ActivityLogger imported? `from usersys.activity_logger import ActivityLogger`
2. Is logging called in views? Search for `ActivityLogger.log`
3. Check database for logs: `ActivityLog.objects.count()`

### Issue: Emails Not Sending

**Check:**
1. Email settings in .env
2. Test email configuration (see above)
3. Check email service logs
4. Verify DEFAULT_FROM_EMAIL is set

## Performance Tips

1. **Use select_related for foreign keys:**
   ```python
   users = PartnerUser.objects.select_related('partner', 'permissions').all()
   ```

2. **Use prefetch_related for reverse foreign keys:**
   ```python
   partners = Partner.objects.prefetch_related('users').all()
   ```

3. **Add indexes to frequently queried fields** (already done in models)

4. **Use pagination for large result sets:**
   ```python
   from django.core.paginator import Paginator
   
   paginator = Paginator(queryset, 50)  # 50 items per page
   page = paginator.get_page(page_number)
   ```

5. **Cache expensive queries:**
   ```python
   from django.core.cache import cache
   
   metrics = cache.get('dashboard_metrics')
   if not metrics:
       metrics = AnalyticsService.get_dashboard_metrics()
       cache.set('dashboard_metrics', metrics, 60)  # Cache for 60 seconds
   ```

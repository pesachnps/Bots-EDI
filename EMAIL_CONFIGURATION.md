# Email Configuration

## Overview

The application now uses environment variables for email configuration, making it easy to customize email settings without modifying code.

## Configuration

### Environment Variables (.env file)

The email configuration is controlled by these environment variables:

```bash
# SMTP Server Settings
EMAIL_HOST=localhost                    # SMTP server hostname
EMAIL_PORT=25                          # SMTP server port
EMAIL_USE_TLS=False                    # Use TLS encryption
EMAIL_HOST_USER=                       # SMTP username (if required)
EMAIL_HOST_PASSWORD=                   # SMTP password (if required)

# Email Addresses
DEFAULT_FROM_EMAIL=EDI System <pesach.nps@gmail.com>  # All outgoing emails
SERVER_EMAIL=bots@localhost            # Error reports to managers
```

### Current Configuration

Based on your `.env` file:
- **From Email**: `EDI System <pesach.nps@gmail.com>`
- **Server Email**: `bots@localhost` (or from environment)
- **SMTP Host**: `localhost` (or from environment)
- **SMTP Port**: `25` (or from environment)

## Usage

### Manager Email (Error Reports)

Error reports are sent to the email address specified in `DEFAULT_FROM_EMAIL`:

```python
MANAGERS = (
    ('EDI Manager', DEFAULT_FROM_EMAIL),  # Uses pesach.nps@gmail.com
)
```

### Outgoing Emails

All outgoing emails (reports, notifications, password resets) use `DEFAULT_FROM_EMAIL`:

- Scheduled reports
- Password reset emails
- Partner notifications
- Admin notifications

### Email Backend

The email backend automatically switches based on `DEBUG` setting:

- **Development** (`DEBUG=True`): Emails printed to console
- **Production** (`DEBUG=False`): Emails sent via SMTP

## Files Modified

1. **`env/default/config/settings.py`**
   - Updated to read email settings from environment variables
   - Uses `DEFAULT_FROM_EMAIL` for MANAGERS
   - Automatically switches email backend based on DEBUG mode

2. **`.env.example`**
   - Added comments explaining each email setting
   - Clarified the purpose of `DEFAULT_FROM_EMAIL` and `SERVER_EMAIL`

## Testing

### Development (Console Backend)

When `DEBUG=True`, emails are printed to the console:

```bash
# Start backend and watch console for email output
cd env/default
python start_server.py
```

### Production (SMTP Backend)

When `DEBUG=False`, emails are sent via SMTP:

1. Configure SMTP settings in `.env`:
   ```bash
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   DEFAULT_FROM_EMAIL=EDI System <your-email@gmail.com>
   ```

2. Set `DEBUG=False` in `.env`

3. Restart the backend

### Test Email Sending

You can test email configuration with Django shell:

```bash
cd env/default
python manage.py shell
```

```python
from django.core.mail import send_mail

send_mail(
    'Test Email',
    'This is a test email from Bots EDI.',
    None,  # Uses DEFAULT_FROM_EMAIL
    ['recipient@example.com'],
    fail_silently=False,
)
```

## Gmail Configuration

If using Gmail for SMTP:

1. Enable 2-factor authentication on your Google account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Update `.env`:
   ```bash
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=pesach.nps@gmail.com
   EMAIL_HOST_PASSWORD=your-16-char-app-password
   DEFAULT_FROM_EMAIL=EDI System <pesach.nps@gmail.com>
   ```

## Security Notes

1. **Never commit `.env` file** - It contains sensitive credentials
2. **Use App Passwords** - Don't use your actual Gmail password
3. **Restrict permissions** - Only authorized users should access `.env`
4. **Use TLS** - Always enable `EMAIL_USE_TLS=True` for production

## Troubleshooting

### Emails Not Sending

1. Check `DEBUG` setting - if `True`, emails go to console
2. Verify SMTP credentials in `.env`
3. Check firewall/network allows SMTP connections
4. Review Django logs for email errors

### Gmail "Less Secure Apps" Error

Gmail no longer supports "less secure apps". Use App Passwords instead:
1. Enable 2FA on your Google account
2. Generate App Password
3. Use App Password in `EMAIL_HOST_PASSWORD`

### Connection Refused

If you see "Connection refused" errors:
1. Verify `EMAIL_HOST` and `EMAIL_PORT` are correct
2. Check if SMTP server is accessible from your network
3. Try telnet: `telnet smtp.gmail.com 587`

## Related Files

- `.env` - Your local email configuration (not in git)
- `.env.example` - Template with default values
- `env/default/config/settings.py` - Django email settings
- `env/default/usersys/email_service.py` - Email sending service
- `env/default/usersys/report_service.py` - Scheduled report emails

## Summary

✅ Email configuration now uses environment variables
✅ `DEFAULT_FROM_EMAIL` is used for all outgoing emails
✅ Current setting: `EDI System <pesach.nps@gmail.com>`
✅ Easy to change by updating `.env` file
✅ No code changes needed to update email addresses

# Email Setup Guide for Bots EDI

This guide shows you how to configure email notifications for Bots EDI error reports.

## Overview

Bots EDI can send email notifications when errors occur during EDI processing. This guide covers setting up Gmail SMTP for email delivery.

## Prerequisites

- Gmail account (or Google Workspace account)
- 2-Factor Authentication enabled on your Google account
- Access to modify configuration files

## Step 1: Enable 2-Factor Authentication on Gmail

1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Click on **Security** in the left sidebar
3. Under "How you sign in to Google", click **2-Step Verification**
4. Follow the prompts to enable 2-Step Verification
5. You'll need your phone to receive verification codes

## Step 2: Generate Gmail App Password

1. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. You may need to sign in again
3. In the "Select app" dropdown, choose **Mail**
4. In the "Select device" dropdown, choose **Other (Custom name)**
5. Enter a name like "Bots EDI Server"
6. Click **Generate**
7. **IMPORTANT**: Copy the 16-character password that appears - you won't see it again!
   - It will look like: `abcd efgh ijkl mnop` (without spaces when you copy it)

## Step 3: Create Environment File

Create a `.env` file in your project root (`C:\Users\USER\Projects\bots\.env`):

```bash
# Email Configuration
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password-here
EMAIL_RECIPIENT=recipient@example.com

# Optional: Override defaults
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

**Replace:**
- `your-email@gmail.com` - Your Gmail address
- `your-app-password-here` - The 16-character app password (no spaces)
- `recipient@example.com` - Where to send error notifications

## Step 4: Verify Configuration

The configuration has already been set up in:
- `env/default/config/bots.ini` - Line 59: `sendreportiferror = True`
- `env/default/config/settings.py` - Lines 39-56: Gmail SMTP configuration

These files read from environment variables, so you only need to create the `.env` file.

## Step 5: Test Email Configuration

1. Create your `.env` file with the settings above
2. Restart the backend server:
   ```powershell
   .\start_backend.ps1
   ```
3. Log in to http://localhost:8080/admin
4. Navigate to **Home** → **Send Test Email** (if available)
5. Or trigger an error to test automatic email notifications

## Security Best Practices

### DO:
- ✅ Use App Passwords, never your main Gmail password
- ✅ Store credentials in `.env` file (already in `.gitignore`)
- ✅ Use environment variables for sensitive data
- ✅ Revoke App Password if compromised
- ✅ Keep `.env` file permissions restricted

### DON'T:
- ❌ Never commit `.env` file to git
- ❌ Never share your App Password
- ❌ Never use your main Gmail password
- ❌ Never hard-code passwords in configuration files

## Alternative Email Providers

### Microsoft 365 / Outlook.com

```bash
EMAIL_HOST=smtp.office365.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@outlook.com
EMAIL_HOST_PASSWORD=your-password
```

### SendGrid

```bash
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

### Amazon SES

```bash
EMAIL_HOST=email-smtp.us-east-1.amazonaws.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-smtp-username
EMAIL_HOST_PASSWORD=your-smtp-password
```

### Local SMTP Server

```bash
EMAIL_HOST=localhost
EMAIL_PORT=25
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

## Troubleshooting

### Error: "SMTP AUTH extension not supported"

**Cause**: TLS is not enabled

**Solution**: Verify `EMAIL_USE_TLS = True` in settings.py (already configured)

### Error: "Username and Password not accepted"

**Cause**: Using regular password instead of App Password

**Solution**: 
1. Generate a new App Password
2. Update `.env` file with the correct App Password
3. Make sure there are no spaces in the password

### Error: "Connection refused"

**Cause**: 
- Firewall blocking port 587
- Wrong SMTP server

**Solution**:
1. Check firewall settings
2. Verify `EMAIL_HOST=smtp.gmail.com` in `.env`
3. Try port 465 with SSL instead:
   ```bash
   EMAIL_PORT=465
   EMAIL_USE_SSL=True
   EMAIL_USE_TLS=False
   ```

### No Emails Received

**Check:**
1. Spam/Junk folder
2. Email recipient address is correct
3. Backend server logs for errors:
   ```powershell
   Get-Content env\botssys\logging\*.log -Tail 50
   ```

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `EMAIL_HOST_USER` | Yes | - | Your Gmail address |
| `EMAIL_HOST_PASSWORD` | Yes | - | Gmail App Password |
| `EMAIL_RECIPIENT` | Yes | - | Where to send error emails |
| `EMAIL_HOST` | No | `smtp.gmail.com` | SMTP server |
| `EMAIL_PORT` | No | `587` | SMTP port |
| `DEFAULT_FROM_EMAIL` | No | Same as `EMAIL_HOST_USER` | From address |
| `SERVER_EMAIL` | No | Same as `EMAIL_HOST_USER` | Server email |

## Example .env File

```bash
# Complete email configuration example
EMAIL_HOST_USER=bots-edi@gmail.com
EMAIL_HOST_PASSWORD=abcdefghijklmnop
EMAIL_RECIPIENT=admin@company.com

# Optional overrides
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
DEFAULT_FROM_EMAIL=Bots EDI <bots-edi@gmail.com>
SERVER_EMAIL=bots-edi@gmail.com
```

## Revoking Access

If you need to revoke the App Password:

1. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Find "Bots EDI Server" in the list
3. Click **Remove**
4. Generate a new one if needed

## Testing Commands

Test email configuration from Python:

```python
# Test from Python shell
python -c "
from django.core.mail import send_mail
send_mail(
    'Test Email from Bots EDI',
    'This is a test message.',
    'from@example.com',
    ['to@example.com'],
    fail_silently=False,
)
"
```

## Next Steps

After email is configured:
1. Monitor error notifications
2. Set up email filters for Bots EDI messages
3. Configure additional recipients as needed
4. Review security settings regularly

---

**Questions?** Check the main installation guide or troubleshooting section in README.md.

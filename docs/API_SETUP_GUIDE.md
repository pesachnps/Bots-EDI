# Bots EDI REST API - Setup Guide

Complete installation and configuration guide for the Bots EDI REST API system.

## 📋 **Prerequisites**

- Bots EDI installed and running
- Python 3.7 or higher
- Django framework (included with Bots)
- Access to Django admin interface

---

## 🚀 **Installation Steps**

### **Step 1: Verify API Files**

Ensure all API files are in place:

```
C:\Users\USER\.bots\env\default\usersys\
├── api_models.py          ✅ API models
├── api_auth.py            ✅ Authentication
├── api_views.py           ✅ API endpoints
├── api_urls.py            ✅ URL routing
├── api_admin.py           ✅ Admin interface
└── api_management.py      ✅ Management CLI
```

### **Step 2: Update Django Settings**

Add the API app to your Django settings:

**Edit:** `C:\Users\USER\.bots\env\default\config\settings.py`

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bots',
    'usersys',  # Add this line
]
```

### **Step 3: Configure API URLs**

Update the main URL configuration to include API routes.

**Edit:** `C:\Users\USER\.bots\env\default\config\urls.py` (or create if it doesn't exist)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('usersys.api_urls')),  # Add this line
    # ... other Bots URLs
]
```

If Bots uses its own URL configuration, you may need to edit the Bots package URLs or add a custom URL configuration file.

### **Step 4: Run Database Migrations**

Create database tables for API models:

```bash
cd C:\Users\USER\.bots\env\default
python -c "import bots.botsinit; bots.botsinit.generalinit(); import os; os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'; import django; django.setup(); from django.core.management import execute_from_command_line; execute_from_command_line(['manage.py', 'makemigrations', 'usersys'])"

python -c "import bots.botsinit; bots.botsinit.generalinit(); import os; os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'; import django; django.setup(); from django.core.management import execute_from_command_line; execute_from_command_line(['manage.py', 'migrate'])"
```

### **Step 5: Initialize API Permissions**

Create default API permissions:

```bash
cd C:\Users\USER\.bots\env\default
python usersys\api_management.py init_permissions
```

Expected output:
```
✅ Created permission: file_upload
✅ Created permission: file_download
✅ Created permission: file_list
...
✅ Initialized 13 permissions
```

### **Step 6: Create Your First API Key**

```bash
python usersys\api_management.py create "My First API Key" edi_admin file_upload file_download file_list report_view
```

**Save the generated API key!** You won't be able to see it again.

### **Step 7: Test the API**

```bash
# Test API status
curl -H "X-API-Key: YOUR_API_KEY" http://localhost:8080/api/v1/status

# Or use the test script
python test_api.py
```

---

## 🔧 **Configuration**

### **API Settings**

You can customize API behavior by adding these settings to `config/settings.py`:

```python
# API Configuration
API_DEFAULT_RATE_LIMIT = 1000  # Requests per hour
API_KEY_EXPIRY_DAYS = 365  # Days until API key expires
API_AUDIT_LOG_RETENTION_DAYS = 90  # Days to keep audit logs
```

### **Rate Limiting**

Rate limits can be configured per API key:

```bash
# Via Django admin interface
http://localhost:8080/admin/usersys/apikey/

# Or via database
```

### **IP Whitelisting**

Configure IP restrictions for API keys:

1. Log in to Django admin: `http://localhost:8080/admin/`
2. Navigate to **API Keys**
3. Edit the desired API key
4. Add comma-separated IP addresses to **Allowed IPs** field
5. Save

---

## 👤 **User Management**

### **List API Keys**

```bash
python usersys\api_management.py list
```

### **Create API Key with Permissions**

```bash
python usersys\api_management.py create "Production API" edi_admin file_upload file_download route_execute report_view
```

### **List Available Permissions**

```bash
python usersys\api_management.py permissions
```

### **Revoke API Key**

```bash
python usersys\api_management.py revoke YOUR_API_KEY_HERE
```

### **View Audit Logs**

```bash
python usersys\api_management.py audit 100
```

---

## 🛡️ **Security Best Practices**

### **1. Protect API Keys**

- Never commit API keys to version control
- Store API keys in environment variables
- Rotate API keys regularly
- Use different API keys for different environments

### **2. Use IP Whitelisting**

Restrict API keys to specific IP addresses or ranges:

```
192.168.1.100, 10.0.0.0/24
```

### **3. Limit Permissions**

Grant only the permissions required for each API key:

```bash
# Read-only API key
python usersys\api_management.py create "Read-Only" user file_list report_view

# Upload-only API key
python usersys\api_management.py create "Upload-Only" user file_upload
```

### **4. Monitor API Usage**

Regularly review audit logs:

```bash
python usersys\api_management.py audit 500
```

### **5. Set Expiration Dates**

Configure API keys to expire automatically via Django admin interface.

### **6. Use HTTPS**

Always use HTTPS in production. Configure SSL in `config/bots.ini`:

```ini
[webserver]
ssl_certificate = /path/to/cert.pem
ssl_private_key = /path/to/key.pem
```

---

## 🧪 **Testing**

### **Using the Test Script**

```bash
# Set your API key
set BOTS_API_KEY=your-api-key-here

# Run all tests
python test_api.py

# Test specific functionality
python test_api.py status
python test_api.py upload path\to\file.edi
```

### **Manual Testing with cURL**

```bash
# Test authentication
curl -H "X-API-Key: YOUR_API_KEY" http://localhost:8080/api/v1/status

# Upload a file
curl -X POST -H "X-API-Key: YOUR_API_KEY" -F "file=@test.edi" http://localhost:8080/api/v1/files/upload

# List files
curl -H "X-API-Key: YOUR_API_KEY" "http://localhost:8080/api/v1/files/list?type=outfile"

# Get reports
curl -H "X-API-Key: YOUR_API_KEY" "http://localhost:8080/api/v1/reports?limit=10"
```

### **Using Python**

```python
import requests

API_KEY = "your-api-key-here"
headers = {"X-API-Key": API_KEY}

# Test API
response = requests.get("http://localhost:8080/api/v1/status", headers=headers)
print(response.json())
```

---

## 🔍 **Troubleshooting**

### **Issue: API endpoints return 404**

**Solution:** Ensure API URLs are properly configured in Django settings and URL configuration.

```bash
# Verify URL configuration
python -c "import bots.botsinit; bots.botsinit.generalinit(); from django.urls import get_resolver; print(get_resolver().url_patterns)"
```

### **Issue: "No module named 'usersys'"**

**Solution:** Ensure `usersys` is added to `INSTALLED_APPS` in `settings.py`.

### **Issue: Database errors**

**Solution:** Run migrations:

```bash
python -c "import bots.botsinit; bots.botsinit.generalinit(); import os; os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'; import django; django.setup(); from django.core.management import execute_from_command_line; execute_from_command_line(['manage.py', 'migrate'])"
```

### **Issue: "API key required" error**

**Solution:** Ensure API key is provided in `X-API-Key` header:

```bash
curl -H "X-API-Key: YOUR_API_KEY" http://localhost:8080/api/v1/status
```

### **Issue: Permission denied errors**

**Solution:** Verify API key has required permissions:

```bash
python usersys\api_management.py list
```

Grant missing permissions via Django admin interface.

---

## 📊 **Monitoring**

### **Check API Usage**

```bash
# View recent API activity
python usersys\api_management.py audit 100

# Check specific API key usage
# Via Django admin: http://localhost:8080/admin/usersys/apikey/
```

### **Monitor Rate Limits**

API status endpoint shows current usage:

```bash
curl -H "X-API-Key: YOUR_API_KEY" http://localhost:8080/api/v1/status
```

### **Audit Logs**

All API requests are logged in the database with:
- API key used
- Endpoint accessed
- Request parameters
- Response status
- Duration
- IP address
- Timestamp

Access via Django admin:
```
http://localhost:8080/admin/usersys/apiauditlog/
```

---

## 📚 **Additional Resources**

- **API Documentation:** `API_DOCUMENTATION.md`
- **Test Script:** `test_api.py`
- **Management CLI:** `usersys\api_management.py`
- **Bots EDI Docs:** https://bots.sourceforge.io/
- **Django Admin:** http://localhost:8080/admin/

---

## ✅ **Quick Start Checklist**

- [ ] All API files in place
- [ ] Django settings updated
- [ ] URL configuration updated
- [ ] Database migrations run
- [ ] API permissions initialized
- [ ] First API key created
- [ ] API tested successfully
- [ ] Django admin accessible
- [ ] API documentation reviewed
- [ ] Security best practices implemented

---

## 🎉 **Next Steps**

1. Create API keys for your applications
2. Integrate API into your workflows
3. Set up monitoring and alerts
4. Configure IP whitelisting for production
5. Enable HTTPS for secure communication
6. Review and customize permissions
7. Set up automated backups of API keys
8. Document your API integration

---

**Congratulations! Your Bots EDI REST API is now fully configured and ready to use!**

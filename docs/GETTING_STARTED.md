# Getting Started with Bots EDI Environment

Welcome! This guide will help you get up and running quickly.

## Prerequisites

Before you begin, ensure you have:

- [ ] Python 3.8 or higher installed
- [ ] Git installed (for cloning the repository)
- [ ] Basic understanding of EDI concepts
- [ ] Command line/terminal access

## Installation Methods

Choose the method that works best for you:

### Method 1: Automated Quick Start (Recommended)

**Linux/macOS:**
```bash
chmod +x scripts/quickstart.sh
./scripts/quickstart.sh
```

**Windows:**
```cmd
scripts\quickstart.bat
```

This will automatically:
- Create a virtual environment
- Install all dependencies
- Generate a secure secret key
- Initialize the database
- Create a default admin user

### Method 2: Manual Installation

If you prefer manual control:

```bash
# 1. Clone the repository
git clone <repository-url>
cd bots-edi-environment

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your settings

# 5. Initialize database tables
python create_missing_tables.py

# 6. Create admin users
python create_admin.py

# 7. Add bots-engine to PATH (Windows only)
# Replace YOUR_USERNAME with your actual Windows username
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Users\YOUR_USERNAME\AppData\Roaming\Python\Python313\Scripts", "User")
```

## First Steps After Installation

### 1. Start the Web Server

```bash
cd env/default
bots-webserver
```

The server will start on http://localhost:8080

### 2. Access the Web Interface

Open your browser and navigate to:
- **Main Interface:** http://localhost:8080
- **Admin Interface:** http://localhost:8080/admin

**Default Login:**
- Username: `admin`
- Password: `admin123` (or the password you set)

⚠️ **IMPORTANT:** Change the default password immediately!

### 3. Create Your First API Key

```bash
cd env/default

# Initialize API permissions (first time only)
python usersys/api_management.py init_permissions

# Create an API key
python usersys/api_management.py create "My First API Key" admin file_upload file_download
```

Save the generated API key securely - you'll need it for API requests.

### 4. Test the API

```bash
# Test API status
curl http://localhost:8080/api/v1/status \
  -H "X-API-Key: your-api-key-here"
```

You should receive a JSON response with your API key details.

## Next Steps

### Learn the Basics

1. **Read the Documentation**
   - [README.md](README.md) - Overview and quick start
   - [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Complete API reference
   - [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Command cheat sheet

2. **Explore the Web Interface**
   - Navigate through the admin interface
   - View the configuration options
   - Check the reports section

3. **Try the API**
   - Upload a test file
   - List available files
   - Execute a route
   - View reports

### Configure Your Environment

1. **Review Configuration Files**
   - `env/default/config/settings.py` - Django settings
   - `env/default/config/bots.ini` - Bots configuration
   - `.env` - Environment variables

2. **Set Up Your First Route**
   - Define input/output formats
   - Create mapping scripts
   - Configure partners
   - Test the translation

3. **Configure Security**
   - Change default passwords
   - Set up API key permissions
   - Configure IP whitelisting (optional)
   - Review security settings

### Development Workflow

1. **Create EDI Grammars**
   - Location: `env/default/usersys/grammars/`
   - Define message structures
   - Test with sample files

2. **Create Mapping Scripts**
   - Location: `env/default/usersys/mappings/`
   - Transform data between formats
   - Handle business logic

3. **Configure Routes**
   - Define translation workflows
   - Set up channels
   - Configure partners

4. **Test Your Setup**
   - Place test files in `infile/`
   - Run the engine
   - Check `outfile/` for results
   - Review logs for errors

## Common Tasks

### Upload a File via API

```bash
curl -X POST http://localhost:8080/api/v1/files/upload \
  -H "X-API-Key: your-api-key" \
  -F "file=@test.edi" \
  -F "route=myroute"
```

### Execute a Route

```bash
curl -X POST http://localhost:8080/api/v1/routes/execute \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"route": "myroute"}'
```

### View Reports

```bash
curl http://localhost:8080/api/v1/reports?limit=10 \
  -H "X-API-Key: your-api-key"
```

### Create a New User

```bash
cd env/default
python manage_users.py create newuser SecurePassword123!
```

### Create an API Key for a User

```bash
cd env/default
python usersys/api_management.py create "Production API" newuser file_upload file_download
```

## Troubleshooting

### Server Won't Start

**Check if port is in use:**
```bash
# Linux/macOS
lsof -i :8080

# Windows
netstat -ano | findstr :8080
```

**Solution:** Change port in `env/default/config/bots.ini`:
```ini
[webserver]
port = 8081
```

### Can't Login to Web Interface

**Reset admin password:**
```bash
cd env/default
python manage_users.py reset admin NewPassword123!
```

### API Key Not Working

**Check API key status:**
```bash
cd env/default
python usersys/api_management.py list
```

**Create new API key if needed:**
```bash
python usersys/api_management.py create "New Key" admin
```

### Database Errors

**Reinitialize database:**
```bash
# Backup first!
cp env/default/botssys/sqlitedb/botsdb env/default/botssys/sqlitedb/botsdb.backup

# Reinitialize
python scripts/init_database.py
```

## Learning Resources

### Documentation
- **README.md** - Project overview and quick start
- **API_DOCUMENTATION.md** - Complete API reference
- **SECURITY.md** - Security best practices
- **DEPLOYMENT.md** - Production deployment guide
- **QUICK_REFERENCE.md** - Command cheat sheet

### External Resources
- [Django Documentation](https://docs.djangoproject.com/)
- [EDI Basics](https://www.edibasics.com/)

## Getting Help

### Check the Documentation
Most questions are answered in:
- README.md
- API_DOCUMENTATION.md
- QUICK_REFERENCE.md

### Review Logs
```bash
# Webserver logs
tail -f env/default/botssys/logging/webserver*.log

# Engine logs
tail -f env/default/botssys/logging/engine*.log
```

### Common Issues
See the Troubleshooting section in README.md

### Report Issues
- Check existing issues on GitHub
- Create a new issue with:
  - Clear description
  - Steps to reproduce
  - Error messages
  - Environment details

## Best Practices

### Security
- [ ] Change default passwords immediately
- [ ] Use strong passwords (12+ characters)
- [ ] Keep API keys secure
- [ ] Use HTTPS in production
- [ ] Regularly review audit logs
- [ ] Keep software updated

### Development
- [ ] Test in development environment first
- [ ] Use version control for custom scripts
- [ ] Document your mappings and routes
- [ ] Keep backups of configuration
- [ ] Monitor logs regularly

### Production
- [ ] Use PostgreSQL or MySQL (not SQLite)
- [ ] Set DEBUG=False
- [ ] Configure proper logging
- [ ] Set up automated backups
- [ ] Monitor system resources
- [ ] Plan for scaling

## Quick Checklist

After installation, verify:

- [ ] Web interface accessible at http://localhost:8080
- [ ] Can login with admin credentials
- [ ] API status endpoint responds
- [ ] Can create API keys
- [ ] Can upload files via API
- [ ] Logs are being written
- [ ] Database is accessible

## What's Next?

Now that you're set up, you can:

1. **Configure Your First EDI Translation**
   - Create grammars for your EDI formats
   - Write mapping scripts
   - Set up routes
   - Test with sample files

2. **Integrate with Your Systems**
   - Use the REST API
   - Set up automated file transfers
   - Configure webhooks (if needed)
   - Monitor translations

3. **Prepare for Production**
   - Review DEPLOYMENT.md
   - Follow SECURITY.md guidelines
   - Set up monitoring
   - Configure backups

4. **Customize and Extend**
   - Add custom scripts
   - Create new API endpoints
   - Integrate with other systems
   - Contribute improvements

## Support

- **Documentation:** See the docs/ folder
- **Issues:** GitHub Issues
- **Community:** Bots EDI forums
- **Commercial Support:** Contact your vendor

---

**Welcome to Bots EDI!** 🚀

You're now ready to start translating EDI messages. If you have questions, check the documentation or reach out for help.

**Version:** 1.0.0  
**Last Updated:** 2025-11-05

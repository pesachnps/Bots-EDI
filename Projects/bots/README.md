# Bots EDI Environment

A Django-based Electronic Data Interchange (EDI) translation system with REST API support. This repository contains the environment configuration for the Bots EDI framework.

## Features

- **Multi-format EDI Support**: EDIFACT, X12, TRADACOMS, XML, JSON, CSV, and more
- **REST API**: Token-based authentication with rate limiting and permissions
- **Web Interface**: Django admin for configuration and monitoring
- **Flexible Routing**: Configurable translation routes and mappings
- **Audit Logging**: Complete API request tracking
- **Directory Monitoring**: Automatic file processing on detection

## Quick Start

### Prerequisites

- Python 3.8+
- Bots EDI framework installed
- SQLite (default) or PostgreSQL/MySQL

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
```

4. Initialize the database:
```bash
cd env/default
python manage_users.py list
```

5. Create a superuser:
```bash
python manage_users.py create admin YourSecurePassword123!
```

6. Start the Bots webserver:
```bash
bots-webserver
```

Access the web interface at `http://localhost:8080`

## API Usage

### Authentication

All API requests require an API key in the `X-API-Key` header.

### Create an API Key

```bash
cd env/default
python usersys/api_management.py init_permissions
python usersys/api_management.py create "My API Key" admin file_upload file_download
```

### Example API Requests

**Upload a file:**
```bash
curl -X POST http://localhost:8080/api/v1/files/upload \
  -H "X-API-Key: your-api-key" \
  -F "file=@invoice.edi" \
  -F "route=myroute"
```

**List files:**
```bash
curl http://localhost:8080/api/v1/files/list?type=outfile \
  -H "X-API-Key: your-api-key"
```

**Execute a route:**
```bash
curl -X POST http://localhost:8080/api/v1/routes/execute \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"route": "myroute"}'
```

**View reports:**
```bash
curl http://localhost:8080/api/v1/reports?limit=50 \
  -H "X-API-Key: your-api-key"
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
BOTSENV=production
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_ENGINE=sqlite3
TIME_ZONE=UTC
```

### Directory Structure

```
env/default/
├── config/
│   ├── settings.py      # Django settings
│   └── bots.ini         # Bots engine configuration
├── botssys/             # System files (database, logs, archive)
│   ├── data/
│   ├── infile/          # Incoming EDI files
│   ├── logging/
│   ├── sqlitedb/
│   └── static/
└── usersys/             # User customizations
    ├── grammars/        # EDI format definitions
    ├── mappings/        # Translation mappings
    ├── partners/        # Trading partner configs
    ├── routescripts/    # Custom route logic
    └── api_*.py         # REST API implementation
```

## API Permissions

Available permissions:
- `file_upload` - Upload EDI files
- `file_download` - Download processed files
- `file_list` - List available files
- `route_execute` - Execute translation routes
- `report_view` - View translation reports
- `admin_access` - Full administrative access

## Management Commands

### User Management
```bash
python manage_users.py list                    # List all users
python manage_users.py create <user> <pass>    # Create superuser
python manage_users.py reset <user> <pass>     # Reset password
```

### API Management
```bash
python usersys/api_management.py list                  # List API keys
python usersys/api_management.py create <name> <user>  # Create API key
python usersys/api_management.py permissions           # List permissions
python usersys/api_management.py revoke <key>          # Revoke API key
python usersys/api_management.py audit [limit]         # View audit logs
```

## Security

### Important Security Notes

1. **Change default passwords** immediately after installation
2. **Set a unique SECRET_KEY** in your environment variables
3. **Use HTTPS** in production environments
4. **Restrict API key IP addresses** when possible
5. **Regularly rotate API keys**
6. **Monitor audit logs** for suspicious activity

### Production Checklist

- [ ] Set `DEBUG=False` in settings
- [ ] Configure unique `SECRET_KEY`
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure email settings for error reports
- [ ] Set appropriate `ALLOWED_HOSTS`
- [ ] Configure production database (PostgreSQL/MySQL)
- [ ] Set up regular database backups
- [ ] Configure log rotation
- [ ] Review and restrict API permissions
- [ ] Set up monitoring and alerting

## Database Options

### SQLite (Default)
No additional configuration needed. Database stored in `botssys/sqlitedb/`.

### PostgreSQL
Edit `config/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'botsdb',
        'USER': 'bots',
        'PASSWORD': 'your-password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

### MySQL
Edit `config/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'botsdb',
        'USER': 'bots',
        'PASSWORD': 'your-password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8'},
    }
}
```

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Change port in config/bots.ini
[webserver]
port = 8081
```

**Database locked:**
```bash
# Stop all Bots processes
pkill -f bots-engine
pkill -f bots-webserver
```

**API key not working:**
```bash
# Check API key status
python usersys/api_management.py list
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Support

- Documentation: [Bots EDI Documentation](https://bots.readthedocs.io/)
- Issues: Use GitHub Issues for bug reports
- Community: Bots EDI user forums

## License

See LICENSE file for details.

## Acknowledgments

Built on the Bots EDI framework - an open-source EDI translation system.

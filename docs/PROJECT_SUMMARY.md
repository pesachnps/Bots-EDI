# Bots EDI Environment - Project Summary

## Overview

This repository contains a production-ready Bots EDI (Electronic Data Interchange) environment with a comprehensive REST API layer. The system enables automated translation between various EDI formats including EDIFACT, X12, TRADACOMS, XML, JSON, and CSV.

## Key Features

### Core Functionality
- **Multi-format EDI Support**: EDIFACT, X12, TRADACOMS, XML, JSON, CSV, Fixed-length
- **Translation Engine**: Automated message translation between formats
- **Web Interface**: Django-based admin interface for configuration
- **Directory Monitoring**: Automatic file processing on detection
- **Flexible Routing**: Configurable translation routes and mappings

### REST API
- **Token Authentication**: Secure API key-based authentication
- **Rate Limiting**: Configurable per-key request limits
- **Granular Permissions**: 13 different permission types
- **IP Whitelisting**: Restrict access by IP address
- **Audit Logging**: Complete request tracking
- **File Operations**: Upload, download, and list files
- **Route Execution**: Trigger translations via API
- **Report Access**: Query translation results

### Security
- Environment-based configuration
- Secret key management
- HTTPS/SSL support
- CSRF protection
- SQL injection prevention
- XSS protection
- Rate limiting
- IP restrictions
- Comprehensive audit trails

## Project Structure

```
.
├── README.md                    # Main documentation
├── API_DOCUMENTATION.md         # Complete API reference
├── SECURITY.md                  # Security guidelines
├── CONTRIBUTING.md              # Contribution guide
├── CHANGELOG.md                 # Version history
├── LICENSE                      # MIT License
├── requirements.txt             # Python dependencies
├── setup.py                     # Package configuration
├── pytest.ini                   # Test configuration
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
│
├── env/default/                 # Bots environment
│   ├── config/
│   │   ├── settings.py          # Django settings (enhanced)
│   │   └── bots.ini             # Bots configuration
│   │
│   ├── botssys/                 # System files
│   │   ├── data/                # Runtime data
│   │   ├── infile/              # Incoming files
│   │   ├── outfile/             # Processed files
│   │   ├── logging/             # Log files
│   │   ├── sqlitedb/            # Database
│   │   └── static/              # Static assets
│   │
│   ├── usersys/                 # User customizations
│   │   ├── api_models.py        # API data models
│   │   ├── api_views.py         # API endpoints
│   │   ├── api_urls.py          # API routing
│   │   ├── api_auth.py          # Authentication
│   │   ├── api_admin.py         # Admin interface
│   │   ├── api_management.py    # CLI management
│   │   ├── migrations/          # Database migrations
│   │   ├── grammars/            # EDI format definitions
│   │   ├── mappings/            # Translation mappings
│   │   ├── partners/            # Trading partners
│   │   ├── routescripts/        # Route logic
│   │   ├── communicationscripts/# File handling
│   │   └── envelopescripts/     # Format envelopes
│   │
│   └── manage_users.py          # User management CLI
│
├── scripts/
│   ├── quickstart.sh            # Linux setup script
│   ├── quickstart.bat           # Windows setup script
│   ├── backup.sh                # Linux backup script
│   ├── backup.bat               # Windows backup script
│   └── init_database.py         # Database initialization
│
└── tests/
    ├── __init__.py
    ├── test_api_auth.py         # Authentication tests
    └── test_api_views.py        # API endpoint tests
```

## Technology Stack

### Backend
- **Python 3.8+**: Core language
- **Django 3.2+**: Web framework
- **Bots EDI 4.0+**: EDI translation engine
- **CherryPy**: Web server

### Database
- **SQLite**: Default (development)
- **PostgreSQL**: Production option
- **MySQL**: Production option

### Testing
- **pytest**: Test framework
- **pytest-django**: Django integration

### Development Tools
- **black**: Code formatting
- **flake8**: Linting

## Quick Start

### Linux/macOS
```bash
chmod +x scripts/quickstart.sh
./scripts/quickstart.sh
```

### Windows
```cmd
scripts\quickstart.bat
```

### Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Initialize database
python scripts/init_database.py

# Start webserver
cd env/default
bots-webserver
```

## API Endpoints

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| POST | `/api/v1/files/upload` | Upload EDI file | `file_upload` |
| GET | `/api/v1/files/download/<id>` | Download file | `file_download` |
| GET | `/api/v1/files/list` | List files | `file_list` |
| POST | `/api/v1/routes/execute` | Execute route | `route_execute` |
| GET | `/api/v1/reports` | View reports | `report_view` |
| GET | `/api/v1/status` | API status | None |

## Management Commands

### User Management
```bash
python manage_users.py list                    # List users
python manage_users.py create <user> <pass>    # Create user
python manage_users.py reset <user> <pass>     # Reset password
```

### API Management
```bash
python usersys/api_management.py list                  # List API keys
python usersys/api_management.py create <name> <user>  # Create key
python usersys/api_management.py permissions           # List permissions
python usersys/api_management.py revoke <key>          # Revoke key
python usersys/api_management.py audit [limit]         # View logs
```

## Configuration

### Environment Variables
- `DJANGO_SECRET_KEY`: Django secret key (required in production)
- `DEBUG`: Debug mode (False in production)
- `DATABASE_ENGINE`: Database type (sqlite3, postgresql, mysql)
- `TIME_ZONE`: System timezone
- `ALLOWED_HOSTS`: Comma-separated allowed hosts

### Database Configuration
Edit `env/default/config/settings.py` or use environment variables.

### Bots Configuration
Edit `env/default/config/bots.ini` for Bots-specific settings.

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=usersys --cov-report=html

# Run specific tests
pytest tests/test_api_auth.py
```

## Deployment

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure unique `SECRET_KEY`
- [ ] Set up HTTPS/SSL
- [ ] Configure production database
- [ ] Set `ALLOWED_HOSTS`
- [ ] Change default passwords
- [ ] Configure email settings
- [ ] Set up backups
- [ ] Configure log rotation
- [ ] Review security settings

### Backup
```bash
# Linux
./scripts/backup.sh

# Windows
scripts\backup.bat
```

## Documentation

- **README.md**: Getting started guide
- **API_DOCUMENTATION.md**: Complete API reference with examples
- **SECURITY.md**: Security best practices and policies
- **CONTRIBUTING.md**: Contribution guidelines
- **CHANGELOG.md**: Version history and changes

## Support

- **Issues**: GitHub Issues
- **Documentation**: Project wiki
- **Bots EDI**: https://bots.readthedocs.io/

## License

MIT License - See LICENSE file for details

## Improvements Made

This project includes the following enhancements over a basic Bots EDI setup:

### Documentation
✅ Comprehensive README with quick start guide
✅ Complete API documentation with examples
✅ Security policy and best practices
✅ Contribution guidelines
✅ Changelog for version tracking

### Configuration
✅ Environment variable support
✅ Flexible database configuration
✅ Example environment file
✅ Improved settings.py with env vars

### Security
✅ Environment-based secret key
✅ Configurable debug mode
✅ Allowed hosts configuration
✅ API authentication and authorization
✅ Rate limiting
✅ IP whitelisting
✅ Audit logging

### Testing
✅ Unit tests for authentication
✅ Integration tests for API views
✅ pytest configuration
✅ Test fixtures and utilities

### Tooling
✅ User management CLI
✅ API key management CLI
✅ Database initialization script
✅ Backup scripts (Linux & Windows)
✅ Quick start scripts (Linux & Windows)

### Development
✅ requirements.txt for dependencies
✅ setup.py for package installation
✅ .gitignore for version control
✅ Migration files for API models
✅ Proper project structure

### API Features
✅ RESTful API design
✅ Token-based authentication
✅ Granular permissions
✅ Rate limiting
✅ Audit logging
✅ File operations
✅ Route execution
✅ Report access

## Future Enhancements

Potential improvements for future versions:

- Docker containerization
- Kubernetes deployment manifests
- OpenAPI/Swagger specification
- CI/CD pipeline configuration
- Webhook support
- WebSocket for real-time updates
- API usage analytics dashboard
- Batch file operations
- Asynchronous processing
- Enhanced monitoring and alerting

## Contributors

Initial development and improvements by the project team.

## Acknowledgments

Built on the Bots EDI framework - an open-source EDI translation system.

---

**Version**: 1.0.0  
**Last Updated**: 2025-11-05  
**Status**: Production Ready

# Technology Stack

## Core Technologies

- **Python 3.8+**: Primary language
- **Django 3.2+**: Web framework and admin interface
- **Bots EDI 4.0+**: EDI translation engine
- **CherryPy**: Web server

## Database Support

- **SQLite**: Default for development (stored in `env/default/botssys/sqlitedb/`)
- **PostgreSQL**: Recommended for production
- **MySQL**: Alternative production option

## Testing

- **pytest**: Test framework
- **pytest-django**: Django integration for tests

## Common Commands

### Setup and Initialization
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database and create admin user
python scripts/init_database.py

# Manual user management
cd env/default
python manage_users.py create <username> <password>
python manage_users.py list
python manage_users.py reset <username> <password>
```

### API Key Management
```bash
cd env/default
python usersys/api_management.py init_permissions
python usersys/api_management.py create "<name>" <username> [permissions...]
python usersys/api_management.py list
python usersys/api_management.py revoke <key>
python usersys/api_management.py audit [limit]
```

### Running the Application
```bash
# Start Bots webserver (from env/default directory)
bots-webserver

# Access web interface at http://localhost:8080
# Access admin at http://localhost:8080/admin
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=usersys --cov-report=html

# Run specific test file
pytest tests/test_api_auth.py
```

### Development Tools
```bash
# Format code
black env/default/usersys/*.py

# Lint code
flake8 env/default/usersys/ --max-line-length=100
```

## Configuration Files

- `env/default/config/settings.py`: Django settings (database, security, middleware)
- `env/default/config/bots.ini`: Bots engine configuration (ports, directories)
- `.env`: Environment variables (SECRET_KEY, DEBUG, DATABASE_ENGINE)
- `requirements.txt`: Python dependencies

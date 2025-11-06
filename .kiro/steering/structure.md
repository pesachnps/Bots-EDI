# Project Structure

## Directory Organization

```
.
├── env/default/              # Bots environment (main application)
│   ├── config/               # Configuration files
│   │   ├── settings.py       # Django settings
│   │   └── bots.ini          # Bots engine config
│   ├── botssys/              # System runtime files (not in git)
│   │   ├── data/             # Runtime data
│   │   ├── infile/           # Incoming EDI files
│   │   ├── outfile/          # Processed output files
│   │   ├── logging/          # Log files
│   │   ├── sqlitedb/         # SQLite database
│   │   └── static/           # Static assets
│   ├── usersys/              # User customizations and API
│   │   ├── api_*.py          # REST API implementation
│   │   ├── migrations/       # Django database migrations
│   │   ├── grammars/         # EDI format definitions
│   │   ├── mappings/         # Translation mapping scripts
│   │   ├── partners/         # Trading partner configurations
│   │   ├── routescripts/     # Custom route logic
│   │   ├── communicationscripts/  # File handling scripts
│   │   └── envelopescripts/  # Format envelope handlers
│   └── manage_users.py       # User management CLI
├── scripts/                  # Automation and setup scripts
├── tests/                    # Test suite
└── *.md                      # Documentation files
```

## Key File Locations

### API Implementation
- `env/default/usersys/api_models.py`: Django models (APIKey, APIPermission, APIAuditLog)
- `env/default/usersys/api_views.py`: REST API endpoints
- `env/default/usersys/api_urls.py`: API URL routing
- `env/default/usersys/api_auth.py`: Authentication and authorization
- `env/default/usersys/api_admin.py`: Django admin interface
- `env/default/usersys/api_management.py`: CLI management tool

### EDI Configuration
- `env/default/usersys/grammars/`: EDI format definitions (EDIFACT, X12, etc.)
- `env/default/usersys/mappings/`: Python scripts for format translation
- `env/default/usersys/partners/`: Trading partner configurations
- `env/default/usersys/routescripts/`: Custom routing logic

### Management Scripts
- `scripts/init_database.py`: Database initialization
- `scripts/quickstart.sh` / `quickstart.bat`: Quick setup scripts
- `scripts/backup.sh` / `backup.bat`: Backup scripts
- `env/default/manage_users.py`: User management

### Tests
- `tests/test_api_auth.py`: Authentication tests
- `tests/test_api_views.py`: API endpoint tests

## Architecture Patterns

### Django App Structure
The API is implemented as Django models and views integrated into the Bots environment. All API code lives in `env/default/usersys/` with the `api_` prefix.

### Database Models
- **APIKey**: Token-based authentication with rate limiting and IP restrictions
- **APIPermission**: Granular permission system (13 permission types)
- **APIAuditLog**: Complete request tracking for compliance

### URL Routing
API endpoints follow REST conventions under `/api/v1/`:
- `/api/v1/files/*`: File operations
- `/api/v1/routes/*`: Route execution
- `/api/v1/reports`: Translation reports
- `/api/v1/status`: Health check

### Authentication Flow
1. Client sends request with `X-API-Key` header
2. `api_auth.py` validates key, checks rate limits, IP restrictions
3. Permission check against required permission for endpoint
4. Request logged to APIAuditLog
5. Response returned

## Working Directory Context

Most Bots commands must be run from `env/default/` directory as they expect to find `config/settings.py` and `config/bots.ini` in the current directory.

# Quick Reference Card

## Quick Start

```bash
# Linux/macOS
./scripts/quickstart.sh

# Windows
scripts\quickstart.bat
```

## Common Commands

### User Management
```bash
cd env/default

# List users
python manage_users.py list

# Create user
python manage_users.py create <username> <password>

# Reset password
python manage_users.py reset <username> <new_password>
```

### API Key Management
```bash
cd env/default

# List API keys
python usersys/api_management.py list

# Create API key
python usersys/api_management.py create "Key Name" <username>

# List permissions
python usersys/api_management.py permissions

# Initialize permissions
python usersys/api_management.py init_permissions

# Revoke API key
python usersys/api_management.py revoke <api_key>

# View audit logs
python usersys/api_management.py audit 100
```

### Service Management
```bash
# Start webserver
cd env/default
bots-webserver

# With systemd
sudo systemctl start bots-webserver
sudo systemctl stop bots-webserver
sudo systemctl restart bots-webserver
sudo systemctl status bots-webserver

# View logs
sudo journalctl -u bots-webserver -f
```

### Backup & Restore
```bash
# Backup (Linux)
./scripts/backup.sh

# Backup (Windows)
scripts\backup.bat

# Restore
tar -xzf backups/bots_backup_YYYYMMDD.tar.gz
```

## API Endpoints

### Authentication
All requests require `X-API-Key` header:
```bash
curl -H "X-API-Key: your-api-key" http://localhost:8080/api/v1/status
```

### File Upload
```bash
curl -X POST http://localhost:8080/api/v1/files/upload \
  -H "X-API-Key: your-api-key" \
  -F "file=@invoice.edi" \
  -F "route=myroute"
```

### File Download
```bash
curl http://localhost:8080/api/v1/files/download/path/to/file.xml \
  -H "X-API-Key: your-api-key" \
  -o output.xml
```

### List Files
```bash
curl "http://localhost:8080/api/v1/files/list?type=outfile" \
  -H "X-API-Key: your-api-key"
```

### Execute Route
```bash
curl -X POST http://localhost:8080/api/v1/routes/execute \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"route": "myroute"}'
```

### View Reports
```bash
curl "http://localhost:8080/api/v1/reports?limit=50" \
  -H "X-API-Key: your-api-key"
```

### Check Status
```bash
curl http://localhost:8080/api/v1/status \
  -H "X-API-Key: your-api-key"
```

## Configuration Files

### Environment Variables (.env)
```env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_ENGINE=postgresql_psycopg2
DATABASE_NAME=botsdb
DATABASE_USER=botsuser
DATABASE_PASSWORD=your-password
TIME_ZONE=UTC
ALLOWED_HOSTS=yourdomain.com
```

### Key Locations
- **Config:** `env/default/config/`
- **User Scripts:** `env/default/usersys/`
- **Database:** `env/default/botssys/sqlitedb/`
- **Logs:** `env/default/botssys/logging/`
- **Incoming Files:** `env/default/botssys/infile/`
- **Outgoing Files:** `env/default/botssys/outfile/`

## Troubleshooting

### Check Logs
```bash
# Webserver logs
tail -f env/default/botssys/logging/webserver*.log

# Engine logs
tail -f env/default/botssys/logging/engine*.log

# System logs (with systemd)
sudo journalctl -u bots-webserver -n 100
```

### Test Database Connection
```bash
cd env/default
python -c "import django; django.setup(); from django.db import connection; connection.ensure_connection(); print('OK')"
```

### Check Service Status
```bash
sudo systemctl status bots-webserver
```

### Restart Service
```bash
sudo systemctl restart bots-webserver
```

### Check Port Usage
```bash
# Linux
sudo netstat -tlnp | grep 8080

# Windows
netstat -ano | findstr :8080
```

## Database Operations

### SQLite (Default)
```bash
# Backup
cp env/default/botssys/sqlitedb/botsdb env/default/botssys/sqlitedb/botsdb.backup

# Restore
cp env/default/botssys/sqlitedb/botsdb.backup env/default/botssys/sqlitedb/botsdb
```

### PostgreSQL
```bash
# Backup
pg_dump -U botsuser botsdb > backup.sql

# Restore
psql -U botsuser botsdb < backup.sql

# Connect
psql -U botsuser -d botsdb
```

### MySQL
```bash
# Backup
mysqldump -u botsuser -p botsdb > backup.sql

# Restore
mysql -u botsuser -p botsdb < backup.sql

# Connect
mysql -u botsuser -p botsdb
```

## Testing

### Run Tests
```bash
# All tests
pytest

# Specific test file
pytest tests/test_api_auth.py

# With coverage
pytest --cov=usersys --cov-report=html

# Verbose
pytest -v
```

## Security Checklist

- [ ] Change default passwords
- [ ] Set unique SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall
- [ ] Set up backups
- [ ] Review API permissions
- [ ] Configure IP whitelisting
- [ ] Monitor audit logs

## Performance Tips

1. **Use PostgreSQL** in production (not SQLite)
2. **Enable caching** for static files
3. **Configure rate limits** appropriately
4. **Monitor disk space** regularly
5. **Rotate logs** to prevent disk fill
6. **Index database** tables as needed
7. **Use CDN** for static assets
8. **Scale horizontally** with load balancer

## Common Issues

### Port Already in Use
```bash
# Find process
sudo lsof -i :8080  # Linux
netstat -ano | findstr :8080  # Windows

# Kill process
sudo kill -9 <PID>  # Linux
taskkill /PID <PID> /F  # Windows
```

### Database Locked
```bash
# Stop all Bots processes
pkill -f bots-engine
pkill -f bots-webserver
sudo systemctl stop bots-webserver
```

### Permission Denied
```bash
# Fix ownership
sudo chown -R botsedi:botsedi /home/botsedi/bots-edi

# Fix permissions
chmod +x scripts/*.sh
```

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | (random) | Django secret key |
| `DEBUG` | False | Debug mode |
| `DATABASE_ENGINE` | sqlite3 | Database type |
| `DATABASE_NAME` | botsdb | Database name |
| `DATABASE_USER` | bots | Database user |
| `DATABASE_PASSWORD` | - | Database password |
| `DATABASE_HOST` | localhost | Database host |
| `DATABASE_PORT` | 5432/3306 | Database port |
| `TIME_ZONE` | UTC | System timezone |
| `ALLOWED_HOSTS` | * | Allowed hosts |
| `BOTSENV` | default | Environment name |

## API Permissions

| Code | Description |
|------|-------------|
| `file_upload` | Upload files |
| `file_download` | Download files |
| `file_list` | List files |
| `file_delete` | Delete files |
| `route_execute` | Execute routes |
| `route_list` | List routes |
| `report_view` | View reports |
| `report_download` | Download reports |
| `partner_view` | View partners |
| `partner_manage` | Manage partners |
| `translate_view` | View translations |
| `channel_view` | View channels |
| `admin_access` | Full admin access |

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 429 | Rate Limited |
| 500 | Server Error |
| 504 | Timeout |

## Support Resources

- **Documentation:** README.md, API_DOCUMENTATION.md
- **Security:** SECURITY.md
- **Deployment:** DEPLOYMENT.md
- **Contributing:** CONTRIBUTING.md
- **Issues:** GitHub Issues

## Quick Links

- Web Interface: http://localhost:8080
- Admin Interface: http://localhost:8080/admin
- API Base URL: http://localhost:8080/api/v1

---

**Version:** 1.0.0  
**Last Updated:** 2025-11-05

For detailed information, see the full documentation files.

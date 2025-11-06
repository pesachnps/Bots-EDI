# Deployment Guide

This guide covers deploying the Bots EDI Environment to production.

## Pre-Deployment Checklist

### Security
- [ ] Generate unique `DJANGO_SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS` with your domain(s)
- [ ] Set up HTTPS/SSL certificates
- [ ] Change all default passwords
- [ ] Review and restrict API permissions
- [ ] Configure IP whitelisting for API keys
- [ ] Set up firewall rules

### Database
- [ ] Choose production database (PostgreSQL or MySQL)
- [ ] Create database and user
- [ ] Configure database connection
- [ ] Test database connectivity
- [ ] Set up automated backups
- [ ] Configure backup retention policy

### Configuration
- [ ] Review `config/bots.ini` settings
- [ ] Configure email settings for error reports
- [ ] Set appropriate time zone
- [ ] Configure log rotation
- [ ] Set file size limits
- [ ] Configure rate limits

### Infrastructure
- [ ] Provision server(s)
- [ ] Install required software
- [ ] Configure reverse proxy (nginx/Apache)
- [ ] Set up monitoring
- [ ] Configure alerting
- [ ] Plan for scaling

## Deployment Options

### Option 1: Traditional Server Deployment

#### 1. Server Setup

**Ubuntu/Debian:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3 python3-pip python3-venv nginx

# Install PostgreSQL (recommended)
sudo apt install -y postgresql postgresql-contrib

# Create application user
sudo useradd -m -s /bin/bash botsedi
sudo su - botsedi
```

**CentOS/RHEL:**
```bash
# Update system
sudo yum update -y

# Install Python and dependencies
sudo yum install -y python3 python3-pip nginx

# Install PostgreSQL
sudo yum install -y postgresql-server postgresql-contrib
sudo postgresql-setup initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create application user
sudo useradd -m -s /bin/bash botsedi
sudo su - botsedi
```

#### 2. Application Setup

```bash
# Clone repository
cd /home/botsedi
git clone <repository-url> bots-edi
cd bots-edi

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Edit with production settings
```

#### 3. Database Setup

**PostgreSQL:**
```bash
# Create database and user
sudo -u postgres psql
```

```sql
CREATE DATABASE botsdb;
CREATE USER botsuser WITH PASSWORD 'secure_password_here';
ALTER ROLE botsuser SET client_encoding TO 'utf8';
ALTER ROLE botsuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE botsuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE botsdb TO botsuser;
\q
```

Update `.env`:
```env
DATABASE_ENGINE=postgresql_psycopg2
DATABASE_NAME=botsdb
DATABASE_USER=botsuser
DATABASE_PASSWORD=secure_password_here
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

#### 4. Initialize Application

```bash
# Initialize database
python scripts/init_database.py

# Create admin user
cd env/default
python manage_users.py create admin "SecurePassword123!"

# Initialize API permissions
python usersys/api_management.py init_permissions
```

#### 5. Configure Systemd Service

Create `/etc/systemd/system/bots-webserver.service`:

```ini
[Unit]
Description=Bots EDI Webserver
After=network.target postgresql.service

[Service]
Type=simple
User=botsedi
Group=botsedi
WorkingDirectory=/home/botsedi/bots-edi/env/default
Environment="PATH=/home/botsedi/bots-edi/venv/bin"
ExecStart=/home/botsedi/bots-edi/venv/bin/bots-webserver
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable bots-webserver
sudo systemctl start bots-webserver
sudo systemctl status bots-webserver
```

#### 6. Configure Nginx Reverse Proxy

Create `/etc/nginx/sites-available/bots-edi`:

```nginx
upstream bots_backend {
    server 127.0.0.1:8080;
}

server {
    listen 80;
    server_name your-domain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    # SSL Configuration
    ssl_certificate /etc/ssl/certs/your-domain.crt;
    ssl_certificate_key /etc/ssl/private/your-domain.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Logging
    access_log /var/log/nginx/bots-edi-access.log;
    error_log /var/log/nginx/bots-edi-error.log;
    
    # Max upload size
    client_max_body_size 10M;
    
    location / {
        proxy_pass http://bots_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    location /static/ {
        alias /home/botsedi/bots-edi/env/default/botssys/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/bots-edi /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 7. SSL Certificate (Let's Encrypt)

```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
sudo certbot renew --dry-run
```

### Option 2: Docker Deployment

#### 1. Create Dockerfile

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 botsedi && \
    chown -R botsedi:botsedi /app
USER botsedi

# Expose port
EXPOSE 8080

# Run application
CMD ["bots-webserver"]
```

#### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: botsdb
      POSTGRES_USER: botsuser
      POSTGRES_PASSWORD: ${DATABASE_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - bots_network
    restart: unless-stopped

  web:
    build: .
    command: bots-webserver
    volumes:
      - ./env/default:/app/env/default
    ports:
      - "8080:8080"
    environment:
      - DATABASE_ENGINE=postgresql_psycopg2
      - DATABASE_NAME=botsdb
      - DATABASE_USER=botsuser
      - DATABASE_PASSWORD=${DATABASE_PASSWORD}
      - DATABASE_HOST=db
      - DATABASE_PORT=5432
      - DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
      - DEBUG=False
    depends_on:
      - db
    networks:
      - bots_network
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  bots_network:
    driver: bridge
```

#### 3. Deploy with Docker

```bash
# Build and start
docker-compose up -d

# Initialize database
docker-compose exec web python scripts/init_database.py

# View logs
docker-compose logs -f web

# Stop
docker-compose down
```

## Post-Deployment

### 1. Verify Installation

```bash
# Check service status
sudo systemctl status bots-webserver

# Check logs
sudo journalctl -u bots-webserver -f

# Test web interface
curl https://your-domain.com

# Test API
curl -H "X-API-Key: your-key" https://your-domain.com/api/v1/status
```

### 2. Create Backup Cron Job

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /home/botsedi/bots-edi/scripts/backup.sh
```

### 3. Configure Log Rotation

Create `/etc/logrotate.d/bots-edi`:

```
/home/botsedi/bots-edi/env/default/botssys/logging/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    missingok
    create 0640 botsedi botsedi
}
```

### 4. Set Up Monitoring

**Basic monitoring with systemd:**
```bash
# Email on service failure
sudo systemctl edit bots-webserver

# Add:
[Service]
OnFailure=status-email@%n.service
```

**Advanced monitoring options:**
- Prometheus + Grafana
- Datadog
- New Relic
- CloudWatch (AWS)

### 5. Configure Alerting

Set up alerts for:
- Service downtime
- High error rates
- Disk space usage
- Database connection issues
- API rate limit violations

## Scaling

### Horizontal Scaling

1. **Load Balancer**: Use nginx or HAProxy
2. **Multiple App Servers**: Run multiple instances
3. **Shared Database**: All instances connect to same DB
4. **Shared Storage**: Use NFS or S3 for file storage

### Vertical Scaling

1. **Increase Resources**: More CPU, RAM
2. **Optimize Database**: Indexes, query optimization
3. **Caching**: Redis or Memcached
4. **CDN**: For static files

## Maintenance

### Regular Tasks

**Daily:**
- Monitor logs for errors
- Check disk space
- Verify backups

**Weekly:**
- Review API audit logs
- Check for security updates
- Monitor performance metrics

**Monthly:**
- Rotate API keys
- Review user permissions
- Update dependencies
- Test disaster recovery

### Updates

```bash
# Backup first
./scripts/backup.sh

# Pull updates
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# Run migrations
cd env/default
python manage.py migrate

# Restart service
sudo systemctl restart bots-webserver
```

## Troubleshooting

### Service Won't Start

```bash
# Check logs
sudo journalctl -u bots-webserver -n 50

# Check configuration
cd env/default
python -c "import settings"

# Check database connection
python -c "import django; django.setup(); from django.db import connection; connection.ensure_connection()"
```

### High Memory Usage

```bash
# Check process
ps aux | grep bots

# Monitor in real-time
top -p $(pgrep -f bots-webserver)

# Restart service
sudo systemctl restart bots-webserver
```

### Database Issues

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connections
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity;"

# Restart database
sudo systemctl restart postgresql
```

## Rollback Procedure

```bash
# Stop service
sudo systemctl stop bots-webserver

# Restore from backup
tar -xzf backups/bots_backup_YYYYMMDD.tar.gz

# Restore database
sudo -u postgres psql botsdb < backup/database.sql

# Start service
sudo systemctl start bots-webserver
```

## Support

For deployment issues:
- Check logs first
- Review documentation
- Open GitHub issue
- Contact support team

## Security Reminders

- Keep system updated
- Monitor security advisories
- Regular security audits
- Principle of least privilege
- Regular password rotation
- Monitor access logs
- Encrypt sensitive data
- Use strong authentication

---

**Last Updated**: 2025-11-05  
**Version**: 1.0.0

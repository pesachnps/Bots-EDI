# Bots EDI Docker Deployment

## 🐳 Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed
- At least 2GB RAM available

### Deployment Options

#### Option 1: Using Docker Compose (Recommended)
```bash
# Clone or copy the Bots EDI installation
git clone <your-repo> bots-edi
cd bots-edi

# Start the service
docker-compose up -d

# Access the web interface
open http://localhost:8080
```

#### Option 2: Using Docker directly
```bash
# Build the image
docker build -t bots-edi .

# Run the container
docker run -d \
  --name bots-edi \
  -p 8080:8080 \
  -v $(pwd)/config:/app/bots_env/config:ro \
  -v $(pwd)/usersys:/app/bots_env/usersys \
  -v $(pwd)/botssys:/app/bots_env/botssys \
  bots-edi
```

## 📁 Volume Mounts

### Configuration (Read-only)
- `./config:/app/bots_env/config:ro`
  - `bots.ini` - Main configuration
  - `settings.py` - Django settings

### User Plugins (Writable)
- `./usersys:/app/bots_env/usersys`
  - `grammars/` - EDI format definitions
  - `mappings/` - Translation scripts
  - `routescripts/` - Route configurations
  - `partners/` - Trading partner info

### System Data (Writable)
- `./botssys:/app/bots_env/botssys`
  - `infile/` - Input EDI files
  - `outfile/` - Output EDI files
  - `sqlitedb/` - SQLite database
  - `logs/` - Application logs
  - `archive/` - Archived files

## 🔧 Configuration

### Environment Variables
- `BOTSENV=docker` - Bots environment identifier
- `PYTHONUNBUFFERED=1` - Python output buffering
- `TZ=UTC` - Timezone setting

### Database Options

#### Default: SQLite
- Database file: `botssys/sqlitedb/botsdb`
- No additional configuration needed

#### Optional: PostgreSQL
Uncomment the PostgreSQL service in `docker-compose.yml` and update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'botsdb',
        'USER': 'bots',
        'PASSWORD': 'botsbots',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}
```

## 🚀 Production Deployment

### Security Considerations
1. **Change Default Passwords**: Update Django admin credentials
2. **Use HTTPS**: Configure SSL/TLS termination
3. **Network Isolation**: Use Docker networks
4. **Resource Limits**: Set memory and CPU limits

### Resource Limits
```yaml
services:
  bots-edi:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
```

### Reverse Proxy (Nginx)
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📊 Monitoring

### Health Checks
The container includes built-in health checks:
```bash
# Check container health
docker ps

# View health logs
docker inspect bots-edi-server | grep Health -A 10
```

### Logs
```bash
# View application logs
docker logs bots-edi-server

# Follow logs in real-time
docker logs -f bots-edi-server

# View specific log files
docker exec bots-edi-server tail -f /app/bots_env/botssys/logs/bots.log
```

## 🔧 Development

### Hot Reloading
For development with hot reloading:
```yaml
volumes:
  - ./usersys:/app/bots_env/usersys:delegated
  - ./botssys:/app/bots_env/botssys:delegated
```

### Plugin Development
1. Edit plugin files in `./usersys/`
2. Changes are reflected immediately in the container
3. Access web interface to test changes

## 🔄 Backup and Recovery

### Data Backup
```bash
# Backup database and configuration
docker run --rm -v bots-edi_botssys:/data -v $(pwd):/backup \
  alpine tar czf /backup/bots-backup-$(date +%Y%m%d).tar.gz -C /data .

# Backup user plugins
docker run --rm -v bots-edi_usersys:/data -v $(pwd):/backup \
  alpine tar czf /backup/bots-plugins-$(date +%Y%m%d).tar.gz -C /data .
```

### Recovery
```bash
# Restore database
docker run --rm -v bots-edi_botssys:/data -v $(pwd):/backup \
  alpine tar xzf /backup/bots-backup-20251105.tar.gz -C /data

# Restore plugins
docker run --rm -v bots-edi_usersys:/data -v $(pwd):/backup \
  alpine tar xzf /backup/bots-plugins-20251105.tar.gz -C /data
```

## 🐛 Troubleshooting

### Common Issues

#### Container Won't Start
```bash
# Check logs
docker logs bots-edi-server

# Check configuration
docker exec bots-edi-server cat /app/bots_env/config/bots.ini
```

#### Permission Issues
```bash
# Fix ownership on host
sudo chown -R 1000:1000 ./botssys ./usersys
```

#### Database Issues
```bash
# Access database directly
docker exec -it bots-edi-server sqlite3 /app/bots_env/botssys/sqlitedb/botsdb
```

### Performance Tuning
- Use SSD storage for `botssys` volume
- Allocate sufficient memory (2GB+ recommended)
- Monitor container resource usage

## 📚 Additional Resources

- [Bots EDI Documentation](https://bots.sourceforge.io/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Container Information:**
- Base Image: Python 3.13 Slim
- Web Port: 8080
- Default Database: SQLite
- Plugin Support: Full (20 plugins pre-installed)
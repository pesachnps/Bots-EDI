# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it by:

1. **DO NOT** open a public GitHub issue
2. Email security details to the repository maintainers
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours and work with you to address the issue.

## Security Best Practices

### Production Deployment

#### 1. Environment Configuration

**Critical Settings:**
```env
# MUST be False in production
DEBUG=False

# Generate unique secret key
DJANGO_SECRET_KEY=<use-django-get-random-secret-key>

# Restrict allowed hosts
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

**Generate Secret Key:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### 2. HTTPS/SSL Configuration

Always use HTTPS in production. Configure SSL in `config/bots.ini`:

```ini
[webserver]
ssl_certificate = /path/to/certificate.crt
ssl_private_key = /path/to/private.key
```

#### 3. Database Security

**SQLite (Development Only):**
- Not recommended for production
- File permissions: `chmod 600 botssys/sqlitedb/botsdb`

**PostgreSQL/MySQL (Production):**
- Use strong passwords
- Restrict database user permissions
- Enable SSL connections
- Regular backups with encryption

#### 4. API Key Management

**Best Practices:**
- Generate strong, random API keys (48+ characters)
- Store securely (environment variables, secrets manager)
- Never commit to version control
- Rotate regularly (every 90 days recommended)
- Set expiration dates for temporary access
- Use IP whitelisting when possible
- Grant minimal required permissions

**Create Secure API Key:**
```bash
python usersys/api_management.py create "Production API" admin \
  file_upload file_download report_view
```

**Revoke Compromised Key:**
```bash
python usersys/api_management.py revoke <api-key>
```

#### 5. User Account Security

**Password Requirements:**
- Minimum 12 characters
- Mix of uppercase, lowercase, numbers, symbols
- No common passwords
- Change default passwords immediately

**Create Admin User:**
```bash
python manage_users.py create admin "StrongP@ssw0rd123!"
```

#### 6. File Upload Security

**Validation:**
- Limit file sizes (default: 5MB)
- Validate file types
- Scan for malware
- Sanitize filenames

**Configuration in `config/bots.ini`:**
```ini
[settings]
maxfilesizeincoming = 5000000
```

#### 7. Network Security

**Firewall Rules:**
- Restrict access to webserver port (default: 8080)
- Allow only necessary IP ranges
- Use VPN for remote access

**IP Whitelisting:**
Configure in Django admin for each API key.

#### 8. Logging and Monitoring

**Enable Audit Logging:**
All API requests are automatically logged. Review regularly:

```bash
python usersys/api_management.py audit 1000
```

**Monitor for:**
- Failed authentication attempts
- Rate limit violations
- Unusual access patterns
- Error spikes

**Log Files:**
- `botssys/logging/webserver*.log`
- `botssys/logging/engine*.log`

#### 9. Regular Updates

**Keep Updated:**
- Bots EDI framework
- Django
- Python
- Operating system
- Dependencies

**Check for Updates:**
```bash
pip list --outdated
```

#### 10. Backup and Recovery

**Regular Backups:**
- Database (daily)
- Configuration files
- Custom scripts and mappings
- API keys and permissions

**Backup Script Example:**
```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
tar -czf backup-$DATE.tar.gz \
  env/default/config/ \
  env/default/usersys/ \
  env/default/botssys/sqlitedb/
```

## Security Checklist

### Pre-Production

- [ ] Set `DEBUG=False`
- [ ] Generate unique `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Enable HTTPS/SSL
- [ ] Change all default passwords
- [ ] Configure production database
- [ ] Set up database backups
- [ ] Configure email for error reports
- [ ] Review file upload limits
- [ ] Set up firewall rules
- [ ] Configure log rotation
- [ ] Test disaster recovery

### Post-Deployment

- [ ] Monitor logs daily
- [ ] Review API audit logs weekly
- [ ] Rotate API keys quarterly
- [ ] Update dependencies monthly
- [ ] Test backups monthly
- [ ] Review user permissions quarterly
- [ ] Security audit annually

## Common Vulnerabilities

### 1. Exposed API Keys

**Risk:** Unauthorized access to system

**Prevention:**
- Never commit API keys to version control
- Use environment variables
- Rotate keys regularly
- Monitor audit logs

### 2. SQL Injection

**Risk:** Database compromise

**Prevention:**
- Django ORM provides protection
- Never use raw SQL with user input
- Validate all inputs

### 3. Cross-Site Scripting (XSS)

**Risk:** Session hijacking

**Prevention:**
- Django templates auto-escape
- Validate file uploads
- Sanitize user inputs

### 4. Cross-Site Request Forgery (CSRF)

**Risk:** Unauthorized actions

**Prevention:**
- Django CSRF middleware enabled
- API uses token authentication
- Validate origin headers

### 5. Insecure Direct Object References

**Risk:** Unauthorized file access

**Prevention:**
- Validate file paths
- Check permissions
- Use relative paths only

### 6. Rate Limiting Bypass

**Risk:** DoS attacks

**Prevention:**
- API rate limiting enabled
- Monitor usage patterns
- Block suspicious IPs

### 7. Information Disclosure

**Risk:** Sensitive data exposure

**Prevention:**
- Disable DEBUG in production
- Custom error pages
- Sanitize error messages
- Secure log files

## Incident Response

### If Security Breach Occurs:

1. **Immediate Actions:**
   - Revoke compromised API keys
   - Change all passwords
   - Review audit logs
   - Identify scope of breach

2. **Investigation:**
   - Analyze logs
   - Identify attack vector
   - Document findings

3. **Remediation:**
   - Patch vulnerabilities
   - Update security measures
   - Restore from clean backup if needed

4. **Communication:**
   - Notify affected parties
   - Document incident
   - Update security procedures

5. **Prevention:**
   - Implement additional controls
   - Update monitoring
   - Train team members

## Security Contacts

For security issues:
- Email: [security contact]
- Response time: 48 hours
- PGP key: [if applicable]

## Compliance

This system may need to comply with:
- GDPR (data protection)
- PCI DSS (payment card data)
- HIPAA (healthcare data)
- SOX (financial data)

Consult with compliance officers for specific requirements.

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/)

## Version History

- 1.0 (2025-11-05): Initial security policy

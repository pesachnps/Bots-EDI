#!/bin/bash
# Security Hardening Script for EDI System
# Run this script to apply security best practices

set -e

echo "==================================="
echo "EDI System Security Hardening"
echo "==================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
   echo -e "${RED}Do not run this script as root${NC}"
   exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found${NC}"
    echo "Please create .env from .env.example first"
    exit 1
fi

echo "Step 1: Checking SECRET_KEY..."
if grep -q "change-this-to-a-random-secret-key" .env; then
    echo -e "${RED}✗ SECRET_KEY is still default!${NC}"
    echo "Generating new SECRET_KEY..."
    NEW_SECRET=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
    sed -i.bak "s/DJANGO_SECRET_KEY=.*/DJANGO_SECRET_KEY=$NEW_SECRET/" .env
    echo -e "${GREEN}✓ New SECRET_KEY generated${NC}"
else
    echo -e "${GREEN}✓ SECRET_KEY is set${NC}"
fi

echo ""
echo "Step 2: Checking DEBUG setting..."
if grep -q "DEBUG=True" .env; then
    echo -e "${YELLOW}⚠ DEBUG is True - should be False in production${NC}"
    read -p "Set DEBUG=False? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sed -i.bak "s/DEBUG=True/DEBUG=False/" .env
        echo -e "${GREEN}✓ DEBUG set to False${NC}"
    fi
else
    echo -e "${GREEN}✓ DEBUG is False${NC}"
fi

echo ""
echo "Step 3: Checking ALLOWED_HOSTS..."
if grep -q "ALLOWED_HOSTS=\*" .env || ! grep -q "ALLOWED_HOSTS=" .env; then
    echo -e "${YELLOW}⚠ ALLOWED_HOSTS is not properly configured${NC}"
    read -p "Enter your domain (e.g., yourdomain.com): " domain
    if [ ! -z "$domain" ]; then
        sed -i.bak "s/ALLOWED_HOSTS=.*/ALLOWED_HOSTS=localhost,127.0.0.1,$domain/" .env
        echo -e "${GREEN}✓ ALLOWED_HOSTS configured${NC}"
    fi
else
    echo -e "${GREEN}✓ ALLOWED_HOSTS is configured${NC}"
fi

echo ""
echo "Step 4: Checking SSL/HTTPS settings..."
if ! grep -q "SECURE_SSL_REDIRECT" .env; then
    echo "Adding SSL/HTTPS settings..."
    cat >> .env << EOF

# SSL/HTTPS Settings
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=31536000
EOF
    echo -e "${GREEN}✓ SSL settings added (disabled by default)${NC}"
    echo -e "${YELLOW}⚠ Enable SECURE_SSL_REDIRECT=True when you have SSL certificate${NC}"
else
    echo -e "${GREEN}✓ SSL settings present${NC}"
fi

echo ""
echo "Step 5: Setting file permissions..."
chmod 600 .env
echo -e "${GREEN}✓ .env permissions set to 600${NC}"

if [ -d "env/default/botssys/sqlitedb" ]; then
    chmod 700 env/default/botssys/sqlitedb
    chmod 600 env/default/botssys/sqlitedb/*.db 2>/dev/null || true
    echo -e "${GREEN}✓ Database file permissions secured${NC}"
fi

if [ -d "env/default/botssys/logging" ]; then
    chmod 750 env/default/botssys/logging
    echo -e "${GREEN}✓ Log directory permissions secured${NC}"
fi

echo ""
echo "Step 6: Checking password requirements..."
if ! grep -q "PARTNER_PASSWORD_MIN_LENGTH" .env; then
    echo "Adding password policy settings..."
    cat >> .env << EOF

# Password Policy
PARTNER_PASSWORD_MIN_LENGTH=8
PARTNER_FAILED_LOGIN_LOCKOUT=5
PARTNER_LOCKOUT_DURATION=900
EOF
    echo -e "${GREEN}✓ Password policy settings added${NC}"
else
    echo -e "${GREEN}✓ Password policy configured${NC}"
fi

echo ""
echo "Step 7: Checking email configuration..."
if grep -q "DEFAULT_FROM_EMAIL=noreply@yourdomain.com" .env; then
    echo -e "${YELLOW}⚠ Email configuration uses default domain${NC}"
    read -p "Enter your email domain (e.g., yourdomain.com): " email_domain
    if [ ! -z "$email_domain" ]; then
        sed -i.bak "s/noreply@yourdomain.com/noreply@$email_domain/" .env
        echo -e "${GREEN}✓ Email domain updated${NC}"
    fi
else
    echo -e "${GREEN}✓ Email configuration set${NC}"
fi

echo ""
echo "Step 8: Creating security checklist..."
cat > SECURITY_CHECKLIST.txt << EOF
EDI System Security Checklist
Generated: $(date)

CRITICAL:
[ ] SECRET_KEY is unique and not in version control
[ ] DEBUG=False in production
[ ] ALLOWED_HOSTS configured with actual domains
[ ] SSL/HTTPS enabled (SECURE_SSL_REDIRECT=True)
[ ] Database password is strong and unique
[ ] .env file permissions are 600
[ ] Database file permissions are secure

IMPORTANT:
[ ] Email configuration is correct
[ ] Password policy is enforced
[ ] Session timeout is configured (30 minutes)
[ ] Account lockout is enabled (5 attempts)
[ ] Activity logging is enabled
[ ] Regular backups are configured
[ ] Firewall rules are in place
[ ] Only necessary ports are open

RECOMMENDED:
[ ] Two-factor authentication enabled
[ ] Rate limiting configured
[ ] Monitoring and alerting set up
[ ] Regular security updates scheduled
[ ] Penetration testing performed
[ ] Security audit completed
[ ] Incident response plan documented
[ ] Staff security training completed

ONGOING:
[ ] Review activity logs weekly
[ ] Update dependencies monthly
[ ] Review user permissions quarterly
[ ] Security audit annually
[ ] Backup restoration tested quarterly
EOF

echo -e "${GREEN}✓ Security checklist created: SECURITY_CHECKLIST.txt${NC}"

echo ""
echo "Step 9: Running security checks..."

# Check for common security issues
ISSUES=0

# Check for default passwords in code
if grep -r "password.*=.*'password'" env/default/usersys/*.py 2>/dev/null; then
    echo -e "${RED}✗ Found hardcoded passwords in code${NC}"
    ISSUES=$((ISSUES+1))
fi

# Check for exposed secret keys in code
if grep -r "SECRET_KEY.*=.*['\"]" env/default/config/settings.py 2>/dev/null | grep -v "os.environ"; then
    echo -e "${YELLOW}⚠ SECRET_KEY might be hardcoded${NC}"
fi

# Check for SQL injection vulnerabilities (basic check)
if grep -r "execute.*%.*%" env/default/usersys/*.py 2>/dev/null; then
    echo -e "${YELLOW}⚠ Possible SQL injection vulnerability (string formatting in SQL)${NC}"
    ISSUES=$((ISSUES+1))
fi

if [ $ISSUES -eq 0 ]; then
    echo -e "${GREEN}✓ No obvious security issues found${NC}"
else
    echo -e "${YELLOW}⚠ Found $ISSUES potential security issues${NC}"
fi

echo ""
echo "Step 10: Generating security report..."
cat > SECURITY_REPORT.txt << EOF
EDI System Security Hardening Report
Generated: $(date)

Configuration Status:
- SECRET_KEY: $(grep -q "change-this-to-a-random-secret-key" .env && echo "DEFAULT (INSECURE)" || echo "Custom (OK)")
- DEBUG: $(grep "DEBUG=" .env | cut -d'=' -f2)
- ALLOWED_HOSTS: $(grep "ALLOWED_HOSTS=" .env | cut -d'=' -f2)
- SSL_REDIRECT: $(grep "SECURE_SSL_REDIRECT=" .env | cut -d'=' -f2 || echo "Not set")
- Password Min Length: $(grep "PARTNER_PASSWORD_MIN_LENGTH=" .env | cut -d'=' -f2 || echo "Not set")
- Login Lockout: $(grep "PARTNER_FAILED_LOGIN_LOCKOUT=" .env | cut -d'=' -f2 || echo "Not set")

File Permissions:
- .env: $(stat -c %a .env 2>/dev/null || stat -f %A .env 2>/dev/null || echo "Unknown")
- Database: $(stat -c %a env/default/botssys/sqlitedb 2>/dev/null || stat -f %A env/default/botssys/sqlitedb 2>/dev/null || echo "Not found")

Security Issues Found: $ISSUES

Next Steps:
1. Review SECURITY_CHECKLIST.txt and complete all items
2. Enable SSL/HTTPS in production
3. Configure proper database (PostgreSQL/MySQL) for production
4. Set up monitoring and alerting
5. Schedule regular security audits
6. Configure automated backups
7. Review and test incident response plan

For more information, see:
- SECURITY.md
- BACKEND_DEPLOYMENT_CHECKLIST.md
- PERFORMANCE_OPTIMIZATION_GUIDE.md
EOF

echo -e "${GREEN}✓ Security report created: SECURITY_REPORT.txt${NC}"

echo ""
echo "==================================="
echo "Security Hardening Complete!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Review SECURITY_CHECKLIST.txt"
echo "2. Review SECURITY_REPORT.txt"
echo "3. Enable SSL/HTTPS when ready"
echo "4. Configure production database"
echo "5. Set up monitoring"
echo ""
echo -e "${YELLOW}Important: Restart the application for changes to take effect${NC}"
echo ""

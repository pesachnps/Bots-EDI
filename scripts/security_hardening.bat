@echo off
REM Security Hardening Script for EDI System (Windows)
REM Run this script to apply security best practices

echo ===================================
echo EDI System Security Hardening
echo ===================================
echo.

REM Check if .env file exists
if not exist .env (
    echo Error: .env file not found
    echo Please create .env from .env.example first
    exit /b 1
)

echo Step 1: Checking SECRET_KEY...
findstr /C:"change-this-to-a-random-secret-key" .env >nul
if %errorlevel%==0 (
    echo [X] SECRET_KEY is still default!
    echo Generating new SECRET_KEY...
    for /f "delims=" %%i in ('python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"') do set NEW_SECRET=%%i
    powershell -Command "(gc .env) -replace 'DJANGO_SECRET_KEY=.*', 'DJANGO_SECRET_KEY=%NEW_SECRET%' | Out-File -encoding ASCII .env"
    echo [OK] New SECRET_KEY generated
) else (
    echo [OK] SECRET_KEY is set
)

echo.
echo Step 2: Checking DEBUG setting...
findstr /C:"DEBUG=True" .env >nul
if %errorlevel%==0 (
    echo [!] DEBUG is True - should be False in production
    set /p response="Set DEBUG=False? (y/n): "
    if /i "%response%"=="y" (
        powershell -Command "(gc .env) -replace 'DEBUG=True', 'DEBUG=False' | Out-File -encoding ASCII .env"
        echo [OK] DEBUG set to False
    )
) else (
    echo [OK] DEBUG is False
)

echo.
echo Step 3: Checking ALLOWED_HOSTS...
findstr /C:"ALLOWED_HOSTS=*" .env >nul
if %errorlevel%==0 (
    echo [!] ALLOWED_HOSTS is not properly configured
    set /p domain="Enter your domain (e.g., yourdomain.com): "
    if not "%domain%"=="" (
        powershell -Command "(gc .env) -replace 'ALLOWED_HOSTS=.*', 'ALLOWED_HOSTS=localhost,127.0.0.1,%domain%' | Out-File -encoding ASCII .env"
        echo [OK] ALLOWED_HOSTS configured
    )
) else (
    echo [OK] ALLOWED_HOSTS is configured
)

echo.
echo Step 4: Checking SSL/HTTPS settings...
findstr /C:"SECURE_SSL_REDIRECT" .env >nul
if %errorlevel% neq 0 (
    echo Adding SSL/HTTPS settings...
    echo. >> .env
    echo # SSL/HTTPS Settings >> .env
    echo SECURE_SSL_REDIRECT=False >> .env
    echo SECURE_HSTS_SECONDS=31536000 >> .env
    echo [OK] SSL settings added
    echo [!] Enable SECURE_SSL_REDIRECT=True when you have SSL certificate
) else (
    echo [OK] SSL settings present
)

echo.
echo Step 5: Checking password requirements...
findstr /C:"PARTNER_PASSWORD_MIN_LENGTH" .env >nul
if %errorlevel% neq 0 (
    echo Adding password policy settings...
    echo. >> .env
    echo # Password Policy >> .env
    echo PARTNER_PASSWORD_MIN_LENGTH=8 >> .env
    echo PARTNER_FAILED_LOGIN_LOCKOUT=5 >> .env
    echo PARTNER_LOCKOUT_DURATION=900 >> .env
    echo [OK] Password policy settings added
) else (
    echo [OK] Password policy configured
)

echo.
echo Step 6: Creating security checklist...
(
echo EDI System Security Checklist
echo Generated: %date% %time%
echo.
echo CRITICAL:
echo [ ] SECRET_KEY is unique and not in version control
echo [ ] DEBUG=False in production
echo [ ] ALLOWED_HOSTS configured with actual domains
echo [ ] SSL/HTTPS enabled
echo [ ] Database password is strong and unique
echo [ ] File permissions are secure
echo.
echo IMPORTANT:
echo [ ] Email configuration is correct
echo [ ] Password policy is enforced
echo [ ] Session timeout is configured
echo [ ] Account lockout is enabled
echo [ ] Activity logging is enabled
echo [ ] Regular backups are configured
echo [ ] Firewall rules are in place
echo.
echo RECOMMENDED:
echo [ ] Two-factor authentication enabled
echo [ ] Rate limiting configured
echo [ ] Monitoring and alerting set up
echo [ ] Regular security updates scheduled
echo [ ] Security audit completed
echo.
echo For more information, see:
echo - SECURITY.md
echo - BACKEND_DEPLOYMENT_CHECKLIST.md
echo - PERFORMANCE_OPTIMIZATION_GUIDE.md
) > SECURITY_CHECKLIST.txt

echo [OK] Security checklist created: SECURITY_CHECKLIST.txt

echo.
echo ===================================
echo Security Hardening Complete!
echo ===================================
echo.
echo Next steps:
echo 1. Review SECURITY_CHECKLIST.txt
echo 2. Enable SSL/HTTPS when ready
echo 3. Configure production database
echo 4. Set up monitoring
echo.
echo Important: Restart the application for changes to take effect
echo.

pause

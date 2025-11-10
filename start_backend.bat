@echo off
echo ========================================
echo Starting Bots EDI Backend Server
echo ========================================
echo.

:: Get script directory and navigate to env\default
cd /d "%~dp0env\default"

echo Checking if server is already running on port 8080...
netstat -ano | findstr :8080 > nul
if %errorlevel% equ 0 (
    echo WARNING: Port 8080 is already in use!
    echo Please stop the existing process or use a different port.
    pause
    exit /b 1
)

echo Starting Bots webserver...
echo.
echo Backend will be available at: http://localhost:8080
echo Django Admin: http://localhost:8080/admin
echo Modern EDI API: http://localhost:8080/modern-edi/api/v1/
echo.
echo Press Ctrl+C to stop the server
echo.

:: Start webserver using start_server.py (sets correct config path)
python start_server.py

pause

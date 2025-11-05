@echo off
REM Quick start script for Bots EDI Environment (Windows)

echo ==========================================
echo Bots EDI Environment - Quick Start
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed. Please install Python 3.8 or higher.
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python %PYTHON_VERSION% detected
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
echo Dependencies installed
echo.

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env >nul
    
    REM Generate secret key
    for /f "delims=" %%i in ('python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"') do set SECRET_KEY=%%i
    
    REM Update .env with generated secret key
    powershell -Command "(gc .env) -replace 'change-this-to-a-random-secret-key-in-production', '%SECRET_KEY%' | Out-File -encoding ASCII .env"
    
    echo .env file created with unique secret key
    echo.
) else (
    echo .env file already exists
    echo.
)

REM Initialize database
echo Initializing database...
python scripts\init_database.py

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Review and update .env file if needed
echo 2. Start the webserver:
echo    cd env\default
echo    bots-webserver
echo.
echo 3. Access the web interface:
echo    http://localhost:8080
echo.
echo 4. Login with default credentials:
echo    Username: admin
echo    Password: admin123
echo    WARNING: CHANGE THIS PASSWORD IMMEDIATELY!
echo.
echo 5. View API documentation:
echo    type API_DOCUMENTATION.md
echo.
echo For more information, see README.md
echo.

pause

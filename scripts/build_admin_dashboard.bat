@echo off
echo ========================================
echo Building Admin Dashboard Frontend
echo ========================================
echo.

cd env\default\usersys\static\modern-edi

echo Step 1: Installing dependencies...
call npm install
if errorlevel 1 (
    echo ERROR: npm install failed
    pause
    exit /b 1
)

echo.
echo Step 2: Building production bundle...
call npm run build
if errorlevel 1 (
    echo ERROR: npm build failed
    pause
    exit /b 1
)

echo.
echo Step 3: Collecting Django static files...
cd ..\..\..\..
python manage.py collectstatic --noinput
if errorlevel 1 (
    echo ERROR: collectstatic failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Admin Dashboard is ready at:
echo http://localhost:8080/modern-edi/admin/
echo.
echo Start the server with:
echo   cd env\default
echo   bots-webserver
echo.
pause

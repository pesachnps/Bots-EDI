@echo off
REM Backup script for Bots EDI Environment (Windows)

setlocal enabledelayedexpansion

REM Configuration
if "%BACKUP_DIR%"=="" set BACKUP_DIR=.\backups
set DATE=%date:~-4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set DATE=%DATE: =0%
set BACKUP_NAME=bots_backup_%DATE%
set ENV_DIR=env\default

REM Create backup directory
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

echo Starting Bots EDI backup...
echo Backup name: %BACKUP_NAME%

REM Create temporary directory for backup
set TEMP_BACKUP=%TEMP%\%BACKUP_NAME%
mkdir "%TEMP_BACKUP%"

REM Backup configuration
echo Backing up configuration...
xcopy /E /I /Y "%ENV_DIR%\config" "%TEMP_BACKUP%\config" >nul

REM Backup user scripts
echo Backing up user scripts...
xcopy /E /I /Y "%ENV_DIR%\usersys" "%TEMP_BACKUP%\usersys" >nul

REM Backup database
echo Backing up database...
mkdir "%TEMP_BACKUP%\database"
if exist "%ENV_DIR%\botssys\sqlitedb\botsdb" (
    copy "%ENV_DIR%\botssys\sqlitedb\botsdb" "%TEMP_BACKUP%\database\" >nul
)

REM Backup important system files
echo Backing up system files...
if exist "%ENV_DIR%\botssys\data" (
    xcopy /E /I /Y "%ENV_DIR%\botssys\data" "%TEMP_BACKUP%\data" >nul 2>nul
)

REM Create archive (requires 7-Zip or similar)
echo Creating archive...
if exist "C:\Program Files\7-Zip\7z.exe" (
    "C:\Program Files\7-Zip\7z.exe" a -tzip "%BACKUP_DIR%\%BACKUP_NAME%.zip" "%TEMP_BACKUP%\*" >nul
    echo Archive created successfully
) else (
    echo Warning: 7-Zip not found. Backup saved to: %TEMP_BACKUP%
    echo Install 7-Zip to create compressed archives
    move "%TEMP_BACKUP%" "%BACKUP_DIR%\%BACKUP_NAME%" >nul
)

REM Cleanup
if exist "%BACKUP_DIR%\%BACKUP_NAME%.zip" (
    rmdir /S /Q "%TEMP_BACKUP%"
)

echo.
echo Backup completed: %BACKUP_DIR%\%BACKUP_NAME%
echo.

endlocal

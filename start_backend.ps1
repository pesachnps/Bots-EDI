Write-Host "Starting Bots EDI Backend Server..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$PROJECT_ROOT = $env:PROJECT_ROOT
if (-not $PROJECT_ROOT) { $PROJECT_ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path }
Set-Location "$PROJECT_ROOT\env\default"

Write-Host "Checking if port 8080 is available..." -ForegroundColor Yellow
$port8080 = Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue
if ($port8080) {
    Write-Host "ERROR: Port 8080 is already in use!" -ForegroundColor Red
    Write-Host "Please stop the existing process first." -ForegroundColor Red
    pause
    exit 1
}

Write-Host "Starting backend server..." -ForegroundColor Green
Write-Host "Backend will be available at: http://localhost:8080" -ForegroundColor Cyan
Write-Host "Django Admin: http://localhost:8080/admin" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python -m bots.webserver -c"$PROJECT_ROOT\env\default\config"

#!/bin/bash
echo "========================================"
echo "Starting Bots EDI Backend Server"
echo "========================================"
echo ""

cd env/default

echo "Checking if server is already running on port 8080..."
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null ; then
    echo "WARNING: Port 8080 is already in use!"
    echo "Please stop the existing process or use a different port."
    exit 1
fi

echo "Starting Bots webserver..."
echo ""
echo "Backend will be available at: http://localhost:8080"
echo "Django Admin: http://localhost:8080/admin"
echo "Modern EDI API: http://localhost:8080/modern-edi/api/v1/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python start_server.py

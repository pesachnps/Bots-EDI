#!/bin/bash
echo "========================================"
echo "Starting Modern EDI Frontend Server"
echo "========================================"
echo ""

cd env/default/usersys/static/modern-edi

echo "Checking if server is already running on port 3000..."
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null ; then
    echo "WARNING: Port 3000 is already in use!"
    echo "Please stop the existing process or use a different port."
    exit 1
fi

echo "Starting Vite dev server..."
echo ""
echo "Frontend will be available at: http://localhost:3000/static/modern-edi/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

npm run dev

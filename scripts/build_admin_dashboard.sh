#!/bin/bash

echo "========================================"
echo "Building Admin Dashboard Frontend"
echo "========================================"
echo

cd env/default/usersys/static/modern-edi

echo "Step 1: Installing dependencies..."
npm install
if [ $? -ne 0 ]; then
    echo "ERROR: npm install failed"
    exit 1
fi

echo
echo "Step 2: Building production bundle..."
npm run build
if [ $? -ne 0 ]; then
    echo "ERROR: npm build failed"
    exit 1
fi

echo
echo "Step 3: Collecting Django static files..."
cd ../../../..
python manage.py collectstatic --noinput
if [ $? -ne 0 ]; then
    echo "ERROR: collectstatic failed"
    exit 1
fi

echo
echo "========================================"
echo "Build Complete!"
echo "========================================"
echo
echo "Admin Dashboard is ready at:"
echo "http://localhost:8080/modern-edi/admin/"
echo
echo "Start the server with:"
echo "  cd env/default"
echo "  bots-webserver"
echo

#!/bin/bash
# Quick start script for Bots EDI Environment

set -e

echo "=========================================="
echo "Bots EDI Environment - Quick Start"
echo "=========================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION detected"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

# Install dependencies
echo
echo "Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo
    echo "Creating .env file from template..."
    cp .env.example .env
    
    # Generate secret key
    SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
    
    # Update .env with generated secret key
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/change-this-to-a-random-secret-key-in-production/$SECRET_KEY/" .env
    else
        # Linux
        sed -i "s/change-this-to-a-random-secret-key-in-production/$SECRET_KEY/" .env
    fi
    
    echo "✅ .env file created with unique secret key"
else
    echo
    echo "ℹ️  .env file already exists"
fi

# Initialize database
echo
echo "Initializing database..."
python3 scripts/init_database.py

echo
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo
echo "Next steps:"
echo "1. Review and update .env file if needed"
echo "2. Start the webserver:"
echo "   cd env/default"
echo "   bots-webserver"
echo
echo "3. Access the web interface:"
echo "   http://localhost:8080"
echo
echo "4. Login with default credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo "   ⚠️  CHANGE THIS PASSWORD IMMEDIATELY!"
echo
echo "5. View API documentation:"
echo "   cat API_DOCUMENTATION.md"
echo
echo "For more information, see README.md"
echo

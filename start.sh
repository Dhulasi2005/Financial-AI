#!/bin/bash
# Startup script for Financial AI application

echo "🚀 Starting Financial AI application..."

# Check if we're in the right directory
echo "📁 Current directory: $(pwd)"
echo "🐍 Python version: $(python3 --version)"

# Check if requirements are installed
echo "📦 Checking installed packages..."
pip list | grep -E "(Flask|gunicorn)"

# Initialize database
echo "🗄️  Initializing database..."
python3 init_db.py

# Try to import the app
echo "🔧 Testing app import..."
python3 -c "from app import app; print('✅ App imported successfully')"

# Start the application
echo "🚀 Starting Gunicorn..."
exec gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120

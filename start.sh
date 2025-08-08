#!/bin/bash
# Startup script for Financial AI application

set -e  # Exit on any error

echo "🚀 Starting Financial AI application..."

# Check if we're in the right directory
echo "📁 Current directory: $(pwd)"
echo "🐍 Python version: $(python3 --version)"

# Check if requirements are installed
echo "📦 Checking installed packages..."
pip list | grep -E "(Flask|gunicorn)" || echo "⚠️  Some packages may not be installed"

# Create instance directory if it doesn't exist
echo "📁 Creating instance directory..."
mkdir -p instance

# Initialize database with error handling
echo "🗄️  Initializing database..."
if python3 init_db.py; then
    echo "✅ Database initialized successfully"
else
    echo "⚠️  Database initialization failed, continuing anyway..."
fi

# Try to import the app with error handling
echo "🔧 Testing app import..."
if python3 -c "from app import app; print('✅ App imported successfully')"; then
    echo "✅ App import successful"
else
    echo "❌ App import failed, but continuing..."
fi

# Check if PORT is set
if [ -z "$PORT" ]; then
    echo "⚠️  PORT not set, using default 5001"
    export PORT=5001
fi

echo "🚀 Starting Gunicorn on port $PORT..."

# Start the application with better error handling
exec gunicorn wsgi:app \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info

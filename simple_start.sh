#!/bin/bash
# Simple startup script for Financial AI application

echo "🚀 Simple startup for Financial AI application..."

# Set default port if not provided
export PORT=${PORT:-5001}

# Create instance directory
mkdir -p instance

# Start the application directly
echo "🚀 Starting Gunicorn on port $PORT..."

exec gunicorn wsgi:app \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --timeout 120 \
    --preload

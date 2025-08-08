#!/bin/bash

# Build script for Render deployment
echo "🔧 Building Financial AI application..."

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Build completed successfully!"

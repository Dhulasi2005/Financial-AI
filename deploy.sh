#!/bin/bash

# Financial AI Deployment Script
echo "🚀 Financial AI Deployment Script"
echo "=================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create it with your environment variables."
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found."
    exit 1
fi

echo "✅ Prerequisites check passed!"

# Show deployment options
echo ""
echo "📋 Choose your deployment platform:"
echo "1. Railway (Recommended for beginners)"
echo "2. Render (Great free tier)"
echo "3. Heroku (Classic choice)"
echo "4. DigitalOcean App Platform"
echo "5. VPS (Advanced users)"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo "🚂 Deploying to Railway..."
        echo "1. Go to https://railway.app"
        echo "2. Sign up with GitHub"
        echo "3. Click 'New Project' → 'Deploy from GitHub repo'"
        echo "4. Connect your repository"
        echo "5. Add environment variables in project settings"
        echo "6. Railway will auto-deploy on git push"
        echo ""
        echo "Run these commands:"
        echo "git add ."
        echo "git commit -m 'Deploy to Railway'"
        echo "git push origin main"
        ;;
    2)
        echo "🎨 Deploying to Render..."
        echo "1. Go to https://render.com"
        echo "2. Sign up with GitHub"
        echo "3. Click 'New +' → 'Web Service'"
        echo "4. Connect your GitHub repository"
        echo "5. Configure:"
        echo "   - Name: financial-ai"
        echo "   - Environment: Python 3"
        echo "   - Build Command: pip install -r requirements.txt"
        echo "   - Start Command: gunicorn app:app"
        echo "6. Add environment variables"
        echo "7. Click 'Create Web Service'"
        ;;
    3)
        echo "🦸 Deploying to Heroku..."
        echo "1. Install Heroku CLI: brew install heroku/brew/heroku"
        echo "2. Login: heroku login"
        echo "3. Create app: heroku create your-app-name"
        echo "4. Set environment variables:"
        echo "   heroku config:set SECRET_KEY=your-secret"
        echo "   heroku config:set NEWSAPI_KEY=your-key"
        echo "   heroku config:set GOOGLE_CLIENT_ID=your-id"
        echo "   heroku config:set GOOGLE_CLIENT_SECRET=your-secret"
        echo "5. Deploy: git push heroku main"
        ;;
    4)
        echo "🐙 Deploying to DigitalOcean App Platform..."
        echo "1. Go to https://digitalocean.com"
        echo "2. Sign up (requires credit card)"
        echo "3. Go to 'Apps' → 'Create App'"
        echo "4. Connect your GitHub repository"
        echo "5. Configure:"
        echo "   - Source: GitHub repository"
        echo "   - Branch: main"
        echo "   - Build Command: pip install -r requirements.txt"
        echo "   - Run Command: gunicorn app:app"
        echo "6. Add environment variables"
        echo "7. Click 'Create Resources'"
        ;;
    5)
        echo "🖥️  VPS Deployment (Advanced)..."
        echo "See DEPLOYMENT_GUIDE.md for detailed VPS instructions"
        echo "This requires server management skills"
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "📚 For detailed instructions, see DEPLOYMENT_GUIDE.md"
echo "🆘 For troubleshooting, check the guide or platform documentation"
echo ""
echo "�� Happy deploying!"

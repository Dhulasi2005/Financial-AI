#!/usr/bin/env python3
"""
Deployment check script for Financial AI application
"""

import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_environment():
    """Check environment variables and configuration"""
    logger.info("Checking environment...")
    
    # Check required environment variables
    required_vars = ['SECRET_KEY']
    optional_vars = ['NEWSAPI_KEY', 'GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET']
    
    missing_required = []
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
    
    if missing_required:
        logger.warning(f"Missing required environment variables: {missing_required}")
        logger.info("Setting default SECRET_KEY for development...")
        os.environ['SECRET_KEY'] = 'dev-secret-key-for-deployment'
    
    logger.info("Environment check completed")

def check_database():
    """Check database configuration"""
    logger.info("Checking database configuration...")
    
    try:
        from config import Config
        config = Config()
        logger.info(f"Database URI: {config.SQLALCHEMY_DATABASE_URI}")
        logger.info("Database configuration OK")
    except Exception as e:
        logger.error(f"Database configuration error: {e}")
        return False
    
    return True

def check_imports():
    """Check all critical imports"""
    logger.info("Checking imports...")
    
    try:
        # Test Flask and extensions
        from flask import Flask
        from flask_login import LoginManager
        from flask_sqlalchemy import SQLAlchemy
        from flask_mail import Mail
        from flask_wtf import FlaskForm
        from authlib.integrations.flask_client import OAuth
        logger.info("✓ Flask and extensions imported successfully")
        
        # Test custom modules
        from config import Config
        from models import db, User, NewsItem
        from forms import RegisterForm, LoginForm
        from news_scraper import fetch_news_by_country, get_supported_countries
        from rss_scraper import fetch_news_by_country as rss_fetch_news_by_country
        from sentiment import analyze_text
        from strategy import generate_strategy
        from ai_advisor import FinancialAIAdvisor
        logger.info("✓ Custom modules imported successfully")
        
        # Test app creation
        from app import create_app
        app = create_app()
        logger.info("✓ Flask app created successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Import error: {e}")
        return False

def check_wsgi():
    """Check WSGI configuration"""
    logger.info("Checking WSGI configuration...")
    
    try:
        from wsgi import app
        logger.info("✓ WSGI app imported successfully")
        return True
    except Exception as e:
        logger.error(f"❌ WSGI error: {e}")
        return False

def main():
    """Main deployment check"""
    logger.info("Starting deployment checks...")
    
    success = True
    
    # Check environment
    check_environment()
    
    # Check database
    success &= check_database()
    
    # Check imports
    success &= check_imports()
    
    # Check WSGI
    success &= check_wsgi()
    
    if success:
        logger.info("🎉 All deployment checks passed!")
        return 0
    else:
        logger.error("❌ Some deployment checks failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())

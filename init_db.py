#!/usr/bin/env python3
"""
Database initialization script for Financial AI application
"""

import os
import sys
from pathlib import Path

def init_database():
    """Initialize database and ensure directories exist"""
    try:
        # Create instance directory if it doesn't exist
        instance_path = Path("instance")
        instance_path.mkdir(exist_ok=True)
        print(f"✅ Instance directory created/verified: {instance_path.absolute()}")
        
        # Test database connection
        from app import app
        with app.app_context():
            from models import db
            db.create_all()
            print("✅ Database tables created successfully")
            
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
WSGI entry point for Financial AI application
This file is used by Gunicorn and other WSGI servers
"""

import os
from app import app

# Ensure the app is properly configured for production
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    app.run(host="0.0.0.0", port=port)

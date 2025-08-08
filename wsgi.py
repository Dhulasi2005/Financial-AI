#!/usr/bin/env python3
"""
WSGI entry point for Financial AI application
This file is used by Gunicorn and other WSGI servers
"""

import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from app import app
    logger.info("Successfully imported Flask app")
except ImportError as e:
    logger.error(f"Failed to import app: {e}")
    sys.exit(1)
except Exception as e:
    logger.error(f"Unexpected error importing app: {e}")
    sys.exit(1)

# Ensure the app is properly configured for production
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    logger.info(f"Starting app on port {port}")
    app.run(host="0.0.0.0", port=port)

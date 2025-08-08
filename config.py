import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    
    # Use a more deployment-friendly database path
    if os.getenv("DATABASE_URL"):
        # For production deployments (like Render)
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    else:
        # For local development
        instance_path = os.path.join(os.getcwd(), 'instance')
        os.makedirs(instance_path, exist_ok=True)
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(instance_path, 'app.db')}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")
    MAIL_SERVER = os.getenv("MAIL_SERVER", "")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    
    # OAuth Configuration
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
    APPLE_CLIENT_ID = os.getenv("APPLE_CLIENT_ID", "")
    APPLE_CLIENT_SECRET = os.getenv("APPLE_CLIENT_SECRET", "")
#!/usr/bin/env python3
"""
OAuth Diagnostic Tool for Financial AI App - Render.com Production
This script helps diagnose OAuth configuration issues for the Render deployment.
"""

import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

def main():
    """Run diagnostic for Render.com deployment."""
    print("🚀 OAuth Diagnostic Tool for Financial AI - Render.com")
    print("=" * 60)
    
    print("🔍 Checking Environment Variables...")
    client_id = os.getenv('GOOGLE_CLIENT_ID', '').strip()
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET', '').strip()
    secret_key = os.getenv('SECRET_KEY', '').strip()
    
    if client_id:
        print(f"✅ GOOGLE_CLIENT_ID: {client_id}")
    else:
        print("❌ GOOGLE_CLIENT_ID: NOT SET")
        
    if client_secret:
        print("✅ GOOGLE_CLIENT_SECRET: ******************** (hidden)")
    else:
        print("❌ GOOGLE_CLIENT_SECRET: NOT SET")
        
    if secret_key:
        print("✅ SECRET_KEY: ******************** (hidden)")
    else:
        print("❌ SECRET_KEY: NOT SET")
    
    print("\n🔍 Production Deployment Analysis...")
    print("🌐 Your Render.com URL: https://financial-ai-6z0s.onrender.com")
    
    print("\n📝 CRITICAL: Add these EXACT redirect URIs to your Google Cloud Console:")
    print("   1. https://financial-ai-6z0s.onrender.com/login/google/authorize")
    print("   2. http://localhost:5001/login/google/authorize (for local testing)")
    
    print("\n🛠️  How to fix Google Cloud Console:")
    print("   1. Go to https://console.cloud.google.com")
    print("   2. Navigate to APIs & Services → Credentials")
    print("   3. Find your OAuth 2.0 Client ID:")
    print(f"      {client_id}")
    print("   4. Click 'Edit' on your OAuth client")
    print("   5. In 'Authorized redirect URIs', add:")
    print("      https://financial-ai-6z0s.onrender.com/login/google/authorize")
    print("   6. Save changes")
    
    print("\n🧪 Test URLs for Manual Verification:")
    if client_id:
        # Production test URL
        prod_redirect = "https://financial-ai-6z0s.onrender.com/login/google/authorize"
        prod_test_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth"
            f"?client_id={client_id}"
            f"&redirect_uri={prod_redirect}"
            f"&response_type=code"
            f"&scope=openid%20email%20profile"
            f"&state=test"
        )
        
        print(f"\n🌐 Production Test URL:")
        print(f"   {prod_test_url}")
        print("\n   👆 Open this URL in browser to test OAuth flow")
        
        # Local test URL
        local_redirect = "http://localhost:5001/login/google/authorize"
        local_test_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth"
            f"?client_id={client_id}"
            f"&redirect_uri={local_redirect}"
            f"&response_type=code"
            f"&scope=openid%20email%20profile"
            f"&state=test"
        )
        
        print(f"\n🏠 Local Test URL (when running locally):")
        print(f"   {local_test_url}")
    
    print("\n🔍 Environment Variable Check for Render:")
    print("   Make sure these are set in your Render.com dashboard:")
    print("   - GOOGLE_CLIENT_ID")
    print("   - GOOGLE_CLIENT_SECRET") 
    print("   - SECRET_KEY")
    print("   - FLASK_ENV=production")
    
    print("\n" + "=" * 60)
    print("🎯 LIKELY CAUSE OF THE ISSUE:")
    print("   Your Google Cloud Console OAuth credentials do NOT include:")
    print("   https://financial-ai-6z0s.onrender.com/login/google/authorize")
    print("\n✅ Once you add this redirect URI to Google Console, OAuth should work!")
    
if __name__ == "__main__":
    main()

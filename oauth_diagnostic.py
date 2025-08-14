#!/usr/bin/env python3
"""
OAuth Diagnostic Tool for Financial AI App
This script helps diagnose OAuth configuration issues.
"""

import os
from dotenv import load_dotenv
import requests
import json
from urllib.parse import urlparse

load_dotenv()

def check_environment_variables():
    """Check if all required environment variables are set."""
    print("🔍 Checking Environment Variables...")
    
    required_vars = {
        'GOOGLE_CLIENT_ID': os.getenv('GOOGLE_CLIENT_ID'),
        'GOOGLE_CLIENT_SECRET': os.getenv('GOOGLE_CLIENT_SECRET'),
        'SECRET_KEY': os.getenv('SECRET_KEY')
    }
    
    for var_name, var_value in required_vars.items():
        if var_value:
            if var_name == 'GOOGLE_CLIENT_ID':
                print(f"✅ {var_name}: {var_value}")
            else:
                print(f"✅ {var_name}: {'*' * 20} (hidden)")
        else:
            print(f"❌ {var_name}: NOT SET")
    
    return all(required_vars.values())

def check_google_client_id_format():
    """Validate Google Client ID format."""
    print("\n🔍 Checking Google Client ID Format...")
    
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    if not client_id:
        print("❌ Google Client ID not found")
        return False
    
    # Google Client IDs should end with .apps.googleusercontent.com
    if client_id.endswith('.apps.googleusercontent.com'):
        print("✅ Google Client ID format is correct")
        return True
    else:
        print(f"❌ Google Client ID format is invalid: {client_id}")
        print("   Should end with .apps.googleusercontent.com")
        return False

def check_redirect_uris():
    """Check what redirect URIs should be configured."""
    print("\n🔍 Checking Redirect URI Configuration...")
    
    base_urls = [
        "http://localhost:5001",  # Development
        "http://localhost:5000",  # Alternative dev port
        "https://yourdomain.com", # Production placeholder
    ]
    
    print("📝 Required redirect URIs in Google Console:")
    for base_url in base_urls:
        redirect_uri = f"{base_url}/login/google/authorize"
        print(f"   {redirect_uri}")
    
    print("\n⚠️  Make sure these URIs are added to your Google OAuth credentials!")

def test_oauth_endpoints():
    """Test OAuth endpoints accessibility."""
    print("\n🔍 Testing OAuth Endpoints...")
    
    try:
        # Test if we can reach Google's OAuth discovery endpoint
        response = requests.get(
            'https://accounts.google.com/.well-known/openid-configuration',
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Google OAuth discovery endpoint is accessible")
            
            # Parse the response to get authorization endpoint
            data = response.json()
            auth_endpoint = data.get('authorization_endpoint')
            print(f"   Authorization endpoint: {auth_endpoint}")
        else:
            print(f"❌ Google OAuth discovery endpoint failed: {response.status_code}")
    
    except requests.RequestException as e:
        print(f"❌ Network error accessing Google OAuth: {e}")

def generate_test_urls():
    """Generate test URLs for manual testing."""
    print("\n🔗 Test URLs for Manual Testing:")
    
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    if not client_id:
        print("❌ Cannot generate test URLs - Google Client ID missing")
        return
    
    base_urls = ["http://localhost:5001", "http://localhost:5000"]
    
    for base_url in base_urls:
        redirect_uri = f"{base_url}/login/google/authorize"
        auth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth"
            f"?client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&response_type=code"
            f"&scope=openid%20email%20profile"
            f"&state=test"
        )
        print(f"\n🌐 Test URL for {base_url}:")
        print(f"   {auth_url}")

def check_common_issues():
    """Check for common OAuth configuration issues."""
    print("\n🔍 Checking Common Issues...")
    
    issues = []
    
    # Check Client ID format
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    if client_id and not client_id.endswith('.apps.googleusercontent.com'):
        issues.append("Invalid Google Client ID format")
    
    # Check if running on HTTPS in production
    if os.getenv('FLASK_ENV') == 'production' and os.getenv('PREFERRED_URL_SCHEME') != 'https':
        issues.append("Production should use HTTPS")
    
    if issues:
        print("❌ Issues found:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("✅ No common issues detected")

def main():
    """Run all diagnostic checks."""
    print("🚀 OAuth Diagnostic Tool for Financial AI")
    print("=" * 50)
    
    env_ok = check_environment_variables()
    client_id_ok = check_google_client_id_format()
    
    check_redirect_uris()
    test_oauth_endpoints()
    
    if env_ok and client_id_ok:
        generate_test_urls()
    
    check_common_issues()
    
    print("\n" + "=" * 50)
    if env_ok and client_id_ok:
        print("✅ OAuth configuration looks good!")
        print("💡 Next steps:")
        print("   1. Ensure redirect URIs are added to Google Console")
        print("   2. Test the OAuth flow in your application")
        print("   3. Check browser developer tools for any errors")
    else:
        print("❌ OAuth configuration needs attention")
        print("💡 Fix the issues above and run this diagnostic again")

if __name__ == "__main__":
    main()

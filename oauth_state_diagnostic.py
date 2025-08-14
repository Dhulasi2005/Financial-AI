#!/usr/bin/env python3
"""
OAuth State Parameter Diagnostic Script for Google OAuth Issues

This script helps diagnose OAuth state parameter validation issues
including session handling, cookie configuration, and environment setup.

Run this script to:
1. Check Flask session configuration
2. Test session cookie settings
3. Verify OAuth environment variables
4. Check URL scheme configuration
5. Test state parameter generation and validation

Usage:
    python oauth_state_diagnostic.py
"""

import os
import sys
from dotenv import load_dotenv
import secrets
from datetime import datetime, timedelta

def load_environment():
    """Load environment variables and print status."""
    print("🔧 OAUTH STATE PARAMETER DIAGNOSTIC")
    print("=" * 50)
    
    # Load environment variables
    env_loaded = load_dotenv()
    print(f"Environment file loaded: {'✅' if env_loaded else '❌'}")
    
    return {
        'GOOGLE_CLIENT_ID': os.getenv('GOOGLE_CLIENT_ID', ''),
        'GOOGLE_CLIENT_SECRET': os.getenv('GOOGLE_CLIENT_SECRET', ''),
        'SECRET_KEY': os.getenv('SECRET_KEY', ''),
        'FLASK_ENV': os.getenv('FLASK_ENV', 'development'),
        'PREFERRED_URL_SCHEME': os.getenv('PREFERRED_URL_SCHEME', ''),
        'SESSION_COOKIE_SAMESITE': os.getenv('SESSION_COOKIE_SAMESITE', ''),
        'SESSION_COOKIE_SECURE': os.getenv('SESSION_COOKIE_SECURE', ''),
    }

def check_oauth_credentials(env_vars):
    """Check OAuth credential configuration."""
    print("\n📋 OAUTH CREDENTIALS CHECK")
    print("-" * 30)
    
    client_id = env_vars['GOOGLE_CLIENT_ID'].strip()
    client_secret = env_vars['GOOGLE_CLIENT_SECRET'].strip()
    
    if client_id:
        print(f"✅ GOOGLE_CLIENT_ID: ...{client_id[-12:]}")
        if client_id.endswith('.apps.googleusercontent.com'):
            print("   ✅ Client ID format is correct")
        else:
            print("   ⚠️  Client ID format may be incorrect (should end with .apps.googleusercontent.com)")
    else:
        print("❌ GOOGLE_CLIENT_ID: Not set")
        return False
    
    if client_secret:
        print(f"✅ GOOGLE_CLIENT_SECRET: {'*' * len(client_secret[:8])}...")
    else:
        print("❌ GOOGLE_CLIENT_SECRET: Not set")
        return False
    
    return True

def check_session_configuration(env_vars):
    """Check Flask session configuration for OAuth state handling."""
    print("\n🍪 SESSION CONFIGURATION CHECK")
    print("-" * 35)
    
    secret_key = env_vars['SECRET_KEY'].strip()
    if secret_key and secret_key != 'dev-secret':
        print(f"✅ SECRET_KEY: Set (length: {len(secret_key)})")
        if len(secret_key) < 32:
            print("   ⚠️  Secret key is short, consider using a longer key for production")
    else:
        print("⚠️  SECRET_KEY: Using default/weak secret key")
    
    flask_env = env_vars['FLASK_ENV']
    print(f"🌍 Environment: {flask_env}")
    
    # Check URL scheme configuration
    preferred_scheme = env_vars['PREFERRED_URL_SCHEME']
    expected_scheme = 'https' if flask_env == 'production' else 'http'
    
    if preferred_scheme:
        print(f"🔗 URL Scheme: {preferred_scheme}")
        if preferred_scheme != expected_scheme:
            print(f"   ⚠️  Expected {expected_scheme} for {flask_env} environment")
    else:
        print(f"🔗 URL Scheme: Auto-detected ({expected_scheme})")
    
    # Check cookie settings
    cookie_samesite = env_vars['SESSION_COOKIE_SAMESITE'] or 'Lax'
    cookie_secure = env_vars['SESSION_COOKIE_SECURE']
    expected_secure = 'True' if flask_env == 'production' else 'False'
    
    print(f"🍪 Cookie SameSite: {cookie_samesite}")
    print(f"🔒 Cookie Secure: {cookie_secure or expected_secure}")
    
    if flask_env == 'production':
        if cookie_secure != 'True':
            print("   ⚠️  Cookies should be secure in production")
        if cookie_samesite not in ['Lax', 'Strict', 'None']:
            print(f"   ⚠️  Unusual SameSite value: {cookie_samesite}")

def test_state_parameter_generation():
    """Test OAuth state parameter generation and validation logic."""
    print("\n🎲 STATE PARAMETER GENERATION TEST")
    print("-" * 40)
    
    # Test state parameter generation (similar to what your app does)
    try:
        state1 = secrets.token_urlsafe(32)
        state2 = secrets.token_urlsafe(32)
        
        print(f"✅ State generation working")
        print(f"   Sample state 1: {state1[:8]}...{state1[-8:]}")
        print(f"   Sample state 2: {state2[:8]}...{state2[-8:]}")
        print(f"   States are unique: {'✅' if state1 != state2 else '❌'}")
        print(f"   State length: {len(state1)} characters")
        
        return True
    except Exception as e:
        print(f"❌ State generation failed: {e}")
        return False

def check_flask_app_configuration():
    """Check Flask app configuration that affects OAuth."""
    print("\n🏗️ FLASK APP CONFIGURATION")
    print("-" * 30)
    
    try:
        # Import and check Flask app configuration
        from config import Config
        config = Config()
        
        print(f"✅ Config loaded successfully")
        print(f"   URL Scheme: {getattr(config, 'PREFERRED_URL_SCHEME', 'Not set')}")
        print(f"   Cookie Secure: {getattr(config, 'SESSION_COOKIE_SECURE', 'Not set')}")
        print(f"   Cookie SameSite: {getattr(config, 'SESSION_COOKIE_SAMESITE', 'Not set')}")
        print(f"   Cookie HTTPOnly: {getattr(config, 'SESSION_COOKIE_HTTPONLY', 'Not set')}")
        print(f"   Session Max Age: {getattr(config, 'SESSION_COOKIE_MAX_AGE', 'Not set')}")
        
        # Check if OAuth credentials are accessible through config
        google_client_id = getattr(config, 'GOOGLE_CLIENT_ID', '')
        if google_client_id:
            print(f"   ✅ OAuth credentials accessible through config")
        else:
            print(f"   ⚠️  OAuth credentials not accessible through config")
        
        return True
    except Exception as e:
        print(f"❌ Flask config check failed: {e}")
        return False

def test_session_simulation():
    """Simulate session handling for OAuth state."""
    print("\n🔄 SESSION SIMULATION TEST")
    print("-" * 30)
    
    try:
        # Simulate what Flask session would do
        mock_session = {}
        
        # Generate and "store" state
        state = secrets.token_urlsafe(32)
        mock_session['oauth_state'] = state
        print(f"✅ State stored in mock session: {state[:8]}...{state[-8:]}")
        
        # Simulate retrieval
        retrieved_state = mock_session.get('oauth_state')
        if retrieved_state == state:
            print("✅ State retrieval successful")
            print("✅ State validation would pass")
        else:
            print("❌ State retrieval failed")
        
        # Clean up
        if 'oauth_state' in mock_session:
            del mock_session['oauth_state']
            print("✅ State cleanup successful")
        
        return True
    except Exception as e:
        print(f"❌ Session simulation failed: {e}")
        return False

def provide_recommendations(env_vars):
    """Provide recommendations based on findings."""
    print("\n💡 RECOMMENDATIONS")
    print("-" * 20)
    
    flask_env = env_vars['FLASK_ENV']
    
    recommendations = []
    
    # Check secret key
    secret_key = env_vars['SECRET_KEY'].strip()
    if not secret_key or secret_key == 'dev-secret':
        recommendations.append("🔑 Set a strong SECRET_KEY in your environment variables")
    
    # Check production settings
    if flask_env == 'production':
        if env_vars['SESSION_COOKIE_SECURE'] != 'True':
            recommendations.append("🔒 Set SESSION_COOKIE_SECURE=True for production")
        if not env_vars['PREFERRED_URL_SCHEME'] or env_vars['PREFERRED_URL_SCHEME'] != 'https':
            recommendations.append("🔗 Set PREFERRED_URL_SCHEME=https for production")
    
    # OAuth specific recommendations
    recommendations.extend([
        "🚀 Clear browser cache and cookies before testing",
        "🌐 Ensure your Google Cloud Console OAuth settings include the correct redirect URIs",
        "📱 Test OAuth in an incognito/private browser window",
        "🔄 Check that your Flask session configuration allows proper state storage",
        "⏱️ Verify that OAuth requests complete within the session timeout period"
    ])
    
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")

def check_common_oauth_issues():
    """Check for common OAuth configuration issues."""
    print("\n🔍 COMMON OAUTH ISSUES CHECK")
    print("-" * 35)
    
    issues_found = []
    
    # Check if running on localhost vs 0.0.0.0
    print("🖥️ Host configuration:")
    print("   - Local development should use 127.0.0.1 or localhost")
    print("   - Production should use 0.0.0.0 to accept external connections")
    
    # Check redirect URI patterns
    print("\n🔄 Redirect URI patterns:")
    print("   - Development: http://localhost:5001/login/google/authorize")
    print("   - Development (alt): http://127.0.0.1:5001/login/google/authorize")
    print("   - Production: https://your-domain.com/login/google/authorize")
    
    # Check browser security
    print("\n🌐 Browser security considerations:")
    print("   - Some browsers block OAuth on localhost with HTTPS")
    print("   - Mixed content (HTTP OAuth on HTTPS site) will fail")
    print("   - Third-party cookies must be enabled")
    
    return len(issues_found) == 0

def main():
    """Run the complete OAuth state diagnostic."""
    print("Starting OAuth State Parameter Diagnostic...\n")
    
    # Load environment
    env_vars = load_environment()
    
    # Run all checks
    checks = [
        ("OAuth Credentials", lambda: check_oauth_credentials(env_vars)),
        ("Session Configuration", lambda: check_session_configuration(env_vars)),
        ("State Parameter Generation", test_state_parameter_generation),
        ("Flask App Configuration", check_flask_app_configuration),
        ("Session Simulation", test_session_simulation),
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        try:
            if check_func():
                passed += 1
        except Exception as e:
            print(f"❌ {name} check failed with error: {e}")
    
    # Additional checks
    check_common_oauth_issues()
    
    # Provide recommendations
    provide_recommendations(env_vars)
    
    # Summary
    print(f"\n📊 DIAGNOSTIC SUMMARY")
    print("-" * 25)
    print(f"Checks passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All checks passed! OAuth state handling should work correctly.")
        print("If you're still experiencing issues, the problem may be:")
        print("   - Missing redirect URI in Google Cloud Console")
        print("   - Browser cookie/session issues")
        print("   - Network or proxy configuration")
    else:
        print(f"⚠️ {total - passed} checks failed. Please address the issues above.")
    
    print("\n🔧 NEXT STEPS:")
    print("1. Address any failed checks above")
    print("2. Test the OAuth flow in your application")
    print("3. Check browser developer console for errors")
    print("4. Review server logs during OAuth attempts")

if __name__ == "__main__":
    main()

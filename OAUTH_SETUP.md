# OAuth Authentication Setup Guide

This guide will help you set up Google and Apple OAuth authentication for the Financial AI application.

## Prerequisites

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Google OAuth Setup

### 1. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable required APIs:
   - "Google Identity Services" (OAuth 2.0)

### 2. Configure OAuth Consent Screen

1. Go to "APIs & Services" > "OAuth consent screen"
2. Choose "External" user type
3. Fill in the required information:
   - App name: "Financial AI"
   - User support email: Your email
   - Developer contact information: Your email
4. Add scopes: `openid`, `email`, `profile`
5. Add test users if needed

### 3. Create OAuth Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Choose "Web application"
4. Add authorized redirect URIs:
   - `http://localhost:5001/login/google/authorize` (development)
   - `https://yourdomain.com/login/google/authorize` (production)
   Also add the authorized JavaScript origins if prompted (your site origins).
5. Copy the Client ID and Client Secret

### 4. Configure Environment Variables

Add these to your `.env` file (or deployment environment):
```
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

If you deploy behind a proxy (Render, Heroku), set `OAUTHLIB_INSECURE_TRANSPORT=0` in production and ensure your app knows it's behind HTTPS (use `X-Forwarded-Proto` handling or platform settings).

## Apple OAuth Setup

### 1. Create an Apple Developer Account

1. Go to [Apple Developer](https://developer.apple.com/)
2. Sign in with your Apple ID
3. Enroll in the Apple Developer Program (if needed)

### 2. Configure Sign in with Apple

1. Go to "Certificates, Identifiers & Profiles"
2. Create a new App ID or select existing one
3. Enable "Sign In with Apple"
4. Configure the domain and redirect URLs

### 3. Create a Service ID

1. Go to "Identifiers" > "Service IDs"
2. Create a new Service ID
3. Enable "Sign In with Apple"
4. Configure the domain and redirect URLs

### 4. Configure Environment Variables

Add these to your `.env` file:
```
APPLE_CLIENT_ID=your-apple-client-id
APPLE_CLIENT_SECRET=your-apple-client-secret
```

## Testing OAuth

1. Start the application:
```bash
python app.py
```

2. Go to the login page
3. Click "Continue with Google" or "Continue with Apple"
4. Complete the OAuth flow

## Troubleshooting

### Common Issues

1. **Redirect URI mismatch**: Make sure the redirect URI in your OAuth provider matches exactly what's configured in the app
2. **Missing environment variables**: Ensure all OAuth credentials are properly set in your `.env` file
3. **Database migration**: If you added OAuth fields to the User model, you may need to recreate the database:
   ```bash
   rm instance/app.db
   python app.py
   ```

### Error Messages

- "Google login failed": Check your Google OAuth credentials and redirect URIs
- "Apple login failed": Check your Apple OAuth credentials and configuration
- "Email not provided": Apple may not provide email on subsequent logins

## Security Notes

1. Never commit your `.env` file to version control
2. Use strong, unique Client Secrets
3. Regularly rotate your OAuth credentials
4. Monitor OAuth usage in your provider's dashboard

## Production Deployment

For production deployment:

1. Update redirect URIs to use your production domain
2. Use HTTPS for all OAuth callbacks
3. Set appropriate security headers
4. Monitor OAuth usage and errors
5. Implement proper error handling and logging

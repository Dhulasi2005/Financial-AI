# ⚡ Quick Deploy Guide

## 🚀 **Fastest Way to Deploy (5 minutes)**

### **Step 1: Prepare Your Code**
```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit"

# Push to GitHub
git remote add origin https://github.com/yourusername/financial-ai.git
git push -u origin main
```

### **Step 2: Deploy to Railway (Recommended)**

1. **Go to [Railway.app](https://railway.app)**
2. **Sign up with GitHub**
3. **Click "New Project" → "Deploy from GitHub repo"**
4. **Select your repository**
5. **Add Environment Variables:**
   ```
   SECRET_KEY=your-secret-key-here
   NEWSAPI_KEY=your-newsapi-key
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   FLASK_ENV=production
   ```
6. **Done!** Railway will auto-deploy

### **Step 3: Update OAuth (if using Google/Apple login)**

1. **Go to Google Cloud Console**
2. **Add your Railway URL to redirect URIs:**
   ```
   https://your-app-name.railway.app/login/google/authorize
   ```

## 🎯 **Alternative: Render (Better Free Tier)**

1. **Go to [Render.com](https://render.com)**
2. **Sign up with GitHub**
3. **Click "New +" → "Web Service"**
4. **Connect your repository**
5. **Configure:**
   - **Name:** `financial-ai`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. **Add environment variables**
7. **Click "Create Web Service"**

## 🔧 **Environment Variables Needed**

Make sure you have these in your hosting platform:

```bash
# Required
SECRET_KEY=your-very-secure-secret-key
NEWSAPI_KEY=your-newsapi-key

# Optional (for OAuth)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
APPLE_CLIENT_ID=your-apple-client-id
APPLE_CLIENT_SECRET=your-apple-client-secret

# Production
FLASK_ENV=production
```

## 🎉 **That's It!**

Your Financial AI app will be live at:
- **Railway:** `https://your-app-name.railway.app`
- **Render:** `https://your-app-name.onrender.com`

## 🆘 **Need Help?**

- **Check logs** in your hosting platform dashboard
- **Verify environment variables** are set correctly
- **See full guide:** `DEPLOYMENT_GUIDE.md`
- **Run deployment script:** `./deploy.sh`

**Happy deploying! 🚀**

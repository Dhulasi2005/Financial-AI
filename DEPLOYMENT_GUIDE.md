# 🚀 Financial AI Deployment Guide

This guide covers multiple deployment options for your Financial AI application, from simple hosting to production-ready solutions.

## 📋 **Prerequisites**

Before deploying, ensure you have:
- ✅ All dependencies installed (`pip install -r requirements.txt`)
- ✅ Environment variables configured (`.env` file)
- ✅ Database working locally
- ✅ OAuth credentials set up (if using Google/Apple login)

## 🎯 **Deployment Options**

### **Option 1: Railway (Recommended for Beginners)**

**Railway** is perfect for beginners - simple, fast, and free tier available.

#### **Steps:**
1. **Create Railway Account:**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Connect Your Repository:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your GitHub repository

3. **Configure Environment Variables:**
   - Go to your project settings
   - Add these variables:
   ```
   SECRET_KEY=your-secret-key-here
   NEWSAPI_KEY=your-newsapi-key
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   FLASK_ENV=production
   ```

4. **Deploy:**
   - Railway will automatically detect Flask
   - Deploy happens automatically on git push

**Pros:** ✅ Free tier, ✅ Auto-deploy, ✅ Easy setup  
**Cons:** ❌ Limited free tier, ❌ No custom domain on free plan

---

### **Option 2: Render (Great Free Tier)**

**Render** offers a generous free tier with custom domains.

#### **Steps:**
1. **Create Render Account:**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure Service:**
   ```
   Name: financial-ai
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

4. **Add Environment Variables:**
   - Go to "Environment" tab
   - Add all your `.env` variables

5. **Deploy:**
   - Click "Create Web Service"
   - Render will build and deploy automatically

**Pros:** ✅ Generous free tier, ✅ Custom domains, ✅ Auto-deploy  
**Cons:** ❌ Sleeps after inactivity (free tier)

---

### **Option 3: Heroku (Classic Choice)**

**Heroku** is reliable but requires credit card for free tier.

#### **Steps:**
1. **Install Heroku CLI:**
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Or download from heroku.com
   ```

2. **Create Heroku App:**
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Add Buildpacks:**
   ```bash
   heroku buildpacks:set heroku/python
   ```

4. **Configure Environment:**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set NEWSAPI_KEY=your-newsapi-key
   heroku config:set GOOGLE_CLIENT_ID=your-google-client-id
   heroku config:set GOOGLE_CLIENT_SECRET=your-google-client-secret
   heroku config:set FLASK_ENV=production
   ```

5. **Deploy:**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

**Pros:** ✅ Reliable, ✅ Good documentation, ✅ Add-ons available  
**Cons:** ❌ Requires credit card, ❌ No free tier anymore

---

### **Option 4: DigitalOcean App Platform**

**DigitalOcean** offers a simple app platform with good performance.

#### **Steps:**
1. **Create DigitalOcean Account:**
   - Go to [digitalocean.com](https://digitalocean.com)
   - Sign up (requires credit card)

2. **Create App:**
   - Go to "Apps" → "Create App"
   - Connect your GitHub repository

3. **Configure App:**
   ```
   Source: GitHub repository
   Branch: main
   Build Command: pip install -r requirements.txt
   Run Command: gunicorn app:app
   ```

4. **Add Environment Variables:**
   - Add all your `.env` variables in the app settings

5. **Deploy:**
   - Click "Create Resources"
   - DigitalOcean will build and deploy

**Pros:** ✅ Good performance, ✅ Custom domains, ✅ SSL included  
**Cons:** ❌ Requires credit card, ❌ No free tier

---

### **Option 5: VPS (Advanced Users)**

For full control, deploy on a VPS like DigitalOcean Droplet or AWS EC2.

#### **Steps:**
1. **Create VPS:**
   - Choose Ubuntu 20.04 or newer
   - Minimum 1GB RAM, 1 CPU

2. **Connect and Setup:**
   ```bash
   ssh root@your-server-ip
   
   # Update system
   apt update && apt upgrade -y
   
   # Install Python and dependencies
   apt install python3 python3-pip python3-venv nginx -y
   ```

3. **Deploy Application:**
   ```bash
   # Clone repository
   git clone https://github.com/yourusername/financial-ai.git
   cd financial-ai
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

4. **Configure Gunicorn:**
   ```bash
   # Create gunicorn service
   sudo nano /etc/systemd/system/financial-ai.service
   ```
   
   Add this content:
   ```ini
   [Unit]
   Description=Financial AI Gunicorn
   After=network.target
   
   [Service]
   User=root
   WorkingDirectory=/root/financial-ai
   Environment="PATH=/root/financial-ai/venv/bin"
   ExecStart=/root/financial-ai/venv/bin/gunicorn --workers 3 --bind unix:financial-ai.sock -m 007 app:app
   
   [Install]
   WantedBy=multi-user.target
   ```

5. **Configure Nginx:**
   ```bash
   sudo nano /etc/nginx/sites-available/financial-ai
   ```
   
   Add this content:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
   
       location / {
           include proxy_params;
           proxy_pass http://unix:/root/financial-ai/financial-ai.sock;
       }
   }
   ```

6. **Enable and Start:**
   ```bash
   sudo ln -s /etc/nginx/sites-available/financial-ai /etc/nginx/sites-enabled
   sudo systemctl start financial-ai
   sudo systemctl enable financial-ai
   sudo systemctl restart nginx
   ```

**Pros:** ✅ Full control, ✅ Best performance, ✅ Customizable  
**Cons:** ❌ Complex setup, ❌ Requires server management

---

## 🔧 **Production Configuration**

### **1. Update Environment Variables**

For production, update your environment variables:

```bash
# Production settings
FLASK_ENV=production
SECRET_KEY=your-very-secure-secret-key
DATABASE_URL=your-production-database-url

# OAuth (update redirect URIs)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
APPLE_CLIENT_ID=your-apple-client-id
APPLE_CLIENT_SECRET=your-apple-client-secret
```

### **2. Update OAuth Redirect URIs**

In your Google/Apple OAuth settings, add your production domain:
- `https://your-domain.com/login/google/authorize`
- `https://your-domain.com/login/apple/authorize`

### **3. Database Setup**

For production, consider using a proper database:

#### **SQLite (Simple):**
```python
# Already configured in config.py
SQLALCHEMY_DATABASE_URI = "sqlite:///instance/app.db"
```

#### **PostgreSQL (Recommended):**
```python
# Update config.py
SQLALCHEMY_DATABASE_URI = "postgresql://user:password@host:port/database"
```

### **4. Add Production Dependencies**

Update `requirements.txt`:
```
# Add these for production
gunicorn==21.2.0
psycopg2-binary==2.9.9  # For PostgreSQL
```

### **5. Create Procfile (for Heroku/Railway)**

Create `Procfile` in your root directory:
```
web: gunicorn app:app
```

---

## 🛡️ **Security Checklist**

Before going live:

- ✅ **Environment Variables:** All secrets in environment, not in code
- ✅ **HTTPS:** SSL certificate configured
- ✅ **OAuth:** Production redirect URIs set
- ✅ **Database:** Proper database with backups
- ✅ **Rate Limiting:** Implement rate limiting for API endpoints
- ✅ **CORS:** Configure CORS for your domain
- ✅ **Logging:** Set up proper logging
- ✅ **Monitoring:** Add health checks

---

## 🚀 **Quick Deploy Commands**

### **Railway (Easiest):**
```bash
# Just push to GitHub, Railway auto-deploys
git add .
git commit -m "Deploy to Railway"
git push origin main
```

### **Render:**
```bash
# Connect GitHub repo, Render handles the rest
# Just configure environment variables in dashboard
```

### **Heroku:**
```bash
heroku create your-app-name
heroku config:set SECRET_KEY=your-secret
git push heroku main
```

---

## 📊 **Performance Optimization**

### **1. Database Optimization:**
```python
# Add to config.py
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}
```

### **2. Caching:**
```python
# Add Redis for caching
from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'redis'})
```

### **3. Static Files:**
```python
# Use CDN for static files
app.static_folder = 'static'
app.static_url_path = '/static'
```

---

## 🔍 **Monitoring & Maintenance**

### **Health Check Endpoint:**
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.utcnow()}
```

### **Logging:**
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### **Error Tracking:**
Consider adding Sentry for error tracking:
```python
import sentry_sdk
sentry_sdk.init(dsn="your-sentry-dsn")
```

---

## 🎯 **Recommended Deployment Path**

### **For Beginners:**
1. **Railway** → Easy setup, good free tier
2. **Render** → Better free tier, custom domains

### **For Production:**
1. **DigitalOcean App Platform** → Good performance, reasonable pricing
2. **VPS** → Full control, best performance

### **For Enterprise:**
1. **AWS/GCP/Azure** → Scalable, enterprise features
2. **Kubernetes** → Container orchestration

---

## 🆘 **Troubleshooting**

### **Common Issues:**

1. **Build Fails:**
   - Check `requirements.txt` is up to date
   - Verify Python version compatibility

2. **Environment Variables:**
   - Ensure all variables are set in hosting platform
   - Check variable names match exactly

3. **Database Issues:**
   - Verify database connection string
   - Check database permissions

4. **OAuth Not Working:**
   - Update redirect URIs in OAuth providers
   - Check domain matches exactly

5. **Static Files Not Loading:**
   - Verify static folder path
   - Check file permissions

---

## 📞 **Support**

If you encounter issues:

1. **Check Logs:** Most platforms provide logs in dashboard
2. **Environment Variables:** Verify all are set correctly
3. **Documentation:** Check platform-specific docs
4. **Community:** Ask in platform forums/communities

**Happy Deploying! 🚀**

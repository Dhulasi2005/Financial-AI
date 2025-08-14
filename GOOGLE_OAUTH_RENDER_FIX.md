# 🔧 Fix "Continue with Google" Button on Render

## 🚨 Critical Issue Found in Your Screenshot

Your Google Cloud Console is missing **Authorized JavaScript Origins** - this is why OAuth fails!

## ✅ Immediate Fix

### 1. Google Cloud Console - Add JavaScript Origins

**Scroll up in your screenshot to "Authorized JavaScript origins"**
**Click "+ ADD URI" and add:**

```
http://localhost:5001
http://localhost:5000  
https://financial-ai-6z0s.onrender.com
```

### 2. Google Cloud Console - Add Development Redirect URIs

**Add these to your existing redirect URIs:**

```
http://localhost:5001/login/google/authorize
http://localhost:5000/login/google/authorize
```

(Keep your existing production URI too)

### 3. Render Environment Variables

In your Render dashboard, add these environment variables:

```
FLASK_ENV=production
PREFERRED_URL_SCHEME=https  
OAUTHLIB_INSECURE_TRANSPORT=0
```

Plus copy your existing credentials from .env file.

## 🎯 Why This Fixes It

- **Missing JavaScript Origins** = CORS blocks OAuth requests
- **HTTP vs HTTPS mismatch** = OAuth security validation fails  
- **Missing environment vars** = Production config incorrect

## 🧪 Test After Fix

Visit: `https://financial-ai-6z0s.onrender.com/login`
Click "Continue with Google" - should work now!

## ⚡ The Key Issue

Your screenshot shows empty "Authorized JavaScript origins" section. 
**JavaScript origins are required for OAuth to work from web browsers.**

Add the 3 origins above and your OAuth will work! 🎉

---

## 🚨 **Additional Fix for Private IP Error (Error 400)**

If you see "device_id and device_name are required for private IP" error:

### **Quick Fix:**
1. **Use localhost instead**: Access `http://localhost:5001/login` instead of `http://192.168.x.x:5001/login`

### **Or add your IP to Google Console:**
If you need to use IP address (like `192.168.137.6`), add these to Google Console:

**JavaScript Origins:**
```
http://192.168.137.6:5001
```

**Redirect URIs:**
```
http://192.168.137.6:5001/login/google/authorize
```

### **Why This Happens:**
Google OAuth restricts private IP addresses for security. Using `localhost` bypasses this restriction.

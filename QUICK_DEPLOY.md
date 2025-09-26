# 🚀 Railway Deployment Steps

## Quick Start (5 minutes)

### Step 1: Go to Railway
1. Visit: https://railway.app
2. Click **"Start a New Project"**
3. Click **"Deploy from GitHub repo"**

### Step 2: Connect GitHub
1. Click **"Connect GitHub"** 
2. Authorize Railway to access your repositories
3. Select: **`2024021129-crypto/New-civic-text`**

### Step 3: Deploy
1. Railway will automatically detect it's a Python app
2. Click **"Deploy"** 
3. Wait 2-3 minutes for deployment

### Step 4: Test Your API
1. Copy your Railway app URL (e.g., `https://your-app.railway.app`)
2. Test the health endpoint:
   ```
   https://your-app.railway.app/health
   ```
3. Test prediction:
   ```bash
   curl -X POST https://your-app.railway.app/predict \
     -H "Content-Type: application/json" \
     -d '{"text": "Street light is broken"}'
   ```

## 🎯 Expected Results

✅ **Health Check**: Should return `{"status": "healthy"}`
✅ **Prediction**: Should return classification with confidence score
✅ **Model**: Will automatically use fallback model if custom model not available

## 🔧 Custom Domain (Optional)
1. In Railway dashboard, go to **Settings**
2. Click **"Domains"**
3. Add your custom domain

---

**That's it! Your civic text classifier is now live on Railway! 🎉**

URL Format: `https://[your-project-name].railway.app`
# Railway Deployment Guide - Civic Text Classifier API

## 🚀 Quick Deploy to Railway

### Method 1: Deploy from GitHub (Recommended)

1. **Push to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Add Railway deployment files"
   git push origin main
   ```

2. **Deploy on Railway**:
   - Go to [Railway.app](https://railway.app)
   - Click "Deploy from GitHub repo"
   - Connect your GitHub account
   - Select the repository: `2024021129-crypto/New-civic-text`
   - Railway will automatically detect it's a Python app and deploy

3. **Environment Variables** (Optional):
   - No environment variables needed - PORT is automatically set by Railway

### Method 2: Deploy with Railway CLI

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and Deploy**:
   ```bash
   railway login
   railway init
   railway up
   ```

## 📋 Railway Configuration Files

### railway.json
- Configures the build and deployment settings
- Sets health check endpoint to `/health`

### nixpacks.toml
- Specifies Python 3.9 runtime
- Defines build and start commands

### runtime.txt
- Ensures Python 3.9.18 is used

## 🔧 API Endpoints

Once deployed, your API will be available at: `https://your-app-name.railway.app`

### Health Check
```bash
curl https://your-app-name.railway.app/health
```

### Text Classification
```bash
curl -X POST https://your-app-name.railway.app/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "The streetlight on main street is broken"}'
```

### Home Page
```bash
curl https://your-app-name.railway.app/
```

## 🎯 Expected Response Examples

### Health Check Response:
```json
{
  "status": "healthy",
  "model_status": "loaded",
  "model_loaded": true,
  "message": "Civic Text Classifier API is running"
}
```

### Prediction Response:
```json
{
  "text": "The streetlight on main street is broken",
  "predicted_class": 0,
  "predicted_label": "streetlight",
  "confidence": 0.95,
  "model_type": "custom_civic_model"
}
```

## 🔍 Model Behavior

1. **Primary Model**: Custom trained DistilBERT for civic issues (streetlight, garbage, potholes)
2. **Fallback Model**: If custom model fails, uses DistilBERT sentiment model
3. **Classification Categories**:
   - `0`: streetlight issues
   - `1`: garbage/waste issues  
   - `2`: potholes/road issues

## 🚨 Troubleshooting

### Common Issues:
1. **pip command not found**: 
   - Railway will now use the Dockerfile instead of Nixpacks
   - Alternative: Use the `requirements-railway.txt` with lighter versions
   
2. **Build Fails**: 
   - Check `requirements.txt` for version conflicts
   - Try using `requirements-railway.txt` for lighter dependencies
   
3. **Model Not Loading**: 
   - App will use fallback model automatically
   - Check model files are included in repository
   
4. **Port Issues**: 
   - Railway automatically sets PORT environment variable
   - App defaults to port 8000 if PORT not set

### Build Solutions:
If Nixpacks fails, Railway will automatically use the Dockerfile. You can also:
1. Use `requirements-railway.txt` (lighter versions)
2. Force Dockerfile build by removing `nixpacks.toml`

### Logs:
- View logs in Railway dashboard
- Look for "Model loaded successfully!" message
- Check for any Python/pip installation errors

## 💡 Advantages of Railway vs Render

- ✅ Better handling of large files
- ✅ Faster cold starts
- ✅ Better Python support
- ✅ Automatic HTTPS
- ✅ Built-in monitoring
- ✅ Easy rollbacks

## 🔗 Links

- **Repository**: https://github.com/2024021129-crypto/New-civic-text
- **Railway Platform**: https://railway.app
- **Railway Docs**: https://docs.railway.app

## 📝 Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Railway account created
- [ ] Repository connected to Railway
- [ ] Deployment successful
- [ ] Health check returns 200
- [ ] Prediction endpoint working
- [ ] Model loading properly

---

🎉 **Your civic text classifier API is now live on Railway!**
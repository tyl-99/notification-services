# Railway Deployment Guide

This guide will help you deploy the Notification Service to Railway.

## Prerequisites

1. Railway account (sign up at [railway.app](https://railway.app))
2. GitHub account (optional, for GitHub integration)
3. Firebase service account credentials JSON file

## Step 1: Prepare Your Project

All necessary files are already in place:
- ✅ `Procfile` - Defines how to run the app
- ✅ `requirements.txt` - Python dependencies
- ✅ `railway.json` - Railway configuration
- ✅ `runtime.txt` - Python version

## Step 2: Deploy to Railway

### Option A: Deploy via GitHub (Recommended)

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/notification-services.git
   git push -u origin main
   ```

2. **Connect Railway to GitHub:**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will automatically detect Python and start building

### Option B: Deploy via Railway CLI

1. **Install Railway CLI:**
   ```bash
   npm i -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Initialize and Deploy:**
   ```bash
   railway init
   railway up
   ```

### Option C: Deploy via Railway Dashboard

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Empty Project"
4. Click "Add Service" → "GitHub Repo" or "Empty Service"
5. Upload your project files or connect to GitHub

## Step 3: Configure Environment Variables

In Railway dashboard, go to your service → Variables tab and add:

### Required Variables:

```
FIREBASE_ADMIN_CREDENTIALS_PATH=./my-trader.json
PORT=5001
DEBUG=False
```

### Optional Variables:

```
API_KEY=your-secret-api-key-here
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

### Firebase Credentials

You have two options:

**Option 1: Upload JSON file (Recommended)**
1. In Railway dashboard → Variables
2. Click "Add Variable"
3. Name: `FIREBASE_ADMIN_CREDENTIALS_PATH`
4. Value: `./my-trader.json`
5. Go to "Settings" → "Source" → Upload `my-trader.json` file

**Option 2: Use JSON string**
1. In Railway dashboard → Variables
2. Click "Add Variable"
3. Name: `FIREBASE_ADMIN_CREDENTIALS`
4. Value: Paste the entire JSON content from `my-trader.json` (as a single line)

## Step 4: Verify Deployment

1. Railway will automatically build and deploy your service
2. Check the "Deployments" tab for build logs
3. Once deployed, Railway will provide a URL like: `https://your-app-name.up.railway.app`

## Step 5: Test Your Deployment

### Health Check:
```bash
curl https://your-app-name.up.railway.app/api/health
```

### Test Notification:
```bash
curl -X POST https://your-app-name.up.railway.app/api/send-to-app \
  -H "Content-Type: application/json" \
  -d '{"app_id":"trading-app","title":"Test","body":"Hello from Railway!"}'
```

## Step 6: Configure Custom Domain (Optional)

1. Go to Railway dashboard → Your service → Settings
2. Click "Generate Domain" or "Add Custom Domain"
3. Follow the DNS configuration instructions

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `FIREBASE_ADMIN_CREDENTIALS_PATH` | Yes* | Path to Firebase JSON file | `./my-trader.json` |
| `FIREBASE_ADMIN_CREDENTIALS` | Yes* | Firebase JSON as string | `{"type":"service_account",...}` |
| `PORT` | No | Server port (Railway sets this) | `5001` |
| `DEBUG` | No | Debug mode | `False` |
| `API_KEY` | No | API authentication key | `your-secret-key` |
| `ALLOWED_ORIGINS` | No | CORS allowed origins | `https://app.com` |

*Either `FIREBASE_ADMIN_CREDENTIALS_PATH` or `FIREBASE_ADMIN_CREDENTIALS` is required

## Troubleshooting

### Build Fails
- Check build logs in Railway dashboard
- Ensure `requirements.txt` is correct
- Verify Python version in `runtime.txt`

### Service Won't Start
- Check logs in Railway dashboard
- Verify environment variables are set
- Ensure `Procfile` is correct

### Firebase Errors
- Verify Firebase credentials are uploaded correctly
- Check that Firestore is enabled in Firebase Console
- Ensure Cloud Messaging API is enabled

### Port Issues
- Railway automatically sets `PORT` environment variable
- Don't hardcode port in code (use `os.getenv('PORT', 5001)`)

## Production Checklist

- [ ] Environment variables configured
- [ ] Firebase credentials uploaded
- [ ] API_KEY set (for security)
- [ ] ALLOWED_ORIGINS configured (for CORS)
- [ ] Custom domain configured (optional)
- [ ] Health check endpoint working
- [ ] Test notification sent successfully

## Monitoring

Railway provides:
- Real-time logs
- Deployment history
- Metrics and usage stats
- Error tracking

Access these in the Railway dashboard under your service.

## Cost

Railway offers:
- **Free tier**: $5 credit/month
- **Hobby**: $5/month (after free credit)
- **Pro**: $20/month

Check [railway.app/pricing](https://railway.app/pricing) for current pricing.

## Support

- Railway Docs: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- Railway Twitter: [@railway](https://twitter.com/railway)


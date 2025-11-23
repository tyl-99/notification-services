# Railway Firebase Credentials Setup

## Problem
Railway can't find `my-trader.json` file because it needs to be uploaded to Railway's file system.

## Solution Options

### Option 1: Upload File to Railway (Recommended)

1. **Go to Railway Dashboard:**
   - Open your service
   - Go to **Settings** tab
   - Scroll to **Source** section

2. **Upload the file:**
   - Click **"Add File"** or **"Upload"**
   - Select your `my-trader.json` file
   - Railway will upload it to `/app/my-trader.json`

3. **Set Environment Variable:**
   - Go to **Variables** tab
   - Add: `FIREBASE_ADMIN_CREDENTIALS_PATH=./my-trader.json`
   - Or: `FIREBASE_ADMIN_CREDENTIALS_PATH=/app/my-trader.json`

### Option 2: Use Environment Variable (Easier)

Instead of uploading a file, paste the JSON content as an environment variable:

1. **Open your `my-trader.json` file** and copy ALL its content

2. **In Railway Dashboard → Variables:**
   - Add new variable: `FIREBASE_ADMIN_CREDENTIALS`
   - Paste the ENTIRE JSON content as the value (as a single line)
   - Example:
     ```
     FIREBASE_ADMIN_CREDENTIALS={"type":"service_account","project_id":"my-trader-9e446",...}
     ```

3. **Remove or don't set** `FIREBASE_ADMIN_CREDENTIALS_PATH` variable

The code will automatically use the environment variable if the file doesn't exist.

## Quick Fix Steps

### Using Environment Variable (Fastest):

1. Copy your `my-trader.json` content
2. Railway Dashboard → Variables → Add:
   ```
   FIREBASE_ADMIN_CREDENTIALS=<paste entire JSON here>
   ```
3. Redeploy or restart the service

### Using File Upload:

1. Railway Dashboard → Settings → Source → Upload `my-trader.json`
2. Railway Dashboard → Variables → Set:
   ```
   FIREBASE_ADMIN_CREDENTIALS_PATH=./my-trader.json
   ```
3. Redeploy the service

## Verify It Works

After setting up credentials, check the logs:
- Should see: "Loading Firebase credentials from environment variable" OR
- Should see: "Loading Firebase credentials from file: /app/my-trader.json"
- Should NOT see: "Firebase credentials file not found"

Then test:
```bash
curl https://your-app.up.railway.app/api/health
```


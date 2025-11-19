# Quick Start Guide

## Prerequisites

- Python 3.8 or higher
- Firebase project with Cloud Messaging API enabled
- Firebase service account credentials JSON file

## Setup Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Firebase Credentials

1. Download your Firebase service account credentials JSON file from Firebase Console
2. Save it as `firebase-credentials.json` in the project root directory

### 3. Configure Environment Variables

Copy `env.example` to `.env`:

```bash
# On Windows PowerShell
Copy-Item env.example .env

# On Linux/Mac
cp env.example .env
```

Edit `.env` and update the Firebase credentials path if needed:

```env
FIREBASE_ADMIN_CREDENTIALS_PATH=./firebase-credentials.json
PORT=6000
DEBUG=False
```

### 4. Run the Service

```bash
python app.py
```

The service will start on `http://localhost:6000`

### 5. Test the Service

Open a new terminal and test the health endpoint:

```bash
# Using curl
curl http://localhost:6000/api/health

# Using PowerShell
Invoke-RestMethod -Uri http://localhost:6000/api/health
```

You should see:

```json
{
  "status": "healthy",
  "service": "notification-service",
  "version": "1.0.0"
}
```

## Next Steps

1. **Register a device token** from your PWA frontend
2. **Send notifications** using the `/api/send-to-app` endpoint
3. **Configure app-specific settings** in `app_configs.py`

See `README.md` for detailed API documentation and usage examples.


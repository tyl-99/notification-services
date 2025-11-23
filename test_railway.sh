#!/bin/bash

# Railway Test Script
# Your Railway URL
RAILWAY_URL="https://web-production-dbb3b.up.railway.app"

echo "=========================================="
echo "Testing Railway Notification Service"
echo "URL: $RAILWAY_URL"
echo "=========================================="
echo ""

# Test 1: Health Check
echo "1. Testing Health Check..."
HEALTH_RESPONSE=$(curl -s "$RAILWAY_URL/api/health")
echo "Response: $HEALTH_RESPONSE"
echo ""

# Test 2: Send to App
echo "2. Testing Send to App..."
SEND_RESPONSE=$(curl -s -X POST "$RAILWAY_URL/api/send-to-app" \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "trading-app",
    "title": "🚀 Test from Railway",
    "body": "This is a test notification from Railway deployment",
    "data": {
      "test": "true",
      "source": "railway"
    }
  }')
echo "Response: $SEND_RESPONSE"
echo ""

echo "=========================================="
echo "Tests completed!"
echo "=========================================="


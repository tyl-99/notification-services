# Railway Test Script for PowerShell
# Your Railway URL
$RAILWAY_URL = "https://web-production-dbb3b.up.railway.app"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Testing Railway Notification Service" -ForegroundColor Cyan
Write-Host "URL: $RAILWAY_URL" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "1. Testing Health Check..." -ForegroundColor Yellow
try {
    $healthResponse = Invoke-RestMethod -Uri "$RAILWAY_URL/api/health" -Method GET
    Write-Host "✅ Health Check Passed!" -ForegroundColor Green
    Write-Host "Response: $($healthResponse | ConvertTo-Json)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Health Check Failed: $_" -ForegroundColor Red
}
Write-Host ""

# Test 2: Send to App
Write-Host "2. Testing Send to App..." -ForegroundColor Yellow
try {
    $body = @{
        app_id = "trading-app"
        title = "🚀 Test from Railway"
        body = "This is a test notification from Railway deployment"
        data = @{
            test = "true"
            source = "railway"
        }
    } | ConvertTo-Json

    $sendResponse = Invoke-RestMethod -Uri "$RAILWAY_URL/api/send-to-app" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body

    Write-Host "✅ Send to App Succeeded!" -ForegroundColor Green
    Write-Host "Response: $($sendResponse | ConvertTo-Json)" -ForegroundColor Gray
    Write-Host "Sent to: $($sendResponse.sent_to) device(s)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Send to App Failed: $_" -ForegroundColor Red
    Write-Host "Error Details: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Tests completed!" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan


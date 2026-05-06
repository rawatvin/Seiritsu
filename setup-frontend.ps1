# Task Intelligence - Frontend Setup Script

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Task Intelligence - Frontend Setup" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

$frontendPath = Join-Path $PSScriptRoot "frontend"

# Check if frontend folder exists
if (-not (Test-Path $frontendPath)) {
    Write-Host "❌ Frontend folder not found at: $frontendPath" -ForegroundColor Red
    exit 1
}

Set-Location $frontendPath
Write-Host "📁 Working directory: $frontendPath" -ForegroundColor Green
Write-Host ""

# Step 1: Install Node.js dependencies
Write-Host "Step 1: Installing Node.js dependencies..." -ForegroundColor Yellow
Write-Host "   This may take a few minutes..." -ForegroundColor Gray

npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "   ❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 2: Setup environment file
Write-Host "Step 2: Setting up environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "   ⚠️  .env file already exists, skipping..." -ForegroundColor Yellow
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "   ✅ Created .env file (defaults should work)" -ForegroundColor Green
}
Write-Host ""

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Frontend Setup Complete!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Ensure backend is running first" -ForegroundColor White
Write-Host "2. Start frontend: .\run-frontend.ps1" -ForegroundColor White
Write-Host ""

Set-Location $PSScriptRoot

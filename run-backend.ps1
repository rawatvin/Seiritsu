# Task Intelligence - Run Backend Server

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Starting Task Intelligence Backend Server" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

$backendPath = Join-Path $PSScriptRoot "backend"
Set-Location $backendPath

# Activate virtual environment
$activateScript = "venv\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & $activateScript
} else {
    Write-Host "❌ Virtual environment not found. Run setup-backend.ps1 first" -ForegroundColor Red
    exit 1
}

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found. Run setup-backend.ps1 first" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🚀 Starting FastAPI server..." -ForegroundColor Green
Write-Host "   API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "   Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Start uvicorn
uvicorn app.main:app --reload --port 8000

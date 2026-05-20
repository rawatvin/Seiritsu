# Task Intelligence - Run Frontend Server

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Starting Task Intelligence Frontend Server" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

$frontendPath = Join-Path $PSScriptRoot "frontend"
Set-Location $frontendPath

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "❌ node_modules not found. Run setup-frontend.ps1 first" -ForegroundColor Red
    exit 1
}

Write-Host "🚀 Starting Vite development server..." -ForegroundColor Green
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Start npm dev server
npm run dev

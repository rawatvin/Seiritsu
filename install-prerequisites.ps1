# Task Intelligence - Prerequisites Installation Script
# This script helps you install all required software

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Task Intelligence - Prerequisites Installer" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "⚠️  This script should be run as Administrator for best results." -ForegroundColor Yellow
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host ""
}

# Function to check if a command exists
function Test-Command($command) {
    try {
        if (Get-Command $command -ErrorAction Stop) {
            return $true
        }
    }
    catch {
        return $false
    }
}

Write-Host "Checking installed software..." -ForegroundColor Green
Write-Host ""

# Check Python
Write-Host "1. Python 3.11+" -ForegroundColor Yellow
if (Test-Command python) {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✅ Found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "   ❌ Not installed" -ForegroundColor Red
    Write-Host "   Download from: https://www.python.org/downloads/" -ForegroundColor Cyan
    Write-Host "   ⚠️  Make sure to check 'Add Python to PATH' during installation!" -ForegroundColor Yellow
}
Write-Host ""

# Check Node.js
Write-Host "2. Node.js 18+" -ForegroundColor Yellow
if (Test-Command node) {
    $nodeVersion = node --version 2>&1
    Write-Host "   ✅ Found: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "   ❌ Not installed" -ForegroundColor Red
    Write-Host "   Download from: https://nodejs.org/ (LTS version)" -ForegroundColor Cyan
}
Write-Host ""

# Check PostgreSQL
Write-Host "3. PostgreSQL 14+" -ForegroundColor Yellow
if (Test-Command psql) {
    $pgVersion = psql --version 2>&1
    Write-Host "   ✅ Found: $pgVersion" -ForegroundColor Green
} else {
    Write-Host "   ❌ Not installed" -ForegroundColor Red
    Write-Host "   Download from: https://www.postgresql.org/download/windows/" -ForegroundColor Cyan
    Write-Host "   OR use installer: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads" -ForegroundColor Cyan
}
Write-Host ""

# Check Git (optional but useful)
Write-Host "4. Git (Optional)" -ForegroundColor Yellow
if (Test-Command git) {
    $gitVersion = git --version 2>&1
    Write-Host "   ✅ Found: $gitVersion" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Not installed (optional)" -ForegroundColor Yellow
    Write-Host "   Download from: https://git-scm.com/download/win" -ForegroundColor Cyan
}
Write-Host ""

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Install any missing software from the links above" -ForegroundColor White
Write-Host "2. Restart PowerShell/Terminal after installations" -ForegroundColor White
Write-Host "3. Run this script again to verify installations" -ForegroundColor White
Write-Host "4. Then run: .\setup-backend.ps1" -ForegroundColor White
Write-Host ""

# Pause
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

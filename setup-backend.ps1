# Task Intelligence - Backend Setup Script

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Task Intelligence - Backend Setup" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

$backendPath = Join-Path $PSScriptRoot "backend"

# Check if backend folder exists
if (-not (Test-Path $backendPath)) {
    Write-Host "❌ Backend folder not found at: $backendPath" -ForegroundColor Red
    exit 1
}

Set-Location $backendPath
Write-Host "📁 Working directory: $backendPath" -ForegroundColor Green
Write-Host ""

# Step 1: Create virtual environment
Write-Host "Step 1: Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "   ⚠️  Virtual environment already exists, skipping..." -ForegroundColor Yellow
} else {
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Virtual environment created" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}
Write-Host ""

# Step 2: Activate virtual environment and install dependencies
Write-Host "Step 2: Installing Python dependencies..." -ForegroundColor Yellow
Write-Host "   This may take a few minutes..." -ForegroundColor Gray

$activateScript = Join-Path $backendPath "venv\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript

    # Upgrade pip
    python -m pip install --upgrade pip --quiet

    # Install requirements
    pip install -r requirements.txt

    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Dependencies installed successfully" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "   ❌ Could not find activation script" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 3: Setup environment file
Write-Host "Step 3: Setting up environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "   ⚠️  .env file already exists, skipping..." -ForegroundColor Yellow
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "   ✅ Created .env file from template" -ForegroundColor Green
    Write-Host ""
    Write-Host "   ⚠️  IMPORTANT: You need to edit .env with your credentials!" -ForegroundColor Red
    Write-Host "   Required values:" -ForegroundColor Yellow
    Write-Host "   - DATABASE_URL (PostgreSQL connection)" -ForegroundColor White
    Write-Host "   - MICROSOFT_CLIENT_ID" -ForegroundColor White
    Write-Host "   - MICROSOFT_CLIENT_SECRET" -ForegroundColor White
    Write-Host "   - ANTHROPIC_API_KEY" -ForegroundColor White
    Write-Host "   - SECRET_KEY (generate with: python -c 'import secrets; print(secrets.token_hex(32))')" -ForegroundColor White
    Write-Host "   - JWT_SECRET_KEY (generate with same command)" -ForegroundColor White
}
Write-Host ""

# Step 4: Test imports
Write-Host "Step 4: Testing backend structure..." -ForegroundColor Yellow
if (Test-Path "test_api_structure.py") {
    python test_api_structure.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Backend structure validated" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Some issues found, but you can continue" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ⚠️  Test file not found, skipping validation" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Backend Setup Complete!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file with your credentials" -ForegroundColor White
Write-Host "2. Create PostgreSQL database: createdb task_intelligence" -ForegroundColor White
Write-Host "3. Start backend: .\run-backend.ps1" -ForegroundColor White
Write-Host ""

Set-Location $PSScriptRoot

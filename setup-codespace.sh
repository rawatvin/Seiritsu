#!/bin/bash
set -e

echo "=========================================="
echo "🚀 Setting up Task Intelligence App"
echo "=========================================="

# Navigate to workspace
cd /workspaces/smart-task-app 2>/dev/null || cd /workspaces/task-intelligence-app || {
    echo "❌ Could not find workspace directory"
    exit 1
}

echo "📍 Working directory: $(pwd)"

# Install and setup PostgreSQL
echo ""
echo "📦 Installing PostgreSQL..."
sudo apt-get update -qq
sudo apt-get install -y postgresql postgresql-contrib -qq
sudo service postgresql start
sleep 2

echo "⚙️  Configuring PostgreSQL..."
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';" 2>/dev/null || true
sudo -u postgres createdb task_intelligence 2>/dev/null || echo "  Database already exists"

# Setup Backend
echo ""
echo "📦 Setting up Backend..."
cd backend

echo "  Installing Python dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

if [ ! -f .env ]; then
    echo "📝 Creating backend/.env..."
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    JWT_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

    cat > .env << EOF
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/task_intelligence

# Microsoft Azure AD (Optional - not needed for demo mode)
MICROSOFT_CLIENT_ID=not_needed_for_demo
MICROSOFT_CLIENT_SECRET=not_needed_for_demo
MICROSOFT_REDIRECT_URI=http://localhost:8000/api/v1/auth/callback

# Anthropic (Claude AI) - Optional, app works without it
ANTHROPIC_API_KEY=not_configured

# Security
SECRET_KEY=$SECRET_KEY
JWT_SECRET_KEY=$JWT_SECRET_KEY

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# Environment
ENVIRONMENT=development
DEBUG=true

# CORS
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000","https://*.app.github.dev"]
EOF
    echo "  ✅ Created backend/.env"
else
    echo "  ✅ backend/.env already exists"
fi

echo "🗄️  Creating database tables..."
python3 -c "
import asyncio
from app.db.base import Base, engine

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('  ✅ Database tables created!')

asyncio.run(init_db())
" 2>&1 || echo "  ⚠️  Database tables may already exist"

# Setup Frontend
echo ""
echo "📦 Setting up Frontend..."
cd ../frontend

echo "  Installing Node dependencies..."
npm install -q

if [ ! -f .env ]; then
    echo "📝 Creating frontend/.env..."
    cat > .env << EOF
VITE_API_URL=http://localhost:8000
EOF
    echo "  ✅ Created frontend/.env"
else
    echo "  ✅ frontend/.env already exists"
fi

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "🚀 To start the application:"
echo ""
echo "Terminal 1 - Backend:"
echo "  cd backend"
echo "  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Terminal 2 - Frontend:"
echo "  cd frontend"
echo "  npm run dev -- --host"
echo ""
echo "📱 Then open port 5173 in your browser"
echo "🎯 Use Demo Mode - no API keys needed!"
echo "=========================================="

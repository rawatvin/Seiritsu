#!/bin/bash

echo "=================================================="
echo "Setting up Task Intelligence App in Codespaces..."
echo "=================================================="

# Install PostgreSQL and start it
echo "📦 Setting up PostgreSQL..."
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib
sudo service postgresql start

# Configure PostgreSQL
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
sudo -u postgres createdb task_intelligence || echo "Database already exists"

echo "✅ PostgreSQL ready!"

# Navigate to workspace
cd /workspaces/smart-task-app || cd /workspaces/task-intelligence-app || exit

# Setup Backend
echo ""
echo "📦 Setting up Backend..."
cd backend

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
    JWT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

    cat > .env << EOF
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/task_intelligence

# Microsoft Azure AD (You'll need to add these)
MICROSOFT_CLIENT_ID=your_client_id_here
MICROSOFT_CLIENT_SECRET=your_client_secret_here
MICROSOFT_REDIRECT_URI=https://your-codespace-url-8000.app.github.dev/api/v1/auth/callback

# Anthropic (Claude AI) (You'll need to add this)
ANTHROPIC_API_KEY=your_anthropic_key_here

# Security
SECRET_KEY=$SECRET_KEY
JWT_SECRET_KEY=$JWT_SECRET_KEY

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# Environment
ENVIRONMENT=development
DEBUG=true
EOF
    echo "✅ Created backend/.env"
fi

# Create database tables
echo "Creating database tables..."
python -c "
import asyncio
from app.db.base import Base, engine

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('✅ Database tables created!')

asyncio.run(init_db())
" 2>&1 || echo "⚠️  Database initialization warning (may already exist)"

# Setup Frontend
echo ""
echo "📦 Setting up Frontend..."
cd /workspaces/smart-task-app/frontend || cd /workspaces/task-intelligence-app/frontend

# Install dependencies
npm install

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating frontend .env file..."
    cat > .env << EOF
VITE_API_URL=http://localhost:8000
EOF
    echo "✅ Created frontend/.env"
fi

echo ""
echo "=================================================="
echo "✅ Setup Complete!"
echo "=================================================="
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
echo "⚠️  IMPORTANT: Update backend/.env with:"
echo "  - Microsoft Azure AD credentials"
echo "  - Anthropic API key"
echo "  - Update MICROSOFT_REDIRECT_URI with your Codespace URL"
echo ""
echo "=================================================="

#!/bin/bash
set -e

echo "=========================================="
echo "Setting up Task Intelligence App..."
echo "=========================================="

# Install PostgreSQL
echo "📦 Installing PostgreSQL..."
sudo apt-get update -qq
sudo apt-get install -y postgresql postgresql-contrib >/dev/null 2>&1
sudo service postgresql start
sleep 2

# Configure PostgreSQL
echo "⚙️  Configuring PostgreSQL..."
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';" >/dev/null 2>&1 || true
sudo -u postgres createdb task_intelligence >/dev/null 2>&1 || true

# Setup Backend
echo "📦 Setting up Backend..."
cd backend || exit 1

pip install --upgrade pip -q
pip install -r requirements.txt -q

if [ ! -f .env ]; then
    echo "📝 Creating backend/.env..."
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    JWT_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

    cat > .env << EOF
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/task_intelligence
MICROSOFT_CLIENT_ID=your_client_id_here
MICROSOFT_CLIENT_SECRET=your_client_secret_here
MICROSOFT_REDIRECT_URI=https://your-codespace-url.app.github.dev/api/v1/auth/callback
ANTHROPIC_API_KEY=your_anthropic_key_here
SECRET_KEY=$SECRET_KEY
JWT_SECRET_KEY=$JWT_SECRET_KEY
REDIS_URL=redis://localhost:6379/0
ENVIRONMENT=development
DEBUG=true
EOF
fi

echo "🗄️  Creating database tables..."
python3 -c "
import asyncio
from app.db.base import Base, engine

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_db())
" 2>&1 || true

# Setup Frontend
echo "📦 Setting up Frontend..."
cd ../frontend || exit 1

npm install -q

if [ ! -f .env ]; then
    echo "📝 Creating frontend/.env..."
    cat > .env << EOF
VITE_API_URL=http://localhost:8000
EOF
fi

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "🚀 Start the app:"
echo ""
echo "Terminal 1:"
echo "  cd backend"
echo "  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Terminal 2:"
echo "  cd frontend"
echo "  npm run dev -- --host"
echo ""
echo "⚠️  Configure backend/.env with your API keys!"
echo "=========================================="

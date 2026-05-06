# Backend Quick Start Guide

Get your Task Intelligence backend up and running in minutes!

## Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis 7+ (optional for now, required for Celery)
- Microsoft Azure AD App Registration
- Anthropic API Key

## Step 1: Environment Setup

### Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```env
# Database
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/task_intelligence

# Redis (optional for now)
REDIS_URL=redis://localhost:6379/0

# Microsoft Azure AD
MICROSOFT_CLIENT_ID=your_client_id_here
MICROSOFT_CLIENT_SECRET=your_client_secret_here
MICROSOFT_TENANT_ID=common
MICROSOFT_REDIRECT_URI=http://localhost:8000/api/v1/auth/callback
MICROSOFT_SCOPES=User.Read,Mail.Read,Calendars.Read,Files.Read.All,Team.ReadBasic.All,Chat.Read,OnlineMeetings.Read

# Anthropic Claude API
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Security
SECRET_KEY=your_secret_key_here_generate_with_openssl_rand_hex_32
JWT_SECRET_KEY=your_jwt_secret_key_here_generate_with_openssl_rand_hex_32

# Celery (use Redis URL)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# CORS (frontend URLs)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Application
DEBUG=True
LOG_LEVEL=INFO
```

### Generate Secret Keys

```bash
# Generate random secret keys
python -c "import secrets; print(secrets.token_hex(32))"
```

## Step 3: Database Setup

### Create Database

```bash
# PostgreSQL command line
createdb task_intelligence

# Or using psql
psql -U postgres
CREATE DATABASE task_intelligence;
\q
```

### Run Migrations

The application automatically creates tables on startup using SQLAlchemy. No manual migration needed for first run!

Alternatively, if you want to use Alembic migrations:

```bash
# Initialize Alembic (already done)
# alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

## Step 4: Microsoft Azure AD Setup

### Create App Registration

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to: Azure Active Directory → App Registrations → New Registration
3. Name: "Task Intelligence"
4. Redirect URI: `http://localhost:8000/api/v1/auth/callback` (Web)
5. Click "Register"

### Configure API Permissions

1. Go to "API Permissions"
2. Click "Add a permission" → Microsoft Graph → Delegated permissions
3. Add these permissions:
   - `User.Read`
   - `Mail.Read`
   - `Calendars.Read`
   - `Files.Read.All`
   - `Team.ReadBasic.All`
   - `Chat.Read`
   - `OnlineMeetings.Read`
4. Click "Grant admin consent" (if you have admin rights)

### Create Client Secret

1. Go to "Certificates & secrets"
2. Click "New client secret"
3. Description: "Task Intelligence Backend"
4. Expires: Choose duration
5. Click "Add"
6. **Copy the secret value immediately** (you can't see it again!)

### Update .env File

Copy the Application (client) ID and client secret to your `.env` file.

## Step 5: Get Anthropic API Key

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Create an account or sign in
3. Navigate to API Keys
4. Create a new API key
5. Copy it to your `.env` file as `ANTHROPIC_API_KEY`

## Step 6: Test the Setup

### Run Import Test

```bash
cd backend
python test_api_structure.py
```

This will verify all imports work correctly.

Expected output:
```
============================================================
API STRUCTURE TEST
============================================================
Testing imports...
✓ Config imported
✓ Database base imported
✓ All models imported
✓ Task schemas imported
✓ User schemas imported
✓ All endpoint modules imported
✓ AI service imported
✓ Learning service imported
✓ Microsoft Graph client imported
✓ FastAPI app imported

✅ All imports successful!

Testing API routes...
✓ Found XX API routes

✅ API routes registered successfully!
✅ ALL TESTS PASSED - Ready to start server!
```

## Step 7: Start the Server

### Start FastAPI Server

```bash
uvicorn app.main:app --reload --port 8000
```

The server will start at: http://localhost:8000

### Verify Server is Running

Open your browser and visit:
- **API Root**: http://localhost:8000/
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Step 8: Test Authentication

### Initiate Login

1. Go to http://localhost:8000/docs
2. Find `GET /api/v1/auth/login`
3. Click "Try it out" → "Execute"
4. Copy the `auth_url` from the response
5. Open it in a browser
6. Sign in with your Microsoft account
7. You'll be redirected back with a JWT token

### Use the Token

In the Swagger UI:
1. Click the "Authorize" button at the top
2. Enter: `Bearer YOUR_JWT_TOKEN`
3. Click "Authorize"
4. Now you can test all authenticated endpoints!

## Step 9: Create Your First Task

Using the Swagger UI:

1. Go to `POST /api/v1/tasks`
2. Click "Try it out"
3. Enter task data:
```json
{
  "title": "Test the API",
  "description": "Create and test my first task",
  "status": "todo",
  "priority": "high",
  "source": "manual"
}
```
4. Click "Execute"
5. You should get a 201 response with your task!

## Common Issues & Solutions

### Issue: Database Connection Error

**Error**: `could not connect to server: Connection refused`

**Solution**:
- Verify PostgreSQL is running: `pg_isready`
- Check DATABASE_URL in .env matches your PostgreSQL config
- Ensure database exists: `psql -l | grep task_intelligence`

### Issue: Import Error with SQLAlchemy

**Error**: `ModuleNotFoundError: No module named 'asyncpg'`

**Solution**:
```bash
pip install asyncpg psycopg2-binary
```

### Issue: Authentication Redirect Error

**Error**: OAuth redirect fails or shows error

**Solution**:
- Verify redirect URI in Azure AD matches exactly: `http://localhost:8000/api/v1/auth/callback`
- Check MICROSOFT_CLIENT_ID and MICROSOFT_CLIENT_SECRET in .env
- Ensure API permissions are granted in Azure AD

### Issue: Anthropic API Error

**Error**: `401 Unauthorized` when using AI features

**Solution**:
- Verify ANTHROPIC_API_KEY is correct in .env
- Check your API key has available credits
- Ensure API key hasn't expired

### Issue: CORS Error from Frontend

**Error**: `Access-Control-Allow-Origin` error in browser console

**Solution**:
- Add your frontend URL to CORS_ORIGINS in .env
- Restart the server after changing .env

## Development Workflow

### Hot Reload

The `--reload` flag enables hot reload. Any changes to Python files will automatically restart the server.

### View Logs

Logs are printed to console. Increase verbosity:

```env
LOG_LEVEL=DEBUG
```

### Database Inspection

```bash
# Connect to database
psql task_intelligence

# List tables
\dt

# View tasks
SELECT * FROM tasks LIMIT 10;
```

## Next Steps

1. **Test All Endpoints**: Use the Swagger UI at http://localhost:8000/docs
2. **Configure Sync Sources**: Enable email, Teams, etc. via `/sync` endpoints
3. **Set Up Celery** (optional): For background task processing
4. **Build Frontend**: See frontend README for React setup
5. **Deploy**: See main README for deployment options

## Optional: Celery Setup (for Background Jobs)

### Start Redis

```bash
# Windows (using WSL or Windows Redis port)
redis-server

# Linux/Mac
redis-server
```

### Start Celery Worker

```bash
celery -A app.tasks worker --loglevel=info
```

### Start Celery Beat (Scheduler)

```bash
celery -A app.tasks beat --loglevel=info
```

### Monitor with Flower

```bash
celery -A app.tasks flower
```

Visit http://localhost:5555 to see Celery monitoring dashboard.

## Useful Commands

```bash
# Run tests
pytest

# Format code
black app/

# Lint code
flake8 app/

# Type check
mypy app/

# Generate requirements
pip freeze > requirements.txt

# Database backup
pg_dump task_intelligence > backup.sql

# Database restore
psql task_intelligence < backup.sql
```

## Support

- **Documentation**: See README.md and API_ENDPOINTS.md
- **Issues**: Check IMPLEMENTATION_STATUS.md for known issues
- **API Reference**: http://localhost:8000/docs when server is running

---

**Happy Coding! 🚀**

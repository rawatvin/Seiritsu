# Complete Setup Instructions for Task Intelligence App

## Current Status
✅ Application code is complete  
❌ Prerequisites need to be installed  
❌ Environment configuration needed  
❌ Database setup needed  

---

## Step 1: Install Prerequisites (20 minutes)

### 1.1 Install Python 3.11+
1. Download: https://www.python.org/downloads/
2. Run installer
3. **IMPORTANT**: Check "Add Python to PATH" ✅
4. Click "Install Now"
5. Verify: Open new PowerShell and run: `python --version`

### 1.2 Install Node.js 18+ (LTS)
1. Download: https://nodejs.org/ (Get the LTS version)
2. Run installer with default settings
3. Verify: Open new PowerShell and run: `node --version` and `npm --version`

### 1.3 Install PostgreSQL 14+
1. Download: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
2. Run installer
3. Remember the password you set for the `postgres` user
4. Port: 5432 (default)
5. Verify: Open new PowerShell and run: `psql --version`

**After installing all three, RESTART PowerShell**

---

## Step 2: Create Microsoft Azure AD App (10 minutes)

You need this for Microsoft OAuth authentication:

1. Go to: https://portal.azure.com
2. Navigate to: **Azure Active Directory** → **App registrations**
3. Click **New registration**
   - Name: `Task Intelligence App`
   - Supported account types: `Accounts in this organizational directory only`
   - Redirect URI: `Web` → `http://localhost:8000/api/v1/auth/callback`
4. Click **Register**
5. Copy the **Application (client) ID** (you'll need this)
6. Go to **Certificates & secrets** → **New client secret**
   - Description: `Task Intelligence Secret`
   - Expires: `24 months`
   - Click **Add**
   - Copy the **Value** immediately (you won't see it again!)
7. Go to **API permissions** → **Add a permission** → **Microsoft Graph** → **Delegated permissions**
   - Add these permissions:
     - `User.Read`
     - `Mail.Read`
     - `Calendars.Read`
     - `Files.Read.All`
     - `Team.ReadBasic.All`
     - `Chat.Read`
     - `OnlineMeetings.Read`
8. Click **Grant admin consent** (if you have admin rights)

**Save these for later:**
- Application (client) ID: `_____________________`
- Client Secret Value: `_____________________`

---

## Step 3: Get Anthropic API Key (5 minutes)

1. Go to: https://console.anthropic.com/
2. Sign up or log in
3. Go to **API Keys**
4. Click **Create Key**
5. Copy the key

**Save this for later:**
- Anthropic API Key: `_____________________`

---

## Step 4: Setup Backend (5 minutes)

Open PowerShell in the project directory:

```powershell
cd C:\Users\rawatvin\task-intelligence-app
```

### 4.1 Create Virtual Environment
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error, run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4.2 Install Dependencies
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

This will take 2-3 minutes.

### 4.3 Create Environment File
```powershell
Copy-Item .env.example .env
```

### 4.4 Edit .env File
Open `backend\.env` in a text editor and fill in:

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/task_intelligence

# Microsoft Azure AD
MICROSOFT_CLIENT_ID=your_azure_app_client_id_from_step_2
MICROSOFT_CLIENT_SECRET=your_azure_client_secret_from_step_2
MICROSOFT_REDIRECT_URI=http://localhost:8000/api/v1/auth/callback

# Anthropic (Claude AI)
ANTHROPIC_API_KEY=your_anthropic_key_from_step_3

# Security (Generate these)
SECRET_KEY=run_python_command_below
JWT_SECRET_KEY=run_python_command_below

# Optional - Redis (leave as is if not using)
REDIS_URL=redis://localhost:6379/0

# Environment
ENVIRONMENT=development
DEBUG=true
```

**Generate secret keys:**
```powershell
# Still in the venv, run these commands:
python -c "import secrets; print(secrets.token_hex(32))"
# Copy the output and paste as SECRET_KEY

python -c "import secrets; print(secrets.token_hex(32))"
# Copy the output and paste as JWT_SECRET_KEY
```

---

## Step 5: Create Database (2 minutes)

Open a new PowerShell window:

```powershell
# Connect to PostgreSQL
psql -U postgres

# In psql prompt, run:
CREATE DATABASE task_intelligence;

# Verify:
\l

# Exit:
\q
```

---

## Step 6: Initialize Database Tables (1 minute)

Back in your backend venv PowerShell:

```powershell
# Make sure you're in backend directory with venv activated
cd C:\Users\rawatvin\task-intelligence-app\backend
.\venv\Scripts\Activate.ps1

# Create database tables
python -c "from app.db.base import init_db; import asyncio; asyncio.run(init_db())"
```

---

## Step 7: Setup Frontend (3 minutes)

Open a NEW PowerShell window:

```powershell
cd C:\Users\rawatvin\task-intelligence-app\frontend

# Install dependencies
npm install

# This will take 2-3 minutes
```

### 7.1 Create Frontend Environment File
```powershell
Copy-Item .env.example .env
```

The defaults should work:
```env
VITE_API_URL=http://localhost:8000
```

---

## Step 8: Run the Application! 🚀

### Terminal 1 - Backend
```powershell
cd C:\Users\rawatvin\task-intelligence-app\backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Wait for: ✅ `Application startup complete`  
Backend: http://localhost:8000  
API Docs: http://localhost:8000/docs  

### Terminal 2 - Frontend
```powershell
cd C:\Users\rawatvin\task-intelligence-app\frontend
npm run dev
```

Wait for: ✅ `Local: http://localhost:5173`  
Frontend: http://localhost:5173

---

## Step 9: Test the Application 🧪

1. Open browser: **http://localhost:5173**
2. You should see the login page
3. Click **"Sign in with Microsoft"**
4. Authorize the app
5. You should be redirected to the Dashboard!

### Test Checklist:
- [ ] Login with Microsoft works
- [ ] Dashboard loads with statistics
- [ ] Navigate to Kanban board
- [ ] Create a new task
- [ ] Drag task between columns
- [ ] Edit task details
- [ ] Search for tasks
- [ ] Delete a task

---

## Common Issues & Solutions

### "Python not found"
- Restart PowerShell after installing Python
- Check PATH: `$env:PATH -split ';' | Select-String python`

### "npm not found"
- Restart PowerShell after installing Node.js
- Try closing all PowerShell windows and opening a new one

### "psql not found"
- Add PostgreSQL to PATH manually:
  ```powershell
  $env:PATH += ";C:\Program Files\PostgreSQL\14\bin"
  ```

### "Cannot connect to database"
- Verify PostgreSQL is running: Check Services (services.msc)
- Check password in DATABASE_URL matches your PostgreSQL password
- Test connection: `psql -U postgres -d task_intelligence`

### "Execution policy" error
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Frontend shows "Network Error"
- Make sure backend is running on port 8000
- Check VITE_API_URL in frontend\.env
- Check browser console (F12) for errors

### "Module not found" errors
- Backend: Make sure venv is activated and requirements installed
- Frontend: Run `npm install` again

---

## Quick Start Commands (After Initial Setup)

Once everything is set up, you only need these two commands:

**Terminal 1:**
```powershell
cd C:\Users\rawatvin\task-intelligence-app\backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2:**
```powershell
cd C:\Users\rawatvin\task-intelligence-app\frontend
npm run dev
```

---

## What's Next?

After successful setup:
1. ✅ Create some tasks manually
2. ✅ Connect your Microsoft account
3. ✅ Explore the Analytics page
4. ✅ Configure sync settings
5. ✅ Let the AI learn from your behavior!

---

## Need Help?

- Backend API docs: http://localhost:8000/docs
- Check logs in PowerShell terminals
- Review README.md for feature details
- Check QUICKSTART.md in backend folder

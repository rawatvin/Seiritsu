# 🚀 START HERE - Complete Setup Guide

Welcome! Follow these steps to get your Task Intelligence app running.

## ⚡ Quick Setup (5 Steps)

### Step 1: Install Prerequisites

Run this to check what you need:

```powershell
.\install-prerequisites.ps1
```

**You need to install:**
- **Python 3.11+**: https://www.python.org/downloads/
  - ⚠️ CHECK "Add Python to PATH" during installation!
- **Node.js 18+ (LTS)**: https://nodejs.org/
- **PostgreSQL 14+**: https://www.postgresql.org/download/windows/

After installing, **restart PowerShell** and run the script again to verify.

---

### Step 2: Setup Backend

```powershell
.\setup-backend.ps1
```

This will:
- Create Python virtual environment
- Install all dependencies
- Create `.env` file

**IMPORTANT:** Edit `backend\.env` with your credentials:
```env
DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@localhost:5432/task_intelligence
MICROSOFT_CLIENT_ID=your_azure_app_client_id
MICROSOFT_CLIENT_SECRET=your_azure_app_client_secret
ANTHROPIC_API_KEY=your_claude_api_key
SECRET_KEY=generate_with_python_command_below
JWT_SECRET_KEY=generate_with_python_command_below
```

Generate secret keys:
```powershell
cd backend
.\venv\Scripts\activate
python -c "import secrets; print(secrets.token_hex(32))"
# Copy output to SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"
# Copy output to JWT_SECRET_KEY
```

---

### Step 3: Create Database

```powershell
# Open PowerShell as Administrator
createdb task_intelligence

# Or using psql:
psql -U postgres
CREATE DATABASE task_intelligence;
\q
```

---

### Step 4: Setup Frontend

```powershell
.\setup-frontend.ps1
```

This will:
- Install all Node.js dependencies
- Create `.env` file (defaults work)

---

### Step 5: Run the App!

**Terminal 1 - Backend:**
```powershell
.\run-backend.ps1
```

Wait for: "Uvicorn running on http://0.0.0.0:8000"

**Terminal 2 - Frontend:**
```powershell
.\run-frontend.ps1
```

Wait for: "Local: http://localhost:3000"

---

## 🎯 Access Your App

1. Open browser: **http://localhost:3000**
2. Click "Sign in with Microsoft"
3. Grant permissions
4. You're in! 🎉

---

## 📋 Checklist

Before running:
- [ ] Python installed and in PATH
- [ ] Node.js installed
- [ ] PostgreSQL installed and running
- [ ] Database `task_intelligence` created
- [ ] `backend\.env` configured with all credentials
- [ ] Microsoft Azure AD app created
- [ ] Anthropic API key obtained

---

## 🆘 Common Issues

### "Python not found"
- Install Python: https://www.python.org/downloads/
- **CHECK "Add Python to PATH"** during installation
- Restart PowerShell

### "node not recognized"
- Install Node.js: https://nodejs.org/
- Restart PowerShell

### "psql not recognized"
- Install PostgreSQL: https://www.postgresql.org/download/windows/
- Add to PATH: `C:\Program Files\PostgreSQL\14\bin`
- Restart PowerShell

### "Cannot connect to database"
- Start PostgreSQL service
- Check DATABASE_URL in `backend\.env`
- Verify database exists: `psql -l | findstr task_intelligence`

### "Authentication failed"
- Check Microsoft credentials in `backend\.env`
- Verify Azure AD redirect URI: `http://localhost:8000/api/v1/auth/callback`

---

## 📖 Need More Help?

- **Backend Setup**: `backend\QUICKSTART.md`
- **Frontend Guide**: `frontend\FRONTEND_GUIDE.md`
- **API Reference**: `backend\API_ENDPOINTS.md`
- **Full Guide**: `QUICK_START.md`

---

## 🎊 What You're Building

An AI-powered task management system that:
- ✅ Extracts tasks from Email, Teams, Meetings
- ✅ Uses Claude AI for smart categorization
- ✅ Learns from your behavior
- ✅ Beautiful drag & drop Kanban board
- ✅ Analytics and insights

**Happy Task Managing! 🚀**

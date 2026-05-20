# ⚡ Quick Reference Card

## 🚀 Push to GitHub (One-Time Setup)

```powershell
# 1. Create repo on GitHub: https://github.com/new

# 2. In PowerShell:
cd C:\Users\rawatvin\task-intelligence-app
git remote add origin https://github.com/YOUR_USERNAME/task-intelligence-app.git
git push -u origin main

# 3. Open in Codespaces:
#    GitHub repo → Code → Codespaces → Create codespace
```

---

## ⚙️ Configure (First Time in Codespaces)

```bash
# Edit backend/.env and add:
MICROSOFT_CLIENT_ID=your_client_id
MICROSOFT_CLIENT_SECRET=your_client_secret
ANTHROPIC_API_KEY=sk-ant-your_key

# Get Codespace URL from PORTS tab, then update:
MICROSOFT_REDIRECT_URI=https://your-url-8000.app.github.dev/api/v1/auth/callback

# Update Azure redirect URI to match
```

---

## ▶️ Start Application

```bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev -- --host
```

**Or use VS Code**: `Ctrl+Shift+P` → Run Task → "Start All Services"

---

## 🌐 Access URLs

- **Frontend**: PORTS tab → port 5173 → click globe 🌐
- **Backend API**: PORTS tab → port 8000
- **API Docs**: Backend URL + `/docs`
- **Health Check**: Backend URL + `/health`

---

## 📊 Test Checklist

1. ✅ Open frontend URL → Login page appears
2. ✅ Click "Sign in with Microsoft" → OAuth flow works
3. ✅ Dashboard loads with statistics
4. ✅ Navigate to Kanban board
5. ✅ Create new task → AI suggestions appear
6. ✅ Drag task between columns
7. ✅ Edit task details
8. ✅ Search for tasks
9. ✅ Delete a task

---

## 🔑 Get API Keys

**Microsoft Azure AD**: 
- https://portal.azure.com → App registrations → New
- Copy Client ID and create Client Secret
- Add redirect URI: `https://your-codespace-8000.app.github.dev/api/v1/auth/callback`

**Anthropic Claude**:
- https://console.anthropic.com/ → API Keys → Create
- Copy key (starts with `sk-ant-`)

---

## 🐛 Common Fixes

```bash
# Port already in use
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:5173 | xargs kill -9  # Frontend

# Reinstall dependencies
cd backend && pip install -r requirements.txt
cd frontend && npm install

# Database issues
pg_isready -h localhost -p 5432
sudo service postgresql restart

# View logs
tail -f /tmp/backend.log
tail -f /tmp/frontend.log
```

---

## 💾 Save Your Work

```bash
git add .
git commit -m "Your changes"
git push
```

---

## 🛑 Stop Codespace

github.com → Profile → Codespaces → "..." → Stop

**Saves hours on free tier!**

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `backend/.env` | API keys & secrets |
| `backend/app/main.py` | Backend entry point |
| `frontend/src/App.tsx` | Frontend entry point |
| `CODESPACES_SETUP.md` | Full setup guide |
| `GITHUB_PUSH_INSTRUCTIONS.md` | Detailed push instructions |

---

## 🎯 Key Features

- ✅ Kanban drag-and-drop
- ✅ AI task extraction (Claude)
- ✅ Microsoft 365 sync (Teams, Outlook)
- ✅ Learning system
- ✅ Analytics & insights
- ✅ Auto-prioritization
- ✅ Smart categorization

---

## 📞 Help Resources

- **Codespaces**: https://docs.github.com/en/codespaces
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev
- **Claude API**: https://docs.anthropic.com

---

**Quick Start**: GITHUB_PUSH_INSTRUCTIONS.md  
**Full Docs**: README.md  
**Setup Details**: CODESPACES_SETUP.md

# GitHub Codespaces Setup Guide

This project is configured to run in GitHub Codespaces with zero local installation required!

## 🚀 Quick Start (5 minutes)

### Step 1: Push to GitHub

```bash
# In your local terminal (where the project is)
cd C:\Users\rawatvin\task-intelligence-app

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Task Intelligence App"

# Create a new repository on GitHub at: https://github.com/new
# Then link and push:
git remote add origin https://github.com/YOUR_USERNAME/task-intelligence-app.git
git branch -M main
git push -u origin main
```

### Step 2: Open in Codespaces

1. Go to your GitHub repository
2. Click the green **"Code"** button
3. Click the **"Codespaces"** tab
4. Click **"Create codespace on main"**
5. Wait 2-3 minutes for setup to complete

### Step 3: Configure API Keys

Once Codespace opens, configure your credentials:

#### 3.1 Backend Environment Variables

```bash
# Edit backend/.env
code backend/.env
```

Update these values:
```env
# Get from: https://portal.azure.com (see SETUP_INSTRUCTIONS.md)
MICROSOFT_CLIENT_ID=your_azure_client_id
MICROSOFT_CLIENT_SECRET=your_azure_client_secret

# IMPORTANT: Update this with your Codespace URL
# It will be: https://YOUR-CODESPACE-NAME-8000.app.github.dev/api/v1/auth/callback
MICROSOFT_REDIRECT_URI=https://your-codespace-url-8000.app.github.dev/api/v1/auth/callback

# Get from: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**To find your Codespace URL:**
- After starting the backend (step 4), check the PORTS tab in VS Code
- Find port 8000, hover to see the full URL
- Copy it and update MICROSOFT_REDIRECT_URI

#### 3.2 Update Azure Redirect URI

1. Go to Azure Portal: https://portal.azure.com
2. Navigate to: Azure AD → App Registrations → Your App
3. Go to: Authentication → Redirect URIs
4. Add your Codespace URL: `https://your-codespace-url-8000.app.github.dev/api/v1/auth/callback`
5. Save

### Step 4: Start the Application

#### Terminal 1 - Backend API

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Wait for: `✅ Application startup complete`

#### Terminal 2 - Frontend (Open new terminal: Ctrl+Shift+`)

```bash
cd frontend
npm run dev -- --host
```

Wait for: `✅ Local: http://localhost:5173`

### Step 5: Access Your App

1. Click on the **PORTS** tab in VS Code (bottom panel)
2. Find port **5173** (Frontend)
3. Click the globe icon 🌐 or the URL to open in browser
4. You should see the login page!

---

## 🧪 Testing Checklist

- [ ] Backend API running on port 8000
- [ ] Frontend running on port 5173
- [ ] Can access frontend URL in browser
- [ ] Login page loads
- [ ] Click "Sign in with Microsoft" → redirects to Microsoft
- [ ] After login → redirects back to Dashboard
- [ ] Dashboard shows statistics
- [ ] Kanban board loads
- [ ] Can create a new task
- [ ] Can drag tasks between columns
- [ ] Can edit task details
- [ ] Can delete tasks

---

## 📊 What's Pre-Installed in Codespaces

✅ Python 3.11  
✅ Node.js 18 LTS  
✅ PostgreSQL 15  
✅ Redis 7  
✅ All Python dependencies  
✅ All Node.js dependencies  
✅ Database initialized  
✅ Development tools (Black, Pylint, ESLint, Prettier)  

---

## 🔍 Useful Codespaces Commands

### View Logs
```bash
# Backend logs (in Terminal 1)
# Just watch the uvicorn output

# Frontend logs (in Terminal 2)
# Watch the Vite output

# Database logs
docker logs postgres
```

### Database Management
```bash
# Connect to PostgreSQL
psql -h localhost -U postgres -d task_intelligence
# Password: postgres

# List tables
\dt

# View tasks
SELECT * FROM tasks;

# Exit
\q
```

### Restart Services
```bash
# Backend: Ctrl+C in Terminal 1, then:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend: Ctrl+C in Terminal 2, then:
npm run dev -- --host
```

---

## 🌐 Port Forwarding

Codespaces automatically forwards these ports:

| Port | Service | Access |
|------|---------|--------|
| 8000 | Backend API | https://your-codespace-8000.app.github.dev |
| 5173 | Frontend | https://your-codespace-5173.app.github.dev |
| 5432 | PostgreSQL | localhost:5432 (internal only) |
| 6379 | Redis | localhost:6379 (internal only) |

---

## 📝 API Documentation

Once backend is running, access interactive API docs:
- **Swagger UI**: `https://your-codespace-8000.app.github.dev/docs`
- **ReDoc**: `https://your-codespace-8000.app.github.dev/redoc`

---

## 🐛 Troubleshooting

### "Module not found" error
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### "Database connection failed"
```bash
# Check if PostgreSQL is running
pg_isready -h localhost -p 5432

# Restart PostgreSQL (if needed)
sudo service postgresql restart
```

### "Port already in use"
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:5173 | xargs kill -9  # Frontend
```

### Frontend can't connect to backend
1. Check PORTS tab - make sure port 8000 is forwarded
2. Verify backend is running (Terminal 1)
3. Check `frontend/.env` has correct API URL

### Microsoft OAuth fails
1. Verify Azure redirect URI matches your Codespace URL
2. Check `backend/.env` has correct CLIENT_ID and CLIENT_SECRET
3. Make sure redirect URI ends with `/api/v1/auth/callback`

---

## 💡 Tips

1. **Codespaces are ephemeral** - Save your API keys somewhere safe!
2. **60 free hours/month** on GitHub Free plan
3. **Stop Codespace when not using** to save hours
4. **Changes are auto-saved** but commit to Git regularly
5. **Database persists** within the same Codespace instance

---

## 🔐 Security Notes

- Never commit `.env` files (already in `.gitignore`)
- Keep API keys secure
- Codespaces are private by default
- Use environment secrets for production deployment

---

## 📚 Next Steps

After successful setup:

1. ✅ Create your first task manually
2. ✅ Test Microsoft OAuth login
3. ✅ Try the AI-powered task extraction
4. ✅ Explore the Analytics dashboard
5. ✅ Let the learning system adapt to your usage

---

## 🎯 Features You Can Now Use

- ✅ Complete task management (CRUD)
- ✅ Drag-and-drop Kanban board
- ✅ AI-powered task extraction (Claude)
- ✅ Microsoft 365 integration (Teams, Outlook, SharePoint)
- ✅ Learning system that adapts to your behavior
- ✅ Analytics and insights
- ✅ Monthly reports
- ✅ Smart categorization
- ✅ Auto-prioritization

---

## 📞 Need Help?

- Check the PORTS tab for service status
- View Terminal output for errors
- Check `backend/.env` configuration
- Review API docs at `/docs` endpoint
- See main `README.md` for feature documentation

---

**Happy Task Managing! 🚀**

Built with ❤️ using GitHub Codespaces

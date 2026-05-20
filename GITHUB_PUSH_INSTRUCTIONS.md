# 🚀 Push to GitHub and Launch in Codespaces

Your project is ready to push to GitHub! Follow these steps:

---

## Step 1: Create GitHub Repository

1. Open your browser and go to: **https://github.com/new**

2. Fill in the repository details:
   - **Repository name**: `task-intelligence-app` (or any name you prefer)
   - **Description**: AI-powered task management system with Microsoft 365 integration
   - **Visibility**: 
     - ✅ **Private** (recommended - contains your app code)
     - Or **Public** (if you want to share)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)

3. Click **"Create repository"**

4. You'll see a page with setup instructions. **Keep this page open!**

---

## Step 2: Push Your Code to GitHub

Open PowerShell in your project directory and run these commands:

```powershell
cd C:\Users\rawatvin\task-intelligence-app

# Set your Git identity (if you haven't already)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Add GitHub as the remote repository
# REPLACE 'YOUR_USERNAME' with your actual GitHub username!
git remote add origin https://github.com/YOUR_USERNAME/task-intelligence-app.git

# Rename branch to main (GitHub's default)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

**Note**: You may be prompted to log in to GitHub. Follow the authentication prompts.

---

## Step 3: Open in GitHub Codespaces

1. Go to your repository on GitHub:
   ```
   https://github.com/YOUR_USERNAME/task-intelligence-app
   ```

2. Click the green **"<> Code"** button

3. Click the **"Codespaces"** tab

4. Click **"Create codespace on main"** (the big green button)

5. **Wait 3-5 minutes** while Codespaces:
   - Creates your container
   - Installs Python, Node.js, PostgreSQL
   - Installs all dependencies
   - Sets up the database
   - Runs the setup script

You'll see progress in the terminal at the bottom.

---

## Step 4: Configure API Keys (IMPORTANT!)

Once the Codespace opens, you need to add your API credentials:

### 4.1 Edit Backend Environment File

In VS Code (Codespaces), open: `backend/.env`

Update these values:

```env
# Microsoft Azure AD
# Get these from: https://portal.azure.com
MICROSOFT_CLIENT_ID=your_azure_app_client_id
MICROSOFT_CLIENT_SECRET=your_azure_app_client_secret

# Anthropic Claude API
# Get this from: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-your-key-here

# IMPORTANT: Update redirect URI after starting backend (see step 5)
MICROSOFT_REDIRECT_URI=https://your-codespace-url-8000.app.github.dev/api/v1/auth/callback
```

**Don't have these yet?** See the "Getting API Keys" section below.

---

## Step 5: Start the Application

### Option A: Use VS Code Tasks (Easiest)

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type: `Tasks: Run Task`
3. Select: **"Start All Services"**

Both backend and frontend will start automatically!

### Option B: Manual Terminal Commands

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Wait for: ✅ `Application startup complete`

**Terminal 2 - Frontend (Ctrl+Shift+` to open new terminal):**
```bash
cd frontend
npm run dev -- --host
```

Wait for: ✅ `Local: http://localhost:5173`

---

## Step 6: Update Microsoft Redirect URI

This is **CRITICAL** for OAuth to work!

1. In VS Code, click the **"PORTS"** tab (bottom panel)
2. Find port **8000** (Backend API)
3. Right-click → **"Copy Local Address"**
4. You'll get something like: `https://fictional-space-disco-abcd1234-8000.app.github.dev`

5. Update `backend/.env`:
   ```env
   MICROSOFT_REDIRECT_URI=https://fictional-space-disco-abcd1234-8000.app.github.dev/api/v1/auth/callback
   ```
   (Add `/api/v1/auth/callback` to the end!)

6. **Restart the backend** (Ctrl+C in Terminal 1, then run uvicorn again)

7. Go to **Azure Portal** → **App Registrations** → Your App → **Authentication**
8. Add this URL as a redirect URI
9. Save

---

## Step 7: Access Your App! 🎉

1. In the **PORTS** tab, find port **5173** (Frontend)
2. Click the **globe icon** 🌐 or hover and click "Open in Browser"
3. Your app will open in a new tab!
4. You should see the **login page**

---

## Step 8: Test Everything ✅

### Test Login
1. Click **"Sign in with Microsoft"**
2. You should be redirected to Microsoft login
3. Grant permissions
4. You should be redirected back to the Dashboard

### Test Task Management
1. Navigate to **Kanban** (sidebar)
2. Click **"+ New Task"**
3. Fill in task details
4. AI should suggest categories
5. Save the task
6. Try dragging it between columns
7. Click on a task to edit it
8. Try deleting a task

### Test API Documentation
1. Go to port 8000's URL + `/docs`
2. Example: `https://your-codespace-8000.app.github.dev/docs`
3. You'll see interactive API documentation
4. Try the `/health` endpoint

---

## 📋 Getting API Keys

### Microsoft Azure AD (Required for login)

1. Go to: https://portal.azure.com
2. Navigate: **Azure Active Directory** → **App registrations** → **New registration**
3. Name: `Task Intelligence App`
4. Redirect URI: `Web` → (use your Codespace URL from step 6)
5. Register and copy **Application (client) ID**
6. Go to **Certificates & secrets** → **New client secret**
7. Copy the **Value** immediately
8. Go to **API permissions** → Add these Microsoft Graph permissions:
   - `User.Read`
   - `Mail.Read`
   - `Calendars.Read`
   - `Files.Read.All`
   - `Team.ReadBasic.All`
   - `Chat.Read`
   - `OnlineMeetings.Read`

### Anthropic Claude API (Required for AI features)

1. Go to: https://console.anthropic.com/
2. Sign up or log in
3. Navigate to **API Keys**
4. Click **"Create Key"**
5. Copy the key (starts with `sk-ant-`)

---

## 🎯 Features to Test

Once everything is running:

- ✅ **Dashboard**: View task statistics and charts
- ✅ **Kanban Board**: Drag and drop tasks between columns
- ✅ **Task Creation**: Create tasks with AI suggestions
- ✅ **Task Editing**: Edit task details inline
- ✅ **Search**: Search tasks by title/description
- ✅ **Categories**: Auto-suggested by AI
- ✅ **Priority Levels**: Low, Medium, High, Urgent
- ✅ **Deadlines**: Set and track due dates
- ✅ **Microsoft Login**: OAuth2 authentication

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
# Check PostgreSQL status
pg_isready -h localhost -p 5432

# If needed, restart
sudo service postgresql restart
```

### Frontend shows blank page
1. Check browser console (F12) for errors
2. Verify backend is running on port 8000
3. Check PORTS tab - make sure ports are forwarded
4. Check `frontend/.env` has correct API URL

### Microsoft OAuth fails
1. Verify redirect URI in Azure matches Codespace URL exactly
2. Check CLIENT_ID and CLIENT_SECRET in `backend/.env`
3. Make sure you added `/api/v1/auth/callback` at the end
4. Restart backend after changing .env

### Changes not appearing
- Codespaces has hot reload, but if it's not working:
- Backend: Ctrl+C and restart uvicorn
- Frontend: Ctrl+C and restart npm run dev

---

## 💡 Tips for Using Codespaces

1. **Codespaces are temporary** - They can be stopped/deleted
   - Commit your changes regularly: `git add . && git commit -m "message" && git push`
   - Database data persists within the same Codespace
   - If deleted, data is lost (but code is safe in Git)

2. **Free tier limits**
   - GitHub Free: 60 hours/month
   - GitHub Pro: 90 hours/month
   - Stop Codespace when not using to save hours

3. **Stop Codespace**
   - Go to github.com
   - Click your profile → Codespaces
   - Find your Codespace → Click "..." → "Stop codespace"

4. **Reopen Codespace**
   - Go to your repository
   - Code → Codespaces → Click your existing Codespace
   - Everything will be as you left it!

5. **Port forwarding**
   - Codespaces automatically forwards ports
   - Change visibility: Right-click port → "Port Visibility"
   - Public: Anyone with URL can access
   - Private: Only you (requires GitHub authentication)

---

## 🎊 Success Checklist

- [ ] Code pushed to GitHub
- [ ] Codespace created and running
- [ ] Backend started on port 8000
- [ ] Frontend started on port 5173
- [ ] API keys configured in .env
- [ ] Microsoft redirect URI updated
- [ ] Login page accessible
- [ ] Microsoft OAuth login works
- [ ] Dashboard loads with statistics
- [ ] Kanban board works
- [ ] Can create tasks
- [ ] Can drag tasks between columns
- [ ] AI suggestions appear
- [ ] Search works

---

## 📚 Next Steps

After successful setup:

1. **Explore the app**
   - Create multiple tasks
   - Try different priorities
   - Set deadlines
   - Use search and filters

2. **Configure Microsoft sync** (optional)
   - Settings page
   - Enable email/Teams sync
   - Let AI extract tasks automatically

3. **Review analytics**
   - Check productivity metrics
   - View task trends
   - Get AI insights

4. **Customize**
   - Modify code in Codespaces
   - Changes auto-reload
   - Commit when ready: `git add . && git commit -m "message" && git push`

---

## 📞 Need Help?

- **Codespaces docs**: https://docs.github.com/en/codespaces
- **Check logs**: Look at terminal output
- **API docs**: Visit port 8000 + `/docs`
- **Review setup**: See `CODESPACES_SETUP.md`

---

## 🎉 You're All Set!

Your AI-powered task management system is now running in the cloud with:
- ✅ Zero local installation
- ✅ Full development environment
- ✅ Python, Node.js, PostgreSQL pre-configured
- ✅ All features working (AI, Microsoft sync, learning)
- ✅ Access from anywhere

**Happy Task Managing! 🚀**

---

**Built with ❤️ using:**
- FastAPI (Python backend)
- React + TypeScript (frontend)
- PostgreSQL (database)
- Claude AI (intelligence)
- GitHub Codespaces (cloud dev environment)

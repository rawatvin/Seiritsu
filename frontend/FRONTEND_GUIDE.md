# Frontend Setup & User Guide

Complete guide to running and using the Task Intelligence frontend.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env if needed (defaults should work)
# VITE_API_URL=http://localhost:8000
```

### 3. Start Development Server

```bash
npm run dev
```

The frontend will be available at: **http://localhost:3000**

## 📋 Prerequisites

- Node.js 18+ and npm
- Backend server running at http://localhost:8000
- Microsoft account for authentication

## 🎯 Features

### ✅ Completed Features

1. **Authentication**
   - Microsoft OAuth2 login
   - Secure JWT token management
   - Auto-redirect on session expiry
   - Protected routes

2. **Dashboard**
   - Real-time statistics
   - Active tasks counter
   - Completion metrics
   - Overdue tasks tracking
   - Tasks by status/priority/source
   - Upcoming deadlines widget
   - Quick action cards

3. **Kanban Board**
   - Drag-and-drop task cards
   - 5 columns: Backlog → To Do → In Progress → Review → Completed
   - Real-time search
   - Visual priority indicators
   - Deadline warnings
   - AI extraction badges

4. **Task Management**
   - **Create Task**: Full form with AI suggestions
   - **View Task**: Detailed task information
   - **Edit Task**: Inline editing with auto-save
   - **Delete Task**: Soft delete with confirmation
   - **Drag & Drop**: Move tasks between statuses

5. **AI Features**
   - Auto-suggestions based on task title
   - Category recommendations
   - Time estimates from similar tasks
   - Confidence scoring
   - Learning from user behavior

## 🖥️ User Interface

### Main Layout

```
┌────────────────────────────────────────────────┐
│ Sidebar                 │  Main Content Area   │
│                         │                      │
│ • Dashboard            │  [Page Content]      │
│ • Tasks (Kanban)       │                      │
│ • Analytics            │                      │
│ • Settings             │                      │
│                         │                      │
│ [Sync Now Button]      │                      │
│ [User Profile]         │                      │
│ [Logout]               │                      │
└────────────────────────────────────────────────┘
```

### Dashboard

- **Stats Cards**: Active, Completed (week), Overdue, Total tasks
- **Charts**: Tasks by Status, Priority, Source
- **Upcoming Deadlines**: Next 7 days with day counters
- **Quick Actions**: Create task, View analytics, Configure sync

### Kanban Board

- **Columns**: 5 status columns with task counts
- **Task Cards**: Show title, description, priority, deadline, tags, category
- **Search Bar**: Real-time filtering
- **Drag & Drop**: Click and drag cards between columns
- **Create Button**: Opens modal for new task
- **Click Card**: Opens detail view

### Task Card Features

- **Priority Badge**: Color-coded (Low/Medium/High/Urgent)
- **Deadline**: Shows date with overdue warning
- **AI Badge**: Indicates AI-extracted tasks
- **Tags**: First 3 tags shown (+N more)
- **Category**: Small icon with category name
- **Urgency Indicator**: 🔥 for high urgency (score > 70)

### Create Task Modal

**Fields:**
- Title* (required)
- Description
- Status (dropdown)
- Priority (dropdown)
- Category (with autocomplete from existing)
- Estimated Hours
- Deadline (date-time picker)
- Tags (comma-separated)

**AI Suggestions Panel:**
- Auto-appears when title > 10 characters
- Shows category suggestion with confidence
- Estimated hours based on similar tasks
- Count of similar tasks found
- "Apply Suggestions" button

### Task Detail Modal

**View Mode:**
- Full task information
- Source information panel
- Created/Updated timestamps
- AI extraction confidence
- Assigned users
- Edit and Delete buttons

**Edit Mode:**
- Inline editing of all fields
- Save button with loading state
- Cancel to discard changes

## 🔑 Key Interactions

### Authentication Flow

1. Click "Sign in with Microsoft" on login page
2. Redirected to Microsoft login
3. Grant permissions
4. Redirected back to app
5. Automatically logged in

### Creating a Task

1. Click "New Task" button (top right)
2. Fill in task details
3. Wait for AI suggestions (optional)
4. Click "Apply Suggestions" if desired
5. Click "Create Task"
6. Task appears in appropriate column

### Moving Tasks

**Option 1: Drag & Drop**
- Click and hold task card
- Drag to target column
- Release to drop

**Option 2: Edit Status**
- Click task card to open detail view
- Click edit button
- Change status in dropdown
- Click save

### Searching Tasks

- Type in search bar at top of Kanban board
- Results update automatically (debounced)
- Searches in title and description

### Viewing Task Details

- Click any task card
- Modal opens with full information
- Click Edit to modify
- Click Delete to remove
- Click X or outside to close

## 🎨 Visual Indicators

### Priority Colors

- **Low**: Blue
- **Medium**: Yellow
- **High**: Orange
- **Urgent**: Red

### Status Colors

- **Backlog**: Gray
- **To Do**: Blue
- **In Progress**: Purple
- **Review**: Yellow
- **Completed**: Green
- **Archived**: Gray

### Special Indicators

- 🔥 **High Urgency**: Urgency score > 70
- ✨ **AI Extracted**: Task created by AI
- ⚠️ **Overdue**: Deadline passed
- 📅 **Due Soon**: Within 3 days

## 🛠️ Development

### Project Structure

```
src/
├── components/          # Reusable components
│   ├── TaskCard.tsx
│   ├── CreateTaskModal.tsx
│   ├── TaskDetailModal.tsx
│   ├── Layout.tsx
│   └── LoadingSpinner.tsx
├── pages/              # Page components
│   ├── LoginPage.tsx
│   ├── AuthCallbackPage.tsx
│   ├── DashboardPage.tsx
│   ├── KanbanPage.tsx
│   ├── AnalyticsPage.tsx
│   └── SettingsPage.tsx
├── lib/                # Utilities
│   ├── api.ts         # API client
│   └── utils.ts       # Helper functions
├── store/             # State management
│   └── authStore.ts   # Auth state
├── types/             # TypeScript definitions
│   └── index.ts
├── App.tsx            # Main app component
├── main.tsx           # Entry point
└── index.css          # Global styles
```

### Available Scripts

```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint

# Run tests
npm test
```

### Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **React Router** - Routing
- **TanStack Query** - Data fetching
- **Zustand** - State management
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **Lucide React** - Icons
- **React Hot Toast** - Notifications
- **date-fns** - Date formatting

## 🔧 Configuration

### API Configuration

Edit `.env` file:

```env
# Change if backend runs on different port
VITE_API_URL=http://localhost:8000
```

### Proxy Configuration

`vite.config.ts` is configured to proxy `/api` requests to the backend:

```typescript
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
  },
}
```

## 🐛 Troubleshooting

### Issue: "Cannot connect to backend"

**Solution:**
- Ensure backend is running: `cd backend && uvicorn app.main:app --reload`
- Check VITE_API_URL in `.env`
- Verify no firewall blocking port 8000

### Issue: "Authentication failed"

**Solution:**
- Check Microsoft Azure AD app configuration
- Verify redirect URI: `http://localhost:8000/api/v1/auth/callback`
- Ensure API permissions are granted
- Clear browser cache and try again

### Issue: "Tasks not loading"

**Solution:**
- Open browser console (F12)
- Check for API errors
- Verify backend is responding: http://localhost:8000/health
- Check authentication token exists in localStorage

### Issue: "Drag and drop not working"

**Solution:**
- Make sure browser supports HTML5 drag & drop
- Try refreshing the page
- Check console for JavaScript errors

### Issue: "AI suggestions not appearing"

**Solution:**
- Type at least 10 characters in title
- Click "Show" in AI Suggestions panel
- Check backend ANTHROPIC_API_KEY is set
- Verify backend logs for Claude API errors

## 📱 Responsive Design

The app is optimized for:
- **Desktop**: Full featured, multi-column layout
- **Tablet**: Adjusted spacing, scrollable columns
- **Mobile**: Single column, touch-optimized (needs testing)

## 🔐 Security

- JWT tokens stored in localStorage
- Automatic token refresh on API calls
- Protected routes with auth guard
- CORS configured on backend
- No sensitive data in frontend code

## 🚀 Production Build

```bash
# Build optimized production bundle
npm run build

# Output in dist/ folder
# dist/
#   ├── assets/
#   │   ├── index-[hash].js
#   │   └── index-[hash].css
#   └── index.html

# Preview production build
npm run preview

# Deploy dist/ folder to:
# - Vercel
# - Netlify
# - AWS S3 + CloudFront
# - Azure Static Web Apps
```

## 📊 Performance

- **Code Splitting**: Automatic with Vite
- **Lazy Loading**: Route-based
- **Query Caching**: 5-minute stale time
- **Optimistic Updates**: Instant UI feedback
- **Debounced Search**: 300ms delay

## 🎯 Next Features (Roadmap)

- ⏳ **Analytics Page**: Charts, trends, productivity metrics
- ⏳ **Settings Page**: Sync configuration, user preferences
- ⏳ **Filters**: Advanced filtering by priority, category, tags
- ⏳ **Bulk Actions**: Select multiple tasks, bulk update
- ⏳ **Notifications**: Real-time updates, deadline reminders
- ⏳ **Dark Mode**: Theme toggle
- ⏳ **Mobile App**: React Native version
- ⏳ **Offline Mode**: PWA with service worker

## 💡 Tips

1. **Keyboard Shortcuts**: (To be implemented)
   - `N` - New task
   - `?` - Help
   - `Esc` - Close modals

2. **Best Practices**:
   - Set deadlines for important tasks
   - Use tags for easy filtering
   - Let AI suggest categories
   - Review similar tasks for time estimates
   - Keep descriptions concise

3. **Performance**:
   - Clear browser cache if experiencing issues
   - Limit tasks per view to < 100 for best performance
   - Archive completed tasks regularly

## 📞 Support

- **Backend API**: See `backend/API_ENDPOINTS.md`
- **Issues**: Check browser console (F12)
- **Logs**: Backend logs at `backend/` directory

---

**Built with ❤️ using React, TypeScript, and Claude AI**

Last Updated: 2026-05-02

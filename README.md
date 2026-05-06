# Task Intelligence - AI-Powered Task Management System

An intelligent task management application that automatically aggregates tasks from multiple sources (Microsoft Teams, Outlook, meeting transcripts, SharePoint, Smartsheets), uses AI to extract actionable items, and learns from your behavior to improve over time.

## 🌟 Key Features

### Multi-Source Task Aggregation
- **Email (Outlook)**: Automatically extract action items from your emails
- **Microsoft Teams**: Monitor chats and channels for tasks and mentions
- **Meeting Transcripts**: Parse meeting transcripts for action items and decisions
- **SharePoint**: Track items where you're tagged for action
- **Smartsheets**: Identify potential actions from discussions
- **Manual Entry**: Create tasks manually with full control

### AI-Powered Intelligence
- **Smart Extraction**: Claude AI extracts tasks from unstructured content
- **Auto-Categorization**: Learns your categorization patterns
- **Priority Calculation**: Combines urgency, age, and deadlines
- **Team Recommendations**: Suggests people/teams based on org structure and patterns

### Learning System
- **Adaptive**: Improves with your instructions and choices
- **Pattern Recognition**: Learns from corrections and preferences
- **Smart Suggestions**: Category, assignee, and priority recommendations
- **Usage-Based**: Adapts to how you use the tool

### Kanban Interface
- **Drag & Drop**: Move tasks across statuses effortlessly
- **Deadline Management**: Set and track deadlines
- **Auto-Prioritization**: Tasks bubble up based on urgency and age
- **Archive**: Repository of completed tasks

### Analytics & Insights
- **Monthly Reports**: Time investment by task type
- **Automation Opportunities**: AI identifies repetitive patterns
- **Time-Saving Brainstorming**: Interactive suggestions for efficiency
- **Trend Analysis**: Track task patterns over time

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│        React Frontend (TypeScript)       │
│   Kanban Board | Analytics | Settings   │
└──────────────────┬──────────────────────┘
                   │ REST API
┌──────────────────┴──────────────────────┐
│         FastAPI Backend (Python)         │
│  Auth | Tasks | Sync | Learning | AI    │
└──────────────────┬──────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
┌───▼────┐  ┌─────▼─────┐  ┌────▼────┐
│PostGres│  │  Celery   │  │  Redis  │
│   DB   │  │Scheduler  │  │  Cache  │
└────────┘  └───────────┘  └─────────┘

External Integrations:
- Microsoft Graph API (Teams, Outlook, SharePoint)
- Anthropic Claude API (AI extraction)
- Smartsheets API
```

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+
- Microsoft Account (for OAuth2)
- Anthropic API Key

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd task-intelligence-app
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your credentials:
# - DATABASE_URL
# - REDIS_URL
# - MICROSOFT_CLIENT_ID & CLIENT_SECRET
# - ANTHROPIC_API_KEY
```

### 3. Microsoft Azure AD App Registration

1. Go to [Azure Portal](https://portal.azure.com) → Azure Active Directory
2. App Registrations → New Registration
3. Set redirect URI: `http://localhost:8000/api/v1/auth/callback`
4. API Permissions → Add these Microsoft Graph delegated permissions:
   - `User.Read`
   - `Mail.Read`
   - `Calendars.Read`
   - `Files.Read.All`
   - `Team.ReadBasic.All`
   - `Chat.Read`
   - `OnlineMeetings.Read`
5. Copy Client ID and create a Client Secret
6. Update `.env` file

### 4. Database Setup

```bash
# Start PostgreSQL and create database
createdb task_intelligence

# Run migrations (Alembic)
alembic upgrade head
```

### 5. Start Backend Services

```bash
# Terminal 1: Start FastAPI
uvicorn app.main:app --reload --port 8000

# Terminal 2: Start Celery worker
celery -A app.tasks worker --loglevel=info

# Terminal 3: Start Celery beat (scheduler)
celery -A app.tasks beat --loglevel=info

# Terminal 4: Start Flower (monitoring)
celery -A app.tasks flower
```

### 6. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local

# Update API URL in .env.local
VITE_API_URL=http://localhost:8000

# Start development server
npm run dev
```

### 7. Access the Application

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Celery Monitoring: http://localhost:5555

## 🐳 Docker Deployment

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📊 Database Schema

### Core Tables
- **users**: User accounts and OAuth tokens
- **tasks**: Task items with metadata
- **source_items**: Raw items from external sources

### Learning Tables
- **learning_events**: User interaction tracking
- **learning_preferences**: Learned preferences
- **category_patterns**: Task categorization patterns
- **team_assignment_patterns**: Assignment recommendations

### Analytics Tables
- **monthly_reports**: Generated monthly insights
- **source_integrations**: Sync status per source

## 🤖 How the Learning System Works

1. **Event Recording**: Every user action (task edit, status change, category assignment) is recorded
2. **Pattern Extraction**: Background jobs analyze events to identify patterns
3. **Preference Storage**: Learned patterns are stored as preferences with confidence scores
4. **Smart Suggestions**: Future tasks use learned patterns for recommendations
5. **Feedback Loop**: User acceptance/rejection of suggestions updates confidence scores

### What It Learns

- **Categorization**: Which keywords/contexts map to which categories
- **Assignments**: Which people/teams handle which types of tasks
- **Extraction Corrections**: How you prefer tasks to be extracted
- **Priority Patterns**: What makes a task urgent for you

## 🔄 Sync Schedule

- **Default Interval**: Every 2 hours
- **Configurable**: User can adjust in preferences
- **Manual Trigger**: Available via UI or API

## 📈 Monthly Reports

Automatically generated on the 1st of each month:
- Task completion statistics
- Time investment by category
- Automation opportunities
- Repetitive task patterns
- Time-saving recommendations

## 🔐 Security

- **OAuth2**: Microsoft authentication
- **JWT Tokens**: Secure API access
- **Encrypted Tokens**: User tokens encrypted at rest
- **CORS**: Configured for frontend domain
- **Rate Limiting**: API rate limits (TODO: implement)

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# E2E tests
npm run test:e2e
```

## 📝 API Documentation

Interactive API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints

- `GET /api/v1/auth/login` - Initiate OAuth flow
- `GET /api/v1/tasks` - List tasks with filters
- `POST /api/v1/tasks` - Create manual task
- `PATCH /api/v1/tasks/{id}` - Update task
- `POST /api/v1/sync/trigger` - Manual sync
- `GET /api/v1/analytics/monthly/{year}/{month}` - Get monthly report
- `GET /api/v1/learning/stats` - Learning system statistics

## 🛠️ Configuration

### Environment Variables

See `.env.example` for all available configuration options.

### User Preferences

Configurable in UI:
- Sync interval
- Auto-categorization on/off
- Notification preferences
- Default view (Kanban/List)
- Theme

## 🐛 Troubleshooting

### OAuth Callback Fails
- Check redirect URI matches Azure AD configuration
- Verify client ID and secret in `.env`

### Tasks Not Syncing
- Check Celery worker is running
- Verify Microsoft tokens haven't expired
- Check Celery logs for errors

### Database Connection Issues
- Verify PostgreSQL is running
- Check DATABASE_URL in `.env`
- Ensure database exists

### AI Extraction Not Working
- Verify ANTHROPIC_API_KEY is set
- Check Claude API quota/limits
- Review backend logs for errors

## 📦 Deployment to Cloud

### AWS Deployment
- Use ECS/Fargate for containers
- RDS for PostgreSQL
- ElastiCache for Redis
- S3 for static frontend
- Application Load Balancer

### Azure Deployment
- App Service for backend
- Azure Database for PostgreSQL
- Azure Cache for Redis
- Static Web Apps for frontend
- Azure AD for native integration

### GCP Deployment
- Cloud Run for containers
- Cloud SQL for PostgreSQL
- Memorystore for Redis
- Cloud Storage + CDN for frontend

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file

## 🙏 Acknowledgments

- **FastAPI**: Modern Python web framework
- **React**: UI library
- **Anthropic Claude**: AI-powered task extraction
- **Microsoft Graph API**: Microsoft 365 integration
- **PostgreSQL**: Reliable database
- **Celery**: Distributed task queue

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check documentation
- Review API docs

---

Built with ❤️ for productivity and automation

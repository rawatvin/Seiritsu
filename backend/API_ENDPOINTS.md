# API Endpoints Documentation

Complete reference for all Task Intelligence API endpoints.

**Base URL**: `http://localhost:8000/api/v1`

## Authentication

All endpoints except `/auth/login` and `/auth/callback` require authentication via JWT token in the `Authorization` header:

```
Authorization: Bearer <your_jwt_token>
```

### Auth Endpoints

#### `GET /auth/login`
Initiate Microsoft OAuth2 login flow.

**Response**:
```json
{
  "auth_url": "https://login.microsoftonline.com/...",
  "state": "random_state_token"
}
```

#### `GET /auth/callback`
OAuth2 callback handler (handled automatically).

**Query Parameters**:
- `code`: Authorization code from Microsoft
- `state`: State token for CSRF protection

#### `GET /auth/me`
Get current user profile.

**Response**: `UserResponse`

#### `POST /auth/logout`
Logout current user.

---

## Tasks

### `GET /tasks`
List tasks with filtering, sorting, and pagination.

**Query Parameters**:
- `page` (int, default: 1): Page number
- `page_size` (int, default: 50, max: 100): Items per page
- `status` (list): Filter by status (backlog, todo, in_progress, blocked, review, completed, archived)
- `priority` (list): Filter by priority (low, medium, high, urgent)
- `source` (list): Filter by source (manual, email, teams_chat, teams_channel, meeting_transcript, sharepoint, smartsheet)
- `category` (str): Filter by category
- `tags` (list): Filter by tags
- `assigned_to` (str): Filter by assignee
- `has_deadline` (bool): Filter tasks with/without deadline
- `overdue` (bool): Filter overdue tasks
- `search` (str): Search in title and description
- `sort_by` (str, default: auto_priority_score): Sort field (created_at, updated_at, deadline, auto_priority_score, title)
- `sort_order` (str, default: desc): Sort order (asc, desc)

**Response**: `TaskListResponse`
```json
{
  "tasks": [...],
  "total": 42,
  "page": 1,
  "page_size": 50
}
```

### `POST /tasks`
Create a new task manually.

**Request Body**: `TaskCreate`
```json
{
  "title": "Complete API documentation",
  "description": "Write comprehensive API docs",
  "status": "todo",
  "priority": "high",
  "deadline": "2026-05-15T17:00:00Z",
  "estimated_hours": 3,
  "tags": ["documentation", "api"],
  "category": "Documentation",
  "assigned_to": ["john@example.com"],
  "source": "manual"
}
```

**Response**: `TaskResponse` (201 Created)

### `GET /tasks/{task_id}`
Get a specific task by ID.

**Response**: `TaskResponse`

### `PATCH /tasks/{task_id}`
Update a task.

**Request Body**: `TaskUpdate` (all fields optional)
```json
{
  "title": "Updated title",
  "status": "in_progress",
  "priority": "urgent",
  "actual_hours": 2
}
```

**Response**: `TaskResponse`

### `PATCH /tasks/{task_id}/status`
Quick status update endpoint.

**Request Body**: `TaskStatusUpdate`
```json
{
  "status": "completed",
  "actual_hours": 3
}
```

**Response**: `TaskResponse`

### `DELETE /tasks/{task_id}`
Delete a task (soft delete by default).

**Query Parameters**:
- `hard_delete` (bool, default: false): Permanently delete instead of soft delete

**Response**: 204 No Content

### `POST /tasks/bulk`
Bulk update multiple tasks.

**Request Body**: `TaskBulkUpdate`
```json
{
  "task_ids": ["uuid1", "uuid2", "uuid3"],
  "update": {
    "status": "in_progress",
    "priority": "high"
  }
}
```

**Response**:
```json
{
  "message": "Successfully updated 3 tasks",
  "updated_count": 3
}
```

### `GET /tasks/categories/list`
Get list of unique categories.

**Response**: `["Development", "Documentation", "Meeting", ...]`

### `GET /tasks/tags/list`
Get list of all tags.

**Response**: `["urgent", "bug", "feature", ...]`

---

## Sync

### `GET /sync/status`
Get sync status for all data sources.

**Response**: List of `SyncStatusResponse`
```json
[
  {
    "source_type": "email",
    "is_enabled": true,
    "last_sync_at": "2026-05-02T10:30:00Z",
    "last_sync_status": "success",
    "last_sync_error": null,
    "next_sync_at": "2026-05-02T12:30:00Z",
    "total_items_synced": 245,
    "total_tasks_created": 89
  }
]
```

### `POST /sync/trigger`
Manually trigger synchronization.

**Query Parameters**:
- `sources` (list, optional): Specific sources to sync (if not provided, syncs all enabled)

**Response**: `SyncTriggerResponse`
```json
{
  "message": "Sync triggered successfully",
  "sources_triggered": ["email", "teams_chat"],
  "estimated_completion": "2-5 minutes"
}
```

### `POST /sync/sources/{source_type}/enable`
Enable a data source integration.

**Request Body**: `SourceConfig` (optional)
```json
{
  "folder_filters": ["Inbox", "Project X"],
  "keywords": ["action", "todo", "deadline"],
  "lookback_days": 7,
  "auto_extract": true
}
```

### `POST /sync/sources/{source_type}/disable`
Disable a data source integration.

### `GET /sync/sources/{source_type}/config`
Get configuration for a specific source.

### `PATCH /sync/sources/{source_type}/config`
Update configuration for a specific source.

**Request Body**: `SourceConfig`

### `GET /sync/items/pending`
Get unprocessed source items.

**Query Parameters**:
- `source_type` (str, optional): Filter by source type
- `limit` (int, default: 50): Maximum items to return

### `POST /sync/items/{item_id}/process`
Process a source item and optionally create a task.

**Query Parameters**:
- `create_task` (bool, default: true): Whether to create a task from the item

**Response**:
```json
{
  "message": "Item processed successfully",
  "item_id": "uuid",
  "contains_action": true,
  "task_created": true,
  "task_id": "task_uuid",
  "extracted_data": {...}
}
```

---

## Analytics

### `GET /analytics/summary`
Get dashboard summary statistics.

**Response**: `DashboardSummary`
```json
{
  "total_tasks": 156,
  "active_tasks": 42,
  "completed_this_week": 12,
  "completed_this_month": 45,
  "overdue_tasks": 3,
  "tasks_by_status": {
    "todo": 25,
    "in_progress": 15,
    "completed": 100
  },
  "tasks_by_priority": {
    "high": 10,
    "medium": 20,
    "low": 12
  },
  "tasks_by_source": {
    "email": 50,
    "manual": 30,
    "teams_chat": 20
  },
  "upcoming_deadlines": [...]
}
```

### `GET /analytics/monthly/{year}/{month}`
Get or generate monthly report.

**Path Parameters**:
- `year` (int): Year (e.g., 2026)
- `month` (int): Month (1-12)

**Query Parameters**:
- `regenerate` (bool, default: false): Force regenerate report

**Response**: `MonthlyReportResponse`

### `POST /analytics/brainstorm`
Interactive AI brainstorming for time-saving opportunities.

**Request Body**: `BrainstormRequest`
```json
{
  "message": "How can I reduce time spent on meetings?",
  "context": {
    "current_meetings_hours": 15
  }
}
```

**Response**: `BrainstormResponse`
```json
{
  "response": "Based on your task patterns...",
  "suggestions": [
    {
      "suggestion": "Batch similar meetings together",
      "estimated_time_saved": "2h/week",
      "difficulty": "easy"
    }
  ],
  "follow_up_questions": [
    "What types of meetings take the most time?"
  ]
}
```

### `GET /analytics/trends`
Get task trends over time.

**Query Parameters**:
- `period` (str, default: month): Time period (week, month, quarter, year)

**Response**:
```json
{
  "period": "month",
  "start_date": "2026-04-02T00:00:00Z",
  "end_date": "2026-05-02T00:00:00Z",
  "created_trend": [...],
  "completed_trend": [...]
}
```

### `GET /analytics/productivity`
Get productivity metrics.

**Response**:
```json
{
  "avg_completion_hours": 3.5,
  "week_completion_rate": 85.2,
  "ai_extraction_accuracy": 92.1,
  "tasks_created_this_week": 15,
  "tasks_completed_this_week": 13
}
```

---

## Learning

### `GET /learning/stats`
Get learning system statistics.

**Response**: `LearningStats`
```json
{
  "total_events": 523,
  "events_by_type": {
    "task_created": 150,
    "task_categorized": 89,
    "status_changed": 200
  },
  "total_preferences": 45,
  "preferences_by_type": {
    "category_mapping": 25,
    "team_assignment": 12
  },
  "category_patterns_count": 15,
  "assignment_patterns_count": 8,
  "avg_confidence": 78.5,
  "learning_enabled": true
}
```

### `POST /learning/feedback`
Record user feedback on AI recommendations.

**Request Body**: `FeedbackRequest`
```json
{
  "task_id": "uuid",
  "feedback_type": "category",
  "accepted": false,
  "original_value": "Development",
  "new_value": "Bug Fix",
  "comment": "This is a bug fix, not new development"
}
```

### `GET /learning/suggestions`
Get AI suggestions based on task content.

**Query Parameters**:
- `title` (str, required): Task title
- `description` (str, optional): Task description
- `source` (str, optional): Source type

**Response**: `SuggestionResponse`
```json
{
  "category_suggestion": "Development",
  "category_confidence": 85,
  "assignment_suggestions": [
    {
      "team": "Backend Team",
      "people": ["john@example.com", "jane@example.com"],
      "confidence": 78
    }
  ],
  "similar_tasks": [...],
  "estimated_hours": 3
}
```

### `GET /learning/categories`
Get learned category patterns.

**Response**: List of `CategoryPatternResponse`

### `GET /learning/preferences`
Get learned preferences.

**Query Parameters**:
- `preference_type` (str, optional): Filter by type
- `min_confidence` (int, optional): Minimum confidence score

**Response**: List of `PreferenceResponse`

### `DELETE /learning/preferences/{preference_id}`
Delete a learned preference.

### `POST /learning/reset`
Reset all learning data.

**Query Parameters**:
- `confirm` (bool, required): Must be true to confirm reset

### `GET /learning/events`
Get recent learning events.

**Query Parameters**:
- `limit` (int, default: 50): Maximum events to return
- `event_type` (str, optional): Filter by event type

### `POST /learning/process`
Manually trigger learning pattern extraction.

**Response**:
```json
{
  "message": "Learning processing completed",
  "events_processed": 25
}
```

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid authentication credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

*To be implemented*

---

## Pagination

List endpoints support pagination with the following parameters:
- `page`: Page number (1-indexed)
- `page_size`: Items per page (default: 50, max: 100)

Response includes pagination metadata:
```json
{
  "items": [...],
  "total": 156,
  "page": 1,
  "page_size": 50
}
```

---

## Filtering

Many endpoints support filtering via query parameters. Multiple values can be provided by repeating the parameter:

```
GET /tasks?status=todo&status=in_progress&priority=high
```

---

## Sorting

List endpoints support sorting via `sort_by` and `sort_order` parameters:

```
GET /tasks?sort_by=deadline&sort_order=asc
```

---

## Interactive API Documentation

When the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

These provide interactive API exploration and testing capabilities.

// Task Types
export type TaskStatus = 'backlog' | 'todo' | 'in_progress' | 'blocked' | 'review' | 'completed' | 'archived'
export type TaskPriority = 'low' | 'medium' | 'high' | 'urgent'
export type TaskSource = 'manual' | 'email' | 'teams_chat' | 'teams_channel' | 'meeting_transcript' | 'sharepoint' | 'smartsheet'

export interface Task {
  id: string
  user_id: string
  title: string
  description?: string
  status: TaskStatus
  priority: TaskPriority
  source: TaskSource
  source_id?: string
  source_url?: string
  source_metadata?: Record<string, any>
  deadline?: string
  estimated_hours?: number
  actual_hours?: number
  urgency_score: number
  age_days: number
  auto_priority_score: number
  category?: string
  tags: string[]
  assigned_to: string[]
  recommended_team?: string
  recommended_people?: Array<{ name: string; confidence: number }>
  ai_extracted: boolean
  extraction_confidence?: number
  user_modified: boolean
  created_at: string
  updated_at: string
  completed_at?: string
  archived_at?: string
}

export interface TaskCreate {
  title: string
  description?: string
  status?: TaskStatus
  priority?: TaskPriority
  deadline?: string
  estimated_hours?: number
  tags?: string[]
  category?: string
  assigned_to?: string[]
  source?: TaskSource
  source_id?: string
  source_url?: string
  source_metadata?: Record<string, any>
}

export interface TaskUpdate {
  title?: string
  description?: string
  status?: TaskStatus
  priority?: TaskPriority
  deadline?: string
  estimated_hours?: number
  actual_hours?: number
  tags?: string[]
  category?: string
  assigned_to?: string[]
}

export interface TaskListResponse {
  tasks: Task[]
  total: number
  page: number
  page_size: number
}

export interface TaskFilter {
  status?: TaskStatus[]
  priority?: TaskPriority[]
  source?: TaskSource[]
  category?: string
  tags?: string[]
  assigned_to?: string
  has_deadline?: boolean
  overdue?: boolean
  search?: string
}

// User Types
export interface User {
  id: string
  email: string
  display_name?: string
  given_name?: string
  surname?: string
  microsoft_id: string
  preferences: Record<string, any>
  timezone: string
  is_active: boolean
  is_onboarded: boolean
  created_at: string
  last_login_at?: string
  last_sync_at?: string
}

// Analytics Types
export interface DashboardSummary {
  total_tasks: number
  active_tasks: number
  completed_this_week: number
  completed_this_month: number
  overdue_tasks: number
  tasks_by_status: Record<string, number>
  tasks_by_priority: Record<string, number>
  tasks_by_source: Record<string, number>
  upcoming_deadlines: Array<{
    id: string
    title: string
    deadline: string
    priority: string
    days_until: number
  }>
}

export interface MonthlyReport {
  year: number
  month: number
  total_tasks: number
  completed_tasks: number
  tasks_by_category: Record<string, number>
  tasks_by_source: Record<string, number>
  avg_completion_time_hours?: number
  time_by_category: Record<string, number>
  time_by_priority: Record<string, number>
  automation_suggestions: Array<{
    pattern: string
    frequency: string
    time_saved: number
  }>
  repetitive_task_patterns: Array<{
    description: string
    occurrence_count: number
  }>
  insights: string[]
  time_saving_opportunities: Array<{
    opportunity: string
    estimated_hours_saved: number
  }>
  generated_at: string
}

// Sync Types
export interface SyncStatus {
  source_type: string
  is_enabled: boolean
  last_sync_at?: string
  last_sync_status?: string
  last_sync_error?: string
  next_sync_at?: string
  total_items_synced: number
  total_tasks_created: number
}

// Learning Types
export interface LearningSuggestion {
  category_suggestion?: string
  category_confidence?: number
  assignment_suggestions: Array<{
    team?: string
    people: string[]
    confidence: number
  }>
  similar_tasks: Array<{
    id: string
    title: string
    category?: string
    actual_hours?: number
    similarity_score: number
  }>
  estimated_hours?: number
}

export interface LearningStats {
  total_events: number
  events_by_type: Record<string, number>
  total_preferences: number
  preferences_by_type: Record<string, number>
  category_patterns_count: number
  assignment_patterns_count: number
  avg_confidence: number
  learning_enabled: boolean
}

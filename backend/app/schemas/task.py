from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from app.models.task import TaskStatus, TaskPriority, TaskSource


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    deadline: Optional[datetime] = None
    estimated_hours: Optional[int] = None
    tags: Optional[List[str]] = []
    category: Optional[str] = None
    assigned_to: Optional[List[str]] = []


class TaskCreate(TaskBase):
    source: TaskSource = TaskSource.MANUAL
    source_id: Optional[str] = None
    source_url: Optional[str] = None
    source_metadata: Optional[Dict[str, Any]] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    deadline: Optional[datetime] = None
    estimated_hours: Optional[int] = None
    actual_hours: Optional[int] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = None
    assigned_to: Optional[List[str]] = None
    recommended_team: Optional[str] = None
    recommended_people: Optional[List[Dict[str, Any]]] = None


class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    source: TaskSource
    source_id: Optional[str] = None
    source_url: Optional[str] = None
    source_metadata: Optional[Dict[str, Any]] = None
    urgency_score: int = 0
    age_days: int = 0
    auto_priority_score: int = 0
    assigned_to: Optional[List[str]] = []
    recommended_team: Optional[str] = None
    recommended_people: Optional[List[Dict[str, Any]]] = []
    actual_hours: Optional[int] = None
    ai_extracted: bool = False
    extraction_confidence: Optional[int] = None
    user_modified: bool = False
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    archived_at: Optional[datetime] = None


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total: int
    page: int
    page_size: int


class TaskFilter(BaseModel):
    status: Optional[List[TaskStatus]] = None
    priority: Optional[List[TaskPriority]] = None
    source: Optional[List[TaskSource]] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    assigned_to: Optional[str] = None
    has_deadline: Optional[bool] = None
    overdue: Optional[bool] = None
    search: Optional[str] = None


class TaskStatusUpdate(BaseModel):
    status: TaskStatus
    actual_hours: Optional[int] = None


class TaskBulkUpdate(BaseModel):
    task_ids: List[UUID]
    update: TaskUpdate

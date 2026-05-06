from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, desc
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from app.db.base import get_db
from app.models import User, Task
from app.models.task import TaskStatus, TaskPriority, TaskSource
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
    TaskFilter,
    TaskStatusUpdate,
    TaskBulkUpdate,
)
from app.api.v1.endpoints.auth import get_current_user_dep
from app.learning.learning_service import LearningService
from app.services.ai_service import AIService

router = APIRouter()


@router.get("/", response_model=TaskListResponse)
async def list_tasks(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    status: Optional[List[TaskStatus]] = Query(None),
    priority: Optional[List[TaskPriority]] = Query(None),
    source: Optional[List[TaskSource]] = Query(None),
    category: Optional[str] = Query(None),
    tags: Optional[List[str]] = Query(None),
    assigned_to: Optional[str] = Query(None),
    has_deadline: Optional[bool] = Query(None),
    overdue: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: str = Query("auto_priority_score", regex="^(created_at|updated_at|deadline|auto_priority_score|title)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """List tasks with filtering, sorting, and pagination"""

    # Build query
    query = select(Task).where(
        and_(
            Task.user_id == current_user.id,
            Task.is_deleted == False
        )
    )

    # Apply filters
    if status:
        query = query.where(Task.status.in_(status))

    if priority:
        query = query.where(Task.priority.in_(priority))

    if source:
        query = query.where(Task.source.in_(source))

    if category:
        query = query.where(Task.category == category)

    if tags:
        # Filter tasks that have any of the specified tags
        for tag in tags:
            query = query.where(Task.tags.contains([tag]))

    if assigned_to:
        query = query.where(Task.assigned_to.contains([assigned_to]))

    if has_deadline is not None:
        if has_deadline:
            query = query.where(Task.deadline.is_not(None))
        else:
            query = query.where(Task.deadline.is_(None))

    if overdue:
        query = query.where(
            and_(
                Task.deadline.is_not(None),
                Task.deadline < datetime.utcnow(),
                Task.status.not_in([TaskStatus.COMPLETED, TaskStatus.ARCHIVED])
            )
        )

    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            or_(
                Task.title.ilike(search_pattern),
                Task.description.ilike(search_pattern)
            )
        )

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Apply sorting
    sort_column = getattr(Task, sort_by)
    if sort_order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(sort_column)

    # Apply pagination
    query = query.offset((page - 1) * page_size).limit(page_size)

    # Execute query
    result = await db.execute(query)
    tasks = result.scalars().all()

    return TaskListResponse(
        tasks=tasks,
        total=total,
        page=page,
        page_size=page_size
    )


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Create a new task manually"""

    # Create task
    task = Task(
        user_id=current_user.id,
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        deadline=task_data.deadline,
        estimated_hours=task_data.estimated_hours,
        tags=task_data.tags or [],
        category=task_data.category,
        assigned_to=task_data.assigned_to or [],
        source=task_data.source,
        source_id=task_data.source_id,
        source_url=task_data.source_url,
        source_metadata=task_data.source_metadata or {},
        ai_extracted=False,
        user_modified=False,
    )

    # Calculate auto priority
    task.calculate_auto_priority()

    db.add(task)
    await db.commit()
    await db.refresh(task)

    # Record learning event
    learning_service = LearningService(db)
    await learning_service.record_event(
        user_id=current_user.id,
        event_type="task_created",
        task_id=task.id,
        metadata={
            "category": task.category,
            "priority": task.priority.value,
            "source": task.source.value,
        }
    )

    return task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific task by ID"""

    query = select(Task).where(
        and_(
            Task.id == task_id,
            Task.user_id == current_user.id,
            Task.is_deleted == False
        )
    )

    result = await db.execute(query)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Update a task"""

    # Get existing task
    query = select(Task).where(
        and_(
            Task.id == task_id,
            Task.user_id == current_user.id,
            Task.is_deleted == False
        )
    )

    result = await db.execute(query)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Track changes for learning
    changes = {}
    original_category = task.category
    original_assigned_to = task.assigned_to
    original_status = task.status

    # Update fields
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(task, field):
            setattr(task, field, value)
            changes[field] = value

    # Mark as user modified if AI extracted
    if task.ai_extracted and changes:
        task.user_modified = True

    # Update completion timestamp
    if task_update.status == TaskStatus.COMPLETED and not task.completed_at:
        task.completed_at = datetime.utcnow()

    # Update archived timestamp
    if task_update.status == TaskStatus.ARCHIVED and not task.archived_at:
        task.archived_at = datetime.utcnow()

    # Recalculate auto priority
    task.calculate_auto_priority()

    await db.commit()
    await db.refresh(task)

    # Record learning events
    learning_service = LearningService(db)

    if "category" in changes and original_category != task.category:
        await learning_service.record_event(
            user_id=current_user.id,
            event_type="category_changed",
            task_id=task.id,
            metadata={
                "old_category": original_category,
                "new_category": task.category,
                "title": task.title,
                "description": task.description,
            }
        )

    if "assigned_to" in changes and original_assigned_to != task.assigned_to:
        await learning_service.record_event(
            user_id=current_user.id,
            event_type="assignment_changed",
            task_id=task.id,
            metadata={
                "old_assigned_to": original_assigned_to,
                "new_assigned_to": task.assigned_to,
                "category": task.category,
            }
        )

    if "status" in changes and original_status != task.status:
        await learning_service.record_event(
            user_id=current_user.id,
            event_type="status_changed",
            task_id=task.id,
            metadata={
                "old_status": original_status.value,
                "new_status": task.status.value,
                "actual_hours": task.actual_hours,
            }
        )

    return task


@router.patch("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
    task_id: UUID,
    status_update: TaskStatusUpdate,
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Quick status update endpoint"""

    # Get existing task
    query = select(Task).where(
        and_(
            Task.id == task_id,
            Task.user_id == current_user.id,
            Task.is_deleted == False
        )
    )

    result = await db.execute(query)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    old_status = task.status
    task.status = status_update.status

    if status_update.actual_hours is not None:
        task.actual_hours = status_update.actual_hours

    # Update timestamps
    if status_update.status == TaskStatus.COMPLETED and not task.completed_at:
        task.completed_at = datetime.utcnow()

    if status_update.status == TaskStatus.ARCHIVED and not task.archived_at:
        task.archived_at = datetime.utcnow()

    await db.commit()
    await db.refresh(task)

    # Record learning event
    learning_service = LearningService(db)
    await learning_service.record_event(
        user_id=current_user.id,
        event_type="status_changed",
        task_id=task.id,
        metadata={
            "old_status": old_status.value,
            "new_status": task.status.value,
            "actual_hours": task.actual_hours,
        }
    )

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    hard_delete: bool = Query(False, description="Permanently delete instead of soft delete"),
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Delete a task (soft delete by default)"""

    query = select(Task).where(
        and_(
            Task.id == task_id,
            Task.user_id == current_user.id
        )
    )

    result = await db.execute(query)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if hard_delete:
        await db.delete(task)
    else:
        task.is_deleted = True
        task.archived_at = datetime.utcnow()

    await db.commit()

    # Record learning event
    learning_service = LearningService(db)
    await learning_service.record_event(
        user_id=current_user.id,
        event_type="task_deleted",
        task_id=task.id,
        metadata={
            "hard_delete": hard_delete,
        }
    )


@router.post("/bulk", response_model=dict)
async def bulk_update_tasks(
    bulk_update: TaskBulkUpdate,
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Bulk update multiple tasks"""

    # Get all tasks
    query = select(Task).where(
        and_(
            Task.id.in_(bulk_update.task_ids),
            Task.user_id == current_user.id,
            Task.is_deleted == False
        )
    )

    result = await db.execute(query)
    tasks = result.scalars().all()

    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tasks found"
        )

    # Update each task
    update_data = bulk_update.update.model_dump(exclude_unset=True)
    updated_count = 0

    for task in tasks:
        for field, value in update_data.items():
            if hasattr(task, field):
                setattr(task, field, value)

        # Update timestamps
        if "status" in update_data:
            if update_data["status"] == TaskStatus.COMPLETED and not task.completed_at:
                task.completed_at = datetime.utcnow()
            if update_data["status"] == TaskStatus.ARCHIVED and not task.archived_at:
                task.archived_at = datetime.utcnow()

        # Recalculate auto priority
        task.calculate_auto_priority()
        updated_count += 1

    await db.commit()

    # Record learning event
    learning_service = LearningService(db)
    await learning_service.record_event(
        user_id=current_user.id,
        event_type="bulk_update",
        metadata={
            "task_count": updated_count,
            "updates": update_data,
        }
    )

    return {
        "message": f"Successfully updated {updated_count} tasks",
        "updated_count": updated_count,
    }


@router.get("/categories/list", response_model=List[str])
async def list_categories(
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Get list of unique categories used by the user"""

    query = select(Task.category).where(
        and_(
            Task.user_id == current_user.id,
            Task.category.is_not(None),
            Task.is_deleted == False
        )
    ).distinct()

    result = await db.execute(query)
    categories = [row[0] for row in result.all()]

    return sorted(categories)


@router.get("/tags/list", response_model=List[str])
async def list_tags(
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Get list of all tags used by the user"""

    query = select(Task.tags).where(
        and_(
            Task.user_id == current_user.id,
            Task.tags.is_not(None),
            Task.is_deleted == False
        )
    )

    result = await db.execute(query)
    all_tags = set()

    for row in result.all():
        if row[0]:
            all_tags.update(row[0])

    return sorted(list(all_tags))

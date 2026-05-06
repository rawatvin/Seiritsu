from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, extract
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from uuid import UUID
from pydantic import BaseModel

from app.db.base import get_db
from app.models import User, Task, MonthlyReport
from app.models.task import TaskStatus, TaskPriority, TaskSource
from app.api.v1.endpoints.auth import get_current_user_dep
from app.services.ai_service import AIService

router = APIRouter()


class DashboardSummary(BaseModel):
    """Dashboard summary statistics"""
    total_tasks: int
    active_tasks: int
    completed_this_week: int
    completed_this_month: int
    overdue_tasks: int
    tasks_by_status: Dict[str, int]
    tasks_by_priority: Dict[str, int]
    tasks_by_source: Dict[str, int]
    upcoming_deadlines: List[Dict[str, Any]]


class MonthlyReportResponse(BaseModel):
    """Monthly report data"""
    year: int
    month: int
    total_tasks: int
    completed_tasks: int
    tasks_by_category: Dict[str, int]
    tasks_by_source: Dict[str, int]
    avg_completion_time_hours: Optional[int] = None
    time_by_category: Dict[str, int]
    time_by_priority: Dict[str, int]
    automation_suggestions: List[Dict[str, Any]]
    repetitive_task_patterns: List[Dict[str, Any]]
    insights: List[str]
    time_saving_opportunities: List[Dict[str, Any]]
    generated_at: datetime


class BrainstormRequest(BaseModel):
    """Request for AI brainstorming session"""
    message: str
    context: Optional[Dict[str, Any]] = None


class BrainstormResponse(BaseModel):
    """AI brainstorming response"""
    response: str
    suggestions: List[Dict[str, Any]]
    follow_up_questions: List[str]


@router.get("/summary", response_model=DashboardSummary)
async def get_dashboard_summary(
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Get dashboard summary statistics"""

    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Total tasks
    total_query = select(func.count(Task.id)).where(
        and_(
            Task.user_id == current_user.id,
            Task.is_deleted == False
        )
    )
    total_result = await db.execute(total_query)
    total_tasks = total_result.scalar()

    # Active tasks (not completed or archived)
    active_query = select(func.count(Task.id)).where(
        and_(
            Task.user_id == current_user.id,
            Task.is_deleted == False,
            Task.status.not_in([TaskStatus.COMPLETED, TaskStatus.ARCHIVED])
        )
    )
    active_result = await db.execute(active_query)
    active_tasks = active_result.scalar()

    # Completed this week
    week_query = select(func.count(Task.id)).where(
        and_(
            Task.user_id == current_user.id,
            Task.status == TaskStatus.COMPLETED,
            Task.completed_at >= week_ago
        )
    )
    week_result = await db.execute(week_query)
    completed_this_week = week_result.scalar()

    # Completed this month
    month_query = select(func.count(Task.id)).where(
        and_(
            Task.user_id == current_user.id,
            Task.status == TaskStatus.COMPLETED,
            Task.completed_at >= month_start
        )
    )
    month_result = await db.execute(month_query)
    completed_this_month = month_result.scalar()

    # Overdue tasks
    overdue_query = select(func.count(Task.id)).where(
        and_(
            Task.user_id == current_user.id,
            Task.is_deleted == False,
            Task.deadline < now,
            Task.status.not_in([TaskStatus.COMPLETED, TaskStatus.ARCHIVED])
        )
    )
    overdue_result = await db.execute(overdue_query)
    overdue_tasks = overdue_result.scalar()

    # Tasks by status
    status_query = select(Task.status, func.count(Task.id)).where(
        and_(
            Task.user_id == current_user.id,
            Task.is_deleted == False
        )
    ).group_by(Task.status)
    status_result = await db.execute(status_query)
    tasks_by_status = {row[0].value: row[1] for row in status_result.all()}

    # Tasks by priority
    priority_query = select(Task.priority, func.count(Task.id)).where(
        and_(
            Task.user_id == current_user.id,
            Task.is_deleted == False,
            Task.status.not_in([TaskStatus.COMPLETED, TaskStatus.ARCHIVED])
        )
    ).group_by(Task.priority)
    priority_result = await db.execute(priority_query)
    tasks_by_priority = {row[0].value: row[1] for row in priority_result.all()}

    # Tasks by source
    source_query = select(Task.source, func.count(Task.id)).where(
        and_(
            Task.user_id == current_user.id,
            Task.is_deleted == False
        )
    ).group_by(Task.source)
    source_result = await db.execute(source_query)
    tasks_by_source = {row[0].value: row[1] for row in source_result.all()}

    # Upcoming deadlines (next 7 days)
    next_week = now + timedelta(days=7)
    deadline_query = select(Task).where(
        and_(
            Task.user_id == current_user.id,
            Task.is_deleted == False,
            Task.deadline.is_not(None),
            Task.deadline >= now,
            Task.deadline <= next_week,
            Task.status.not_in([TaskStatus.COMPLETED, TaskStatus.ARCHIVED])
        )
    ).order_by(Task.deadline).limit(10)
    deadline_result = await db.execute(deadline_query)
    upcoming_tasks = deadline_result.scalars().all()

    upcoming_deadlines = [
        {
            "id": str(task.id),
            "title": task.title,
            "deadline": task.deadline,
            "priority": task.priority.value,
            "days_until": (task.deadline - now).days,
        }
        for task in upcoming_tasks
    ]

    return DashboardSummary(
        total_tasks=total_tasks,
        active_tasks=active_tasks,
        completed_this_week=completed_this_week,
        completed_this_month=completed_this_month,
        overdue_tasks=overdue_tasks,
        tasks_by_status=tasks_by_status,
        tasks_by_priority=tasks_by_priority,
        tasks_by_source=tasks_by_source,
        upcoming_deadlines=upcoming_deadlines,
    )


@router.get("/monthly/{year}/{month}", response_model=MonthlyReportResponse)
async def get_monthly_report(
    year: int,
    month: int,
    regenerate: bool = False,
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Get or generate monthly report"""

    # Check if report exists
    query = select(MonthlyReport).where(
        and_(
            MonthlyReport.user_id == current_user.id,
            MonthlyReport.year == year,
            MonthlyReport.month == month
        )
    )
    result = await db.execute(query)
    report = result.scalar_one_or_none()

    # Generate report if not exists or regenerate requested
    if not report or regenerate:
        report = await generate_monthly_report(current_user.id, year, month, db)

    return MonthlyReportResponse(
        year=report.year,
        month=report.month,
        total_tasks=report.total_tasks,
        completed_tasks=report.completed_tasks,
        tasks_by_category=report.tasks_by_category or {},
        tasks_by_source=report.tasks_by_source or {},
        avg_completion_time_hours=report.avg_completion_time_hours,
        time_by_category=report.time_by_category or {},
        time_by_priority=report.time_by_priority or {},
        automation_suggestions=report.automation_suggestions or [],
        repetitive_task_patterns=report.repetitive_task_patterns or [],
        insights=report.insights or [],
        time_saving_opportunities=report.time_saving_opportunities or [],
        generated_at=report.generated_at,
    )


@router.post("/brainstorm", response_model=BrainstormResponse)
async def brainstorm_time_savings(
    request: BrainstormRequest,
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Interactive AI brainstorming for time-saving opportunities"""

    # Get user's task statistics for context
    stats_query = select(Task).where(
        and_(
            Task.user_id == current_user.id,
            Task.is_deleted == False
        )
    )
    stats_result = await db.execute(stats_query)
    tasks = stats_result.scalars().all()

    # Build context
    task_summary = {
        "total_tasks": len(tasks),
        "categories": {},
        "sources": {},
        "avg_estimated_hours": 0,
    }

    total_hours = 0
    for task in tasks:
        # Count by category
        if task.category:
            task_summary["categories"][task.category] = task_summary["categories"].get(task.category, 0) + 1

        # Count by source
        task_summary["sources"][task.source.value] = task_summary["sources"].get(task.source.value, 0) + 1

        # Sum hours
        if task.estimated_hours:
            total_hours += task.estimated_hours

    if len(tasks) > 0:
        task_summary["avg_estimated_hours"] = total_hours / len(tasks)

    # Use AI to brainstorm
    ai_service = AIService()
    response_data = await ai_service.brainstorm_time_savings(
        user_message=request.message,
        task_summary=task_summary,
        additional_context=request.context or {}
    )

    return BrainstormResponse(
        response=response_data.get("response", ""),
        suggestions=response_data.get("suggestions", []),
        follow_up_questions=response_data.get("follow_up_questions", []),
    )


@router.get("/trends")
async def get_trends(
    period: str = "month",  # week, month, quarter, year
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Get task trends over time"""

    now = datetime.utcnow()

    if period == "week":
        start_date = now - timedelta(days=7)
        group_by_unit = "day"
    elif period == "quarter":
        start_date = now - timedelta(days=90)
        group_by_unit = "week"
    elif period == "year":
        start_date = now - timedelta(days=365)
        group_by_unit = "month"
    else:  # month
        start_date = now - timedelta(days=30)
        group_by_unit = "day"

    # Tasks created over time
    created_query = select(
        func.date_trunc(group_by_unit, Task.created_at).label('period'),
        func.count(Task.id).label('count')
    ).where(
        and_(
            Task.user_id == current_user.id,
            Task.created_at >= start_date
        )
    ).group_by('period').order_by('period')

    created_result = await db.execute(created_query)
    created_trend = [
        {"period": str(row[0]), "count": row[1]}
        for row in created_result.all()
    ]

    # Tasks completed over time
    completed_query = select(
        func.date_trunc(group_by_unit, Task.completed_at).label('period'),
        func.count(Task.id).label('count')
    ).where(
        and_(
            Task.user_id == current_user.id,
            Task.completed_at >= start_date,
            Task.completed_at.is_not(None)
        )
    ).group_by('period').order_by('period')

    completed_result = await db.execute(completed_query)
    completed_trend = [
        {"period": str(row[0]), "count": row[1]}
        for row in completed_result.all()
    ]

    return {
        "period": period,
        "start_date": start_date,
        "end_date": now,
        "created_trend": created_trend,
        "completed_trend": completed_trend,
    }


@router.get("/productivity")
async def get_productivity_metrics(
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Get productivity metrics"""

    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)

    # Average completion time
    completion_query = select(
        func.avg(Task.actual_hours)
    ).where(
        and_(
            Task.user_id == current_user.id,
            Task.actual_hours.is_not(None),
            Task.status == TaskStatus.COMPLETED
        )
    )
    completion_result = await db.execute(completion_query)
    avg_completion_hours = completion_result.scalar() or 0

    # Completion rate (this week)
    week_total_query = select(func.count(Task.id)).where(
        and_(
            Task.user_id == current_user.id,
            Task.created_at >= week_ago
        )
    )
    week_total_result = await db.execute(week_total_query)
    week_total = week_total_result.scalar()

    week_completed_query = select(func.count(Task.id)).where(
        and_(
            Task.user_id == current_user.id,
            Task.created_at >= week_ago,
            Task.status == TaskStatus.COMPLETED
        )
    )
    week_completed_result = await db.execute(week_completed_query)
    week_completed = week_completed_result.scalar()

    week_completion_rate = (week_completed / week_total * 100) if week_total > 0 else 0

    # AI extraction accuracy (user modifications)
    ai_extracted_query = select(func.count(Task.id)).where(
        and_(
            Task.user_id == current_user.id,
            Task.ai_extracted == True
        )
    )
    ai_extracted_result = await db.execute(ai_extracted_query)
    ai_extracted_count = ai_extracted_result.scalar()

    ai_modified_query = select(func.count(Task.id)).where(
        and_(
            Task.user_id == current_user.id,
            Task.ai_extracted == True,
            Task.user_modified == True
        )
    )
    ai_modified_result = await db.execute(ai_modified_query)
    ai_modified_count = ai_modified_result.scalar()

    ai_accuracy = ((ai_extracted_count - ai_modified_count) / ai_extracted_count * 100) if ai_extracted_count > 0 else 0

    return {
        "avg_completion_hours": round(avg_completion_hours, 1),
        "week_completion_rate": round(week_completion_rate, 1),
        "ai_extraction_accuracy": round(ai_accuracy, 1),
        "tasks_created_this_week": week_total,
        "tasks_completed_this_week": week_completed,
    }


async def generate_monthly_report(user_id: UUID, year: int, month: int, db: AsyncSession) -> MonthlyReport:
    """Generate a monthly report with AI insights"""

    # Get tasks for the month
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    query = select(Task).where(
        and_(
            Task.user_id == user_id,
            Task.created_at >= start_date,
            Task.created_at < end_date
        )
    )
    result = await db.execute(query)
    tasks = result.scalars().all()

    # Calculate statistics
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.status == TaskStatus.COMPLETED])

    tasks_by_category = {}
    tasks_by_source = {}
    time_by_category = {}
    time_by_priority = {}
    total_hours = 0
    completed_hours = 0

    for task in tasks:
        # Count by category
        if task.category:
            tasks_by_category[task.category] = tasks_by_category.get(task.category, 0) + 1
            if task.actual_hours:
                time_by_category[task.category] = time_by_category.get(task.category, 0) + task.actual_hours

        # Count by source
        tasks_by_source[task.source.value] = tasks_by_source.get(task.source.value, 0) + 1

        # Time by priority
        if task.actual_hours:
            time_by_priority[task.priority.value] = time_by_priority.get(task.priority.value, 0) + task.actual_hours
            total_hours += task.actual_hours
            if task.status == TaskStatus.COMPLETED:
                completed_hours += task.actual_hours

    avg_completion_time = (completed_hours / completed_tasks) if completed_tasks > 0 else 0

    # Use AI to generate insights
    ai_service = AIService()
    insights_data = await ai_service.generate_monthly_insights(
        year=year,
        month=month,
        task_stats={
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "tasks_by_category": tasks_by_category,
            "time_by_category": time_by_category,
            "avg_completion_time": avg_completion_time,
        }
    )

    # Create or update report
    report_query = select(MonthlyReport).where(
        and_(
            MonthlyReport.user_id == user_id,
            MonthlyReport.year == year,
            MonthlyReport.month == month
        )
    )
    report_result = await db.execute(report_query)
    report = report_result.scalar_one_or_none()

    if report:
        # Update existing
        report.total_tasks = total_tasks
        report.completed_tasks = completed_tasks
        report.tasks_by_category = tasks_by_category
        report.tasks_by_source = tasks_by_source
        report.avg_completion_time_hours = int(avg_completion_time)
        report.time_by_category = time_by_category
        report.time_by_priority = time_by_priority
        report.automation_suggestions = insights_data.get("automation_suggestions", [])
        report.repetitive_task_patterns = insights_data.get("repetitive_patterns", [])
        report.insights = insights_data.get("insights", [])
        report.time_saving_opportunities = insights_data.get("time_saving_opportunities", [])
        report.generated_at = datetime.utcnow()
    else:
        # Create new
        report = MonthlyReport(
            user_id=user_id,
            year=year,
            month=month,
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            tasks_by_category=tasks_by_category,
            tasks_by_source=tasks_by_source,
            avg_completion_time_hours=int(avg_completion_time),
            time_by_category=time_by_category,
            time_by_priority=time_by_priority,
            automation_suggestions=insights_data.get("automation_suggestions", []),
            repetitive_task_patterns=insights_data.get("repetitive_patterns", []),
            insights=insights_data.get("insights", []),
            time_saving_opportunities=insights_data.get("time_saving_opportunities", []),
        )
        db.add(report)

    await db.commit()
    await db.refresh(report)

    return report

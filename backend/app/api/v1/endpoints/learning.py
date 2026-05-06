from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, desc
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from uuid import UUID
from pydantic import BaseModel

from app.db.base import get_db
from app.models import User
from app.models.learning import (
    LearningEvent,
    LearningPreference,
    CategoryPattern,
    TeamAssignmentPattern,
    LearningEventType,
)
from app.api.v1.endpoints.auth import get_current_user_dep
from app.learning.learning_service import LearningService

router = APIRouter()


class LearningStats(BaseModel):
    """Learning system statistics"""
    total_events: int
    events_by_type: Dict[str, int]
    total_preferences: int
    preferences_by_type: Dict[str, int]
    category_patterns_count: int
    assignment_patterns_count: int
    avg_confidence: float
    learning_enabled: bool


class FeedbackRequest(BaseModel):
    """User feedback on AI recommendations"""
    task_id: UUID
    feedback_type: str  # category, assignment, extraction
    accepted: bool
    original_value: Optional[Any] = None
    new_value: Optional[Any] = None
    comment: Optional[str] = None


class SuggestionResponse(BaseModel):
    """AI suggestions based on learning"""
    category_suggestion: Optional[str] = None
    category_confidence: Optional[int] = None
    assignment_suggestions: List[Dict[str, Any]] = []
    similar_tasks: List[Dict[str, Any]] = []
    estimated_hours: Optional[int] = None


class CategoryPatternResponse(BaseModel):
    """Category pattern information"""
    category: str
    keywords: List[str]
    task_count: int
    avg_completion_time_hours: Optional[int] = None
    avg_priority: Optional[str] = None


class PreferenceResponse(BaseModel):
    """Learning preference information"""
    preference_type: str
    preference_key: str
    preference_value: Any
    confidence: int
    usage_count: int
    success_count: int


@router.get("/stats", response_model=LearningStats)
async def get_learning_stats(
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Get learning system statistics for the current user"""

    # Total events
    events_count_query = select(func.count(LearningEvent.id)).where(
        LearningEvent.user_id == current_user.id
    )
    events_count_result = await db.execute(events_count_query)
    total_events = events_count_result.scalar()

    # Events by type
    events_by_type_query = select(
        LearningEvent.event_type,
        func.count(LearningEvent.id)
    ).where(
        LearningEvent.user_id == current_user.id
    ).group_by(LearningEvent.event_type)
    events_by_type_result = await db.execute(events_by_type_query)
    events_by_type = {row[0].value: row[1] for row in events_by_type_result.all()}

    # Total preferences
    prefs_count_query = select(func.count(LearningPreference.id)).where(
        LearningPreference.user_id == current_user.id
    )
    prefs_count_result = await db.execute(prefs_count_query)
    total_preferences = prefs_count_result.scalar()

    # Preferences by type
    prefs_by_type_query = select(
        LearningPreference.preference_type,
        func.count(LearningPreference.id)
    ).where(
        LearningPreference.user_id == current_user.id
    ).group_by(LearningPreference.preference_type)
    prefs_by_type_result = await db.execute(prefs_by_type_query)
    preferences_by_type = {row[0]: row[1] for row in prefs_by_type_result.all()}

    # Category patterns
    category_patterns_query = select(func.count(CategoryPattern.id)).where(
        CategoryPattern.user_id == current_user.id
    )
    category_patterns_result = await db.execute(category_patterns_query)
    category_patterns_count = category_patterns_result.scalar()

    # Assignment patterns
    assignment_patterns_query = select(func.count(TeamAssignmentPattern.id)).where(
        TeamAssignmentPattern.user_id == current_user.id
    )
    assignment_patterns_result = await db.execute(assignment_patterns_query)
    assignment_patterns_count = assignment_patterns_result.scalar()

    # Average confidence
    avg_confidence_query = select(func.avg(LearningPreference.confidence)).where(
        LearningPreference.user_id == current_user.id
    )
    avg_confidence_result = await db.execute(avg_confidence_query)
    avg_confidence = avg_confidence_result.scalar() or 0

    return LearningStats(
        total_events=total_events,
        events_by_type=events_by_type,
        total_preferences=total_preferences,
        preferences_by_type=preferences_by_type,
        category_patterns_count=category_patterns_count,
        assignment_patterns_count=assignment_patterns_count,
        avg_confidence=round(avg_confidence, 1),
        learning_enabled=True,
    )


@router.post("/feedback")
async def record_feedback(
    feedback: FeedbackRequest,
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Record user feedback on AI recommendations"""

    learning_service = LearningService(db)

    # Determine event type
    if feedback.feedback_type == "category":
        event_type = LearningEventType.RECOMMENDATION_ACCEPTED if feedback.accepted else LearningEventType.RECOMMENDATION_REJECTED
    elif feedback.feedback_type == "assignment":
        event_type = LearningEventType.RECOMMENDATION_ACCEPTED if feedback.accepted else LearningEventType.RECOMMENDATION_REJECTED
    elif feedback.feedback_type == "extraction":
        event_type = LearningEventType.EXTRACTION_CORRECTED
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid feedback type"
        )

    # Record event
    await learning_service.record_event(
        user_id=current_user.id,
        event_type=event_type.value,
        task_id=feedback.task_id,
        metadata={
            "feedback_type": feedback.feedback_type,
            "accepted": feedback.accepted,
            "original_value": feedback.original_value,
            "new_value": feedback.new_value,
            "comment": feedback.comment,
        }
    )

    # Process feedback immediately for certain types
    if feedback.feedback_type == "category" and not feedback.accepted:
        await learning_service.process_category_correction(
            user_id=current_user.id,
            task_id=feedback.task_id,
            original_category=feedback.original_value,
            new_category=feedback.new_value,
        )

    return {
        "message": "Feedback recorded successfully",
        "feedback_type": feedback.feedback_type,
        "accepted": feedback.accepted,
    }


@router.get("/suggestions", response_model=SuggestionResponse)
async def get_suggestions(
    title: str,
    description: Optional[str] = None,
    source: Optional[str] = None,
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Get AI suggestions based on task content and learned patterns"""

    learning_service = LearningService(db)

    # Get category suggestion
    category_result = await learning_service.suggest_category(
        user_id=current_user.id,
        title=title,
        description=description or "",
    )

    # Get assignment suggestions
    assignment_result = await learning_service.suggest_assignment(
        user_id=current_user.id,
        category=category_result.get("category"),
        title=title,
        description=description or "",
    )

    # Find similar tasks
    similar_tasks = await learning_service.find_similar_tasks(
        user_id=current_user.id,
        title=title,
        description=description or "",
        limit=5,
    )

    # Estimate hours based on similar tasks
    estimated_hours = None
    if similar_tasks:
        total_hours = sum(task.get("actual_hours", 0) for task in similar_tasks if task.get("actual_hours"))
        count = len([task for task in similar_tasks if task.get("actual_hours")])
        if count > 0:
            estimated_hours = int(total_hours / count)

    return SuggestionResponse(
        category_suggestion=category_result.get("category"),
        category_confidence=category_result.get("confidence"),
        assignment_suggestions=assignment_result.get("suggestions", []),
        similar_tasks=similar_tasks,
        estimated_hours=estimated_hours,
    )


@router.get("/categories", response_model=List[CategoryPatternResponse])
async def get_category_patterns(
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Get learned category patterns"""

    query = select(CategoryPattern).where(
        CategoryPattern.user_id == current_user.id
    ).order_by(desc(CategoryPattern.task_count))

    result = await db.execute(query)
    patterns = result.scalars().all()

    return [
        CategoryPatternResponse(
            category=pattern.category,
            keywords=pattern.keywords or [],
            task_count=pattern.task_count,
            avg_completion_time_hours=pattern.avg_completion_time_hours,
            avg_priority=pattern.avg_priority,
        )
        for pattern in patterns
    ]


@router.get("/preferences", response_model=List[PreferenceResponse])
async def get_preferences(
    preference_type: Optional[str] = None,
    min_confidence: Optional[int] = None,
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Get learned preferences"""

    query = select(LearningPreference).where(
        LearningPreference.user_id == current_user.id
    )

    if preference_type:
        query = query.where(LearningPreference.preference_type == preference_type)

    if min_confidence:
        query = query.where(LearningPreference.confidence >= min_confidence)

    query = query.order_by(desc(LearningPreference.confidence))

    result = await db.execute(query)
    preferences = result.scalars().all()

    return [
        PreferenceResponse(
            preference_type=pref.preference_type,
            preference_key=pref.preference_key,
            preference_value=pref.preference_value,
            confidence=pref.confidence,
            usage_count=pref.usage_count,
            success_count=pref.success_count,
        )
        for pref in preferences
    ]


@router.delete("/preferences/{preference_id}")
async def delete_preference(
    preference_id: UUID,
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Delete a learned preference"""

    query = select(LearningPreference).where(
        and_(
            LearningPreference.id == preference_id,
            LearningPreference.user_id == current_user.id
        )
    )

    result = await db.execute(query)
    preference = result.scalar_one_or_none()

    if not preference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preference not found"
        )

    await db.delete(preference)
    await db.commit()

    return {"message": "Preference deleted successfully"}


@router.post("/reset")
async def reset_learning(
    confirm: bool = False,
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Reset all learning data for the current user"""

    if not confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please confirm reset by setting confirm=true"
        )

    # Delete all learning data
    await db.execute(
        LearningEvent.__table__.delete().where(
            LearningEvent.user_id == current_user.id
        )
    )
    await db.execute(
        LearningPreference.__table__.delete().where(
            LearningPreference.user_id == current_user.id
        )
    )
    await db.execute(
        CategoryPattern.__table__.delete().where(
            CategoryPattern.user_id == current_user.id
        )
    )
    await db.execute(
        TeamAssignmentPattern.__table__.delete().where(
            TeamAssignmentPattern.user_id == current_user.id
        )
    )

    await db.commit()

    return {
        "message": "All learning data has been reset",
        "warning": "The system will start learning from scratch"
    }


@router.get("/events")
async def get_recent_events(
    limit: int = 50,
    event_type: Optional[str] = None,
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Get recent learning events"""

    query = select(LearningEvent).where(
        LearningEvent.user_id == current_user.id
    )

    if event_type:
        query = query.where(LearningEvent.event_type == event_type)

    query = query.order_by(desc(LearningEvent.created_at)).limit(limit)

    result = await db.execute(query)
    events = result.scalars().all()

    return {
        "events": [
            {
                "id": str(event.id),
                "task_id": str(event.task_id) if event.task_id else None,
                "event_type": event.event_type.value,
                "event_data": event.event_data,
                "created_at": event.created_at,
                "processed": event.processed,
            }
            for event in events
        ],
        "count": len(events)
    }


@router.post("/process")
async def trigger_learning_processing(
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Manually trigger learning pattern extraction from events"""

    learning_service = LearningService(db)

    # Process unprocessed events
    processed_count = await learning_service.process_pending_events(current_user.id)

    # Update patterns
    await learning_service.update_category_patterns(current_user.id)
    await learning_service.update_assignment_patterns(current_user.id)

    return {
        "message": "Learning processing completed",
        "events_processed": processed_count,
    }

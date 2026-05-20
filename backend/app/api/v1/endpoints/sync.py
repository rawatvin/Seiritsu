from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from uuid import UUID

from app.db.base import get_db
from app.models import User, Task, SourceIntegration, SourceItem
from app.models.task import TaskSource
from app.api.v1.endpoints.auth import get_current_user_dep
from app.integrations.microsoft_graph import MicrosoftGraphClient
from app.services.ai_service import AIService
from app.learning.learning_service import LearningService
from pydantic import BaseModel

router = APIRouter()


class SourceConfig(BaseModel):
    """Configuration for a data source"""
    folder_filters: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    lookback_days: Optional[int] = 7
    auto_extract: Optional[bool] = True


class SyncStatusResponse(BaseModel):
    source_type: str
    is_enabled: bool
    last_sync_at: Optional[datetime] = None
    last_sync_status: Optional[str] = None
    last_sync_error: Optional[str] = None
    next_sync_at: Optional[datetime] = None
    total_items_synced: int = 0
    total_tasks_created: int = 0


class SyncTriggerResponse(BaseModel):
    message: str
    sources_triggered: List[str]
    estimated_completion: str


@router.get("/status", response_model=List[SyncStatusResponse])
async def get_sync_status(
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Get sync status for all data sources"""

    query = select(SourceIntegration).where(
        SourceIntegration.user_id == current_user.id
    )

    result = await db.execute(query)
    integrations = result.scalars().all()

    return [
        SyncStatusResponse(
            source_type=integration.source_type,
            is_enabled=integration.is_enabled,
            last_sync_at=integration.last_sync_at,
            last_sync_status=integration.last_sync_status,
            last_sync_error=integration.last_sync_error,
            next_sync_at=integration.next_sync_at,
            total_items_synced=integration.total_items_synced,
            total_tasks_created=integration.total_tasks_created,
        )
        for integration in integrations
    ]


@router.post("/trigger", response_model=SyncTriggerResponse)
async def trigger_sync(
    sources: Optional[List[str]] = None,
    background_tasks: BackgroundTasks = None,
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Manually trigger synchronization for specified sources"""

    # Get enabled integrations
    query = select(SourceIntegration).where(
        and_(
            SourceIntegration.user_id == current_user.id,
            SourceIntegration.is_enabled == True
        )
    )

    if sources:
        query = query.where(SourceIntegration.source_type.in_(sources))

    result = await db.execute(query)
    integrations = result.scalars().all()

    if not integrations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No enabled integrations found"
        )

    # Trigger sync for each integration (in production, use Celery)
    sources_triggered = []
    for integration in integrations:
        # Update next sync time
        integration.next_sync_at = datetime.utcnow()
        sources_triggered.append(integration.source_type)

        # Schedule background task
        if background_tasks:
            background_tasks.add_task(
                sync_source,
                user_id=current_user.id,
                source_type=integration.source_type,
                db=db
            )

    await db.commit()

    return SyncTriggerResponse(
        message="Sync triggered successfully",
        sources_triggered=sources_triggered,
        estimated_completion="2-5 minutes"
    )


@router.post("/sources/{source_type}/enable")
async def enable_source(
    source_type: str,
    config: Optional[SourceConfig] = None,
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Enable a data source integration"""

    # Check if integration exists
    query = select(SourceIntegration).where(
        and_(
            SourceIntegration.user_id == current_user.id,
            SourceIntegration.source_type == source_type
        )
    )

    result = await db.execute(query)
    integration = result.scalar_one_or_none()

    if integration:
        # Update existing integration
        integration.is_enabled = True
        if config:
            integration.config = config.model_dump()
    else:
        # Create new integration
        integration = SourceIntegration(
            user_id=current_user.id,
            source_type=source_type,
            is_enabled=True,
            config=config.model_dump() if config else {},
        )
        db.add(integration)

    await db.commit()
    await db.refresh(integration)

    return {
        "message": f"Source {source_type} enabled successfully",
        "integration": {
            "source_type": integration.source_type,
            "is_enabled": integration.is_enabled,
        }
    }


@router.post("/sources/{source_type}/disable")
async def disable_source(
    source_type: str,
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Disable a data source integration"""

    query = select(SourceIntegration).where(
        and_(
            SourceIntegration.user_id == current_user.id,
            SourceIntegration.source_type == source_type
        )
    )

    result = await db.execute(query)
    integration = result.scalar_one_or_none()

    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Integration {source_type} not found"
        )

    integration.is_enabled = False
    await db.commit()

    return {
        "message": f"Source {source_type} disabled successfully"
    }


@router.get("/sources/{source_type}/config")
async def get_source_config(
    source_type: str,
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Get configuration for a specific source"""

    query = select(SourceIntegration).where(
        and_(
            SourceIntegration.user_id == current_user.id,
            SourceIntegration.source_type == source_type
        )
    )

    result = await db.execute(query)
    integration = result.scalar_one_or_none()

    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Integration {source_type} not found"
        )

    return {
        "source_type": integration.source_type,
        "is_enabled": integration.is_enabled,
        "config": integration.config or {},
    }


@router.patch("/sources/{source_type}/config")
async def update_source_config(
    source_type: str,
    config: SourceConfig,
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Update configuration for a specific source"""

    query = select(SourceIntegration).where(
        and_(
            SourceIntegration.user_id == current_user.id,
            SourceIntegration.source_type == source_type
        )
    )

    result = await db.execute(query)
    integration = result.scalar_one_or_none()

    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Integration {source_type} not found"
        )

    integration.config = config.model_dump(exclude_unset=True)
    await db.commit()

    return {
        "message": f"Configuration updated for {source_type}",
        "config": integration.config
    }


@router.get("/items/pending")
async def get_pending_items(
    source_type: Optional[str] = None,
    limit: int = 50,
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Get unprocessed source items"""

    query = select(SourceItem).where(
        and_(
            SourceItem.user_id == current_user.id,
            SourceItem.processed == False
        )
    )

    if source_type:
        query = query.where(SourceItem.source_type == source_type)

    query = query.order_by(SourceItem.created_at.desc()).limit(limit)

    result = await db.execute(query)
    items = result.scalars().all()

    return {
        "items": [
            {
                "id": str(item.id),
                "source_type": item.source_type,
                "source_id": item.source_id,
                "subject": item.subject,
                "sender": item.sender,
                "contains_action": item.contains_action,
                "action_confidence": item.action_confidence,
                "created_at": item.created_at,
            }
            for item in items
        ],
        "count": len(items)
    }


@router.post("/items/{item_id}/process")
async def process_item(
    item_id: UUID,
    create_task: bool = True,
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Process a source item and optionally create a task"""

    # Get source item
    query = select(SourceItem).where(
        and_(
            SourceItem.id == item_id,
            SourceItem.user_id == current_user.id
        )
    )

    result = await db.execute(query)
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source item not found"
        )

    if item.processed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item already processed"
        )

    # Extract task using AI
    ai_service = AIService()
    learning_service = LearningService(db)

    # Get user patterns for better extraction
    patterns = await learning_service.get_extraction_patterns(current_user.id)

    content = f"Subject: {item.subject}\n\n{item.body}"
    extracted = await ai_service.extract_task(
        content=content,
        source_type=item.source_type,
        user_patterns=patterns
    )

    # Update source item
    item.processed = True
    item.processed_at = datetime.utcnow()
    item.contains_action = extracted.get("is_actionable", False)
    item.action_confidence = extracted.get("confidence", 0)
    item.extracted_data = extracted

    task = None
    if create_task and item.contains_action:
        # Create task
        task = Task(
            user_id=current_user.id,
            title=extracted.get("title", item.subject),
            description=extracted.get("description", item.body),
            priority=extracted.get("priority", "medium"),
            deadline=extracted.get("deadline"),
            estimated_hours=extracted.get("estimated_hours"),
            source=item.source_type,
            source_id=item.source_id,
            source_url=item.source_url,
            source_metadata=item.metadata,
            category=extracted.get("category"),
            tags=extracted.get("tags", []),
            urgency_score=extracted.get("urgency_score", 0),
            ai_extracted=True,
            extraction_confidence=item.action_confidence,
        )

        task.calculate_auto_priority()
        db.add(task)

        item.task_created = True
        item.task_id = task.id

    await db.commit()

    return {
        "message": "Item processed successfully",
        "item_id": str(item.id),
        "contains_action": item.contains_action,
        "task_created": task is not None,
        "task_id": str(task.id) if task else None,
        "extracted_data": extracted,
    }


# Helper function for background sync (in production, move to Celery)
async def sync_source(user_id: UUID, source_type: str, db: AsyncSession):
    """Background task to sync a specific source"""

    # This is a placeholder - in production, this should be a Celery task
    # The actual implementation would fetch data from Microsoft Graph API
    # and create SourceItem records for processing

    pass

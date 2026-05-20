from sqlalchemy import Column, String, DateTime, Integer, Boolean, JSON, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.base import Base


class SourceIntegration(Base):
    """Tracks integration status and sync state for each data source"""
    __tablename__ = "source_integrations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    source_type = Column(String(50), nullable=False)  # email, teams_chat, sharepoint, etc.
    is_enabled = Column(Boolean, default=True)

    # Sync tracking
    last_sync_at = Column(DateTime(timezone=True))
    last_sync_status = Column(String(50))  # success, error, partial
    last_sync_error = Column(String(500))
    next_sync_at = Column(DateTime(timezone=True))

    # Statistics
    total_items_synced = Column(Integer, default=0)
    total_tasks_created = Column(Integer, default=0)

    # Source-specific config
    config = Column(JSON)  # e.g., folder filters, keywords to watch

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="source_integrations")

    __table_args__ = (
        Index('ix_source_integrations_user_type', 'user_id', 'source_type'),
    )


class SourceItem(Base):
    """Raw items fetched from external sources before task extraction"""
    __tablename__ = "source_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    source_type = Column(String(50), nullable=False, index=True)
    source_id = Column(String(255), nullable=False)  # Original ID in source system
    source_url = Column(String(1000))

    # Content
    subject = Column(String(500))
    body = Column(String)
    sender = Column(String(255))
    participants = Column(JSON)
    metadata = Column(JSON)

    # Processing
    processed = Column(Boolean, default=False, index=True)
    processed_at = Column(DateTime(timezone=True))
    task_created = Column(Boolean, default=False)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"))

    # AI analysis
    contains_action = Column(Boolean)
    action_confidence = Column(Integer)  # 0-100
    extracted_data = Column(JSON)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User")
    task = relationship("Task")

    __table_args__ = (
        Index('ix_source_items_source_id', 'source_type', 'source_id', unique=True),
        Index('ix_source_items_user_processed', 'user_id', 'processed'),
    )


class MonthlyReport(Base):
    """Monthly task analytics and automation recommendations"""
    __tablename__ = "monthly_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)

    # Task statistics
    total_tasks = Column(Integer, default=0)
    completed_tasks = Column(Integer, default=0)
    tasks_by_category = Column(JSON)
    tasks_by_source = Column(JSON)
    avg_completion_time_hours = Column(Integer)

    # Time investment
    time_by_category = Column(JSON)
    time_by_priority = Column(JSON)

    # Automation opportunities
    automation_suggestions = Column(JSON)
    repetitive_task_patterns = Column(JSON)

    # AI-generated insights
    insights = Column(JSON)
    time_saving_opportunities = Column(JSON)

    generated_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationships
    user = relationship("User")

    __table_args__ = (
        Index('ix_monthly_reports_user_period', 'user_id', 'year', 'month', unique=True),
    )

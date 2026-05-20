from sqlalchemy import Column, String, DateTime, Integer, Text, Boolean, JSON, Enum, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
from app.db.base import Base


class LearningEventType(str, enum.Enum):
    TASK_CREATED = "task_created"
    TASK_EDITED = "task_edited"
    TASK_STATUS_CHANGED = "task_status_changed"
    TASK_CATEGORIZED = "task_categorized"
    TASK_ASSIGNED = "task_assigned"
    EXTRACTION_CORRECTED = "extraction_corrected"
    PRIORITY_ADJUSTED = "priority_adjusted"
    DEADLINE_SET = "deadline_set"
    TAG_ADDED = "tag_added"
    RECOMMENDATION_ACCEPTED = "recommendation_accepted"
    RECOMMENDATION_REJECTED = "recommendation_rejected"


class LearningEvent(Base):
    """Tracks user interactions for learning system"""
    __tablename__ = "learning_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=True, index=True)

    event_type = Column(Enum(LearningEventType), nullable=False, index=True)
    event_data = Column(JSON)  # Before/after values, context

    # For extraction corrections
    original_extraction = Column(JSON)  # What AI extracted
    user_correction = Column(JSON)  # What user changed it to

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)

    # Learning processing
    processed = Column(Boolean, default=False, index=True)
    processed_at = Column(DateTime(timezone=True))

    # Relationships
    user = relationship("User")
    task = relationship("Task", back_populates="learning_events")

    __table_args__ = (
        Index('ix_learning_events_user_type', 'user_id', 'event_type'),
    )


class LearningPreference(Base):
    """Stores learned user preferences and patterns"""
    __tablename__ = "learning_preferences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    preference_type = Column(String(100), nullable=False, index=True)  # e.g., "category_mapping", "team_assignment"
    preference_key = Column(String(255), nullable=False)  # e.g., specific keyword or pattern
    preference_value = Column(JSON, nullable=False)  # The learned preference

    # Confidence and usage tracking
    confidence = Column(Integer, default=0)  # 0-100
    usage_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    last_used_at = Column(DateTime(timezone=True))

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="learning_preferences")

    __table_args__ = (
        Index('ix_learning_prefs_user_type', 'user_id', 'preference_type'),
    )


class CategoryPattern(Base):
    """Learned patterns for task categorization"""
    __tablename__ = "category_patterns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    category = Column(String(100), nullable=False, index=True)
    keywords = Column(JSON)  # List of keywords associated with this category
    context_patterns = Column(JSON)  # Patterns in task context
    source_weights = Column(JSON)  # How often this category appears from each source

    # Statistics
    task_count = Column(Integer, default=0)
    avg_completion_time_hours = Column(Integer)
    avg_priority = Column(String(20))

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User")


class TeamAssignmentPattern(Base):
    """Learned patterns for team/people recommendations"""
    __tablename__ = "team_assignment_patterns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    category = Column(String(100), index=True)
    keywords = Column(JSON)
    assigned_team = Column(String(255))
    assigned_people = Column(JSON)  # List of people IDs/emails

    # Statistics
    assignment_count = Column(Integer, default=0)
    success_rate = Column(Integer, default=0)  # Percentage of times kept vs changed

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User")

    __table_args__ = (
        Index('ix_team_patterns_user_category', 'user_id', 'category'),
    )

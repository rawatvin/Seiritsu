from sqlalchemy import Column, String, DateTime, Integer, Text, Boolean, JSON, Enum, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
from app.db.base import Base


class TaskStatus(str, enum.Enum):
    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    REVIEW = "review"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskSource(str, enum.Enum):
    MANUAL = "manual"
    EMAIL = "email"
    TEAMS_CHAT = "teams_chat"
    TEAMS_CHANNEL = "teams_channel"
    MEETING_TRANSCRIPT = "meeting_transcript"
    SHAREPOINT = "sharepoint"
    SMARTSHEET = "smartsheet"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    # Core fields
    title = Column(String(500), nullable=False)
    description = Column(Text)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO, nullable=False, index=True)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)

    # Source tracking
    source = Column(Enum(TaskSource), nullable=False, index=True)
    source_id = Column(String(255))  # Original message/item ID from source system
    source_url = Column(Text)  # Link back to original item
    source_metadata = Column(JSON)  # Additional source-specific data

    # Scheduling
    deadline = Column(DateTime(timezone=True))
    estimated_hours = Column(Integer)
    actual_hours = Column(Integer)

    # Prioritization factors
    urgency_score = Column(Integer, default=0)  # AI-calculated urgency (0-100)
    age_days = Column(Integer, default=0)  # Days since creation
    auto_priority_score = Column(Integer, default=0, index=True)  # Combined score for sorting

    # Assignment & collaboration
    assigned_to = Column(JSON)  # List of user IDs or team members
    recommended_team = Column(String(255))  # AI recommendation
    recommended_people = Column(JSON)  # List of recommended people with confidence scores

    # Tags and categorization
    tags = Column(JSON)  # User-defined tags
    category = Column(String(100), index=True)  # AI-learned category

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime(timezone=True))
    archived_at = Column(DateTime(timezone=True))

    # Soft delete
    is_deleted = Column(Boolean, default=False, index=True)

    # Learning metadata
    ai_extracted = Column(Boolean, default=False)
    extraction_confidence = Column(Integer)  # 0-100
    user_modified = Column(Boolean, default=False)  # Track if user edited AI extraction

    # Relationships
    user = relationship("User", back_populates="tasks")
    learning_events = relationship("LearningEvent", back_populates="task", cascade="all, delete-orphan")

    __table_args__ = (
        Index('ix_tasks_user_status', 'user_id', 'status'),
        Index('ix_tasks_user_priority', 'user_id', 'auto_priority_score'),
        Index('ix_tasks_deadline', 'deadline'),
    )

    def calculate_auto_priority(self):
        """Calculate automatic priority score based on urgency, age, and deadline"""
        score = 0

        # Urgency component (0-40 points)
        score += (self.urgency_score or 0) * 0.4

        # Age component (0-30 points)
        score += min((self.age_days or 0) * 2, 30)

        # Deadline component (0-30 points)
        if self.deadline:
            days_until_deadline = (self.deadline - datetime.utcnow()).days
            if days_until_deadline < 0:
                score += 30  # Overdue
            elif days_until_deadline == 0:
                score += 25  # Due today
            elif days_until_deadline <= 3:
                score += 20
            elif days_until_deadline <= 7:
                score += 10

        self.auto_priority_score = int(score)
        return self.auto_priority_score

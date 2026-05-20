from sqlalchemy import Column, String, DateTime, Boolean, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Microsoft account info
    microsoft_id = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    display_name = Column(String(255))
    given_name = Column(String(255))
    surname = Column(String(255))

    # OAuth tokens
    access_token = Column(Text)  # Encrypted
    refresh_token = Column(Text)  # Encrypted
    token_expires_at = Column(DateTime(timezone=True))

    # User preferences
    preferences = Column(JSON, default={})  # UI preferences, notification settings
    timezone = Column(String(50), default="UTC")

    # Status
    is_active = Column(Boolean, default=True)
    is_onboarded = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime(timezone=True))
    last_sync_at = Column(DateTime(timezone=True))

    # Relationships
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    learning_preferences = relationship("LearningPreference", back_populates="user", cascade="all, delete-orphan")
    source_integrations = relationship("SourceIntegration", back_populates="user", cascade="all, delete-orphan")

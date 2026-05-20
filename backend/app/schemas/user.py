from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    email: EmailStr
    display_name: Optional[str] = None


class UserCreate(UserBase):
    microsoft_id: str
    given_name: Optional[str] = None
    surname: Optional[str] = None


class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None
    timezone: Optional[str] = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    microsoft_id: str
    display_name: Optional[str] = None
    given_name: Optional[str] = None
    surname: Optional[str] = None
    preferences: Dict[str, Any] = {}
    timezone: str = "UTC"
    is_active: bool = True
    is_onboarded: bool = False
    created_at: datetime
    last_login_at: Optional[datetime] = None
    last_sync_at: Optional[datetime] = None


class UserPreferences(BaseModel):
    theme: str = "light"
    notifications_enabled: bool = True
    email_notifications: bool = True
    auto_categorize: bool = True
    auto_prioritize: bool = True
    sync_interval_hours: int = 2
    default_view: str = "kanban"
    language: str = "en"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse

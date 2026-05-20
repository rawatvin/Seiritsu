"""
Demo Authentication Endpoint
Allows testing the app without Microsoft OAuth
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import jwt

from app.core.config import settings
from app.db.base import get_db
from app.models.user import User

router = APIRouter()


class DemoLoginRequest(BaseModel):
    email: EmailStr
    name: str = "Demo User"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


@router.post("/demo-login", response_model=TokenResponse)
async def demo_login(
    login_data: DemoLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Demo login - creates or gets a demo user without OAuth
    Perfect for testing without Microsoft Azure access
    """

    # Check if user exists
    result = await db.execute(
        select(User).where(User.email == login_data.email)
    )
    user = result.scalar_one_or_none()

    # Create user if doesn't exist
    if not user:
        user = User(
            email=login_data.email,
            name=login_data.name,
            microsoft_id=f"demo_{login_data.email}",
            access_token="demo_token",
            refresh_token="demo_refresh",
            token_expires_at=datetime.utcnow() + timedelta(days=365)
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    # Create JWT token
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(days=7)
    }

    access_token = jwt.encode(
        token_data,
        settings.JWT_SECRET_KEY,
        algorithm="HS256"
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    )


@router.get("/demo-status")
async def demo_status():
    """Check if demo mode is available"""
    return {
        "demo_mode_enabled": True,
        "message": "Demo authentication available - no Azure setup required!"
    }

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from jose import jwt
from typing import Optional
import secrets

from app.core.config import settings
from app.db.base import get_db
from app.models import User
from app.schemas.user import UserResponse, TokenResponse, UserCreate
from app.integrations.microsoft_graph import MicrosoftGraphClient

router = APIRouter()

# In-memory state storage (use Redis in production)
_auth_states = {}


@router.get("/login")
async def login():
    """Initiate Microsoft OAuth2 login flow"""
    state = secrets.token_urlsafe(32)
    _auth_states[state] = datetime.utcnow()

    auth_url = MicrosoftGraphClient.get_auth_url(state)
    return {"auth_url": auth_url, "state": state}


@router.get("/callback")
async def auth_callback(
    code: str,
    state: str,
    db: AsyncSession = Depends(get_db),
):
    """Handle Microsoft OAuth2 callback"""
    # Verify state
    if state not in _auth_states:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid state parameter"
        )

    # Clean up old states
    _auth_states.pop(state)

    try:
        # Exchange code for token
        token_data = await MicrosoftGraphClient.get_token_from_code(code)

        # Get user profile
        graph_client = MicrosoftGraphClient(token_data["access_token"])
        profile = await graph_client.get_user_profile()

        # Find or create user
        query = select(User).where(User.microsoft_id == profile["id"])
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                microsoft_id=profile["id"],
                email=profile["userPrincipalName"],
                display_name=profile.get("displayName"),
                given_name=profile.get("givenName"),
                surname=profile.get("surname"),
            )
            db.add(user)

        # Update tokens
        user.access_token = token_data["access_token"]
        user.refresh_token = token_data.get("refresh_token")
        user.token_expires_at = datetime.utcnow() + timedelta(seconds=token_data["expires_in"])
        user.last_login_at = datetime.utcnow()

        await db.commit()
        await db.refresh(user)

        # Generate JWT for our app
        jwt_token = create_access_token(user.id)

        # Redirect to frontend with token
        frontend_url = settings.cors_origins[0]
        return RedirectResponse(
            url=f"{frontend_url}/auth/callback?token={jwt_token}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user: User = Depends(get_current_user_dep),
):
    """Get current user profile"""
    return current_user


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user_dep),
    db: AsyncSession = Depends(get_db),
):
    """Logout user"""
    current_user.access_token = None
    current_user.refresh_token = None
    await db.commit()
    return {"message": "Logged out successfully"}


def create_access_token(user_id: str) -> str:
    """Create JWT access token"""
    expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expiration_minutes)
    to_encode = {
        "sub": str(user_id),
        "exp": expire,
    }
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


async def get_current_user_dep(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Dependency to get current user from JWT token"""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

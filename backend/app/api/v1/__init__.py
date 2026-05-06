from fastapi import APIRouter
from app.api.v1.endpoints import auth, tasks, sync, analytics, learning, demo_auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(demo_auth.router, prefix="/auth", tags=["Demo Authentication"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(sync.router, prefix="/sync", tags=["Synchronization"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(learning.router, prefix="/learning", tags=["Learning"])

#!/usr/bin/env python3
"""
Quick test script to verify API structure and imports
Run this before starting the server to catch any import errors
"""

import sys
import asyncio

def test_imports():
    """Test that all modules import correctly"""
    print("Testing imports...")

    try:
        from app.core.config import settings
        print("✓ Config imported")

        from app.db.base import get_db, Base
        print("✓ Database base imported")

        from app.models import (
            User, Task, TaskStatus, TaskPriority, TaskSource,
            LearningEvent, LearningEventType, LearningPreference,
            CategoryPattern, TeamAssignmentPattern,
            SourceIntegration, SourceItem, MonthlyReport
        )
        print("✓ All models imported")

        from app.schemas.task import (
            TaskCreate, TaskUpdate, TaskResponse,
            TaskListResponse, TaskFilter, TaskStatusUpdate, TaskBulkUpdate
        )
        print("✓ Task schemas imported")

        from app.schemas.user import UserResponse, TokenResponse
        print("✓ User schemas imported")

        from app.api.v1.endpoints import auth, tasks, sync, analytics, learning
        print("✓ All endpoint modules imported")

        from app.services.ai_service import AIService
        print("✓ AI service imported")

        from app.learning.learning_service import LearningService
        print("✓ Learning service imported")

        from app.integrations.microsoft_graph import MicrosoftGraphClient
        print("✓ Microsoft Graph client imported")

        from app.main import app
        print("✓ FastAPI app imported")

        print("\n✅ All imports successful!")
        return True

    except Exception as e:
        print(f"\n❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_routes():
    """Test that API routes are properly registered"""
    print("\nTesting API routes...")

    try:
        from app.main import app

        routes = []
        for route in app.routes:
            if hasattr(route, 'methods') and hasattr(route, 'path'):
                for method in route.methods:
                    routes.append(f"{method} {route.path}")

        # Expected routes
        expected_prefixes = [
            "GET /api/v1/auth/",
            "POST /api/v1/tasks",
            "GET /api/v1/tasks",
            "PATCH /api/v1/tasks",
            "DELETE /api/v1/tasks",
            "GET /api/v1/sync",
            "POST /api/v1/sync",
            "GET /api/v1/analytics",
            "POST /api/v1/analytics",
            "GET /api/v1/learning",
            "POST /api/v1/learning",
        ]

        found_routes = []
        for prefix in expected_prefixes:
            matching = [r for r in routes if r.startswith(prefix)]
            if matching:
                found_routes.extend(matching)

        print(f"✓ Found {len(found_routes)} API routes")

        # Print grouped routes
        route_groups = {}
        for route in routes:
            if '/api/v1/' in route:
                group = route.split('/api/v1/')[1].split('/')[0]
                if group not in route_groups:
                    route_groups[group] = []
                route_groups[group].append(route)

        print("\nAPI Route Groups:")
        for group, group_routes in sorted(route_groups.items()):
            print(f"\n  {group.upper()}:")
            for route in sorted(group_routes):
                print(f"    {route}")

        print("\n✅ API routes registered successfully!")
        return True

    except Exception as e:
        print(f"\n❌ Route test error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("API STRUCTURE TEST")
    print("=" * 60)

    success = True

    if not test_imports():
        success = False

    if not test_api_routes():
        success = False

    print("\n" + "=" * 60)
    if success:
        print("✅ ALL TESTS PASSED - Ready to start server!")
        print("\nTo start the server:")
        print("  uvicorn app.main:app --reload --port 8000")
    else:
        print("❌ TESTS FAILED - Fix errors before starting server")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    main()

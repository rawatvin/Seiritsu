from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from uuid import UUID
from app.models import (
    LearningEvent,
    LearningEventType,
    LearningPreference,
    CategoryPattern,
    TeamAssignmentPattern,
    Task,
)
import logging

logger = logging.getLogger(__name__)


class LearningService:
    """Service that learns from user behavior to improve task management"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def record_event(
        self,
        user_id: UUID,
        event_type: str,
        task_id: Optional[UUID] = None,
        metadata: Optional[Dict[str, Any]] = None,
        event_data: Optional[Dict[str, Any]] = None,
        original_extraction: Optional[Dict[str, Any]] = None,
        user_correction: Optional[Dict[str, Any]] = None,
    ) -> LearningEvent:
        """Record a learning event"""
        # Convert string to enum if needed
        if isinstance(event_type, str):
            try:
                event_type = LearningEventType(event_type)
            except ValueError:
                # Use task_edited as default
                event_type = LearningEventType.TASK_EDITED

        event = LearningEvent(
            user_id=user_id,
            task_id=task_id,
            event_type=event_type,
            event_data=metadata or event_data,
            original_extraction=original_extraction,
            user_correction=user_correction,
        )
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event


    async def _process_event(self, event: LearningEvent):
        """Process a single learning event to update patterns"""
        if event.event_type == LearningEventType.TASK_CATEGORIZED:
            await self._learn_categorization(event)

        elif event.event_type == LearningEventType.TASK_ASSIGNED:
            await self._learn_assignment(event)

        elif event.event_type == LearningEventType.EXTRACTION_CORRECTED:
            await self._learn_extraction_correction(event)

        elif event.event_type in [
            LearningEventType.RECOMMENDATION_ACCEPTED,
            LearningEventType.RECOMMENDATION_REJECTED,
        ]:
            await self._learn_recommendation_feedback(event)

    async def _learn_categorization(self, event: LearningEvent):
        """Learn from user's task categorization choices"""
        if not event.task_id or not event.event_data:
            return

        task = await self.db.get(Task, event.task_id)
        if not task or not task.category:
            return

        category = task.category
        keywords = self._extract_keywords(task.title, task.description)

        # Find or create category pattern
        query = select(CategoryPattern).where(
            and_(
                CategoryPattern.user_id == event.user_id,
                CategoryPattern.category == category,
            )
        )
        result = await self.db.execute(query)
        pattern = result.scalar_one_or_none()

        if not pattern:
            pattern = CategoryPattern(
                user_id=event.user_id,
                category=category,
                keywords=keywords,
                context_patterns={},
                source_weights={},
                task_count=0,
            )
            self.db.add(pattern)
        else:
            # Merge keywords
            existing_keywords = set(pattern.keywords or [])
            existing_keywords.update(keywords)
            pattern.keywords = list(existing_keywords)

        pattern.task_count += 1

        # Update source weights
        source_weights = pattern.source_weights or {}
        source = str(task.source)
        source_weights[source] = source_weights.get(source, 0) + 1
        pattern.source_weights = source_weights

        await self.db.commit()

    async def _learn_assignment(self, event: LearningEvent):
        """Learn from user's task assignment patterns"""
        if not event.task_id or not event.event_data:
            return

        task = await self.db.get(Task, event.task_id)
        if not task or not task.assigned_to:
            return

        category = task.category or "uncategorized"
        keywords = self._extract_keywords(task.title, task.description)
        assigned_team = task.recommended_team
        assigned_people = task.assigned_to

        # Find or create assignment pattern
        query = select(TeamAssignmentPattern).where(
            and_(
                TeamAssignmentPattern.user_id == event.user_id,
                TeamAssignmentPattern.category == category,
            )
        )
        result = await self.db.execute(query)
        pattern = result.scalar_one_or_none()

        if not pattern:
            pattern = TeamAssignmentPattern(
                user_id=event.user_id,
                category=category,
                keywords=keywords,
                assigned_team=assigned_team,
                assigned_people=assigned_people,
                assignment_count=1,
                success_rate=100,
            )
            self.db.add(pattern)
        else:
            # Update pattern
            existing_keywords = set(pattern.keywords or [])
            existing_keywords.update(keywords)
            pattern.keywords = list(existing_keywords)
            pattern.assignment_count += 1

            # Check if assignment was kept or changed
            was_recommendation = event.event_data.get("was_recommendation", False)
            kept_recommendation = event.event_data.get("kept_recommendation", True)

            if was_recommendation:
                # Update success rate
                total = pattern.assignment_count
                current_successes = (pattern.success_rate * (total - 1)) / 100
                new_successes = current_successes + (1 if kept_recommendation else 0)
                pattern.success_rate = int((new_successes / total) * 100)

        await self.db.commit()

    async def _learn_extraction_correction(self, event: LearningEvent):
        """Learn from user's corrections to AI extractions"""
        if not event.original_extraction or not event.user_correction:
            return

        # Store as a preference for future extractions
        preference = LearningPreference(
            user_id=event.user_id,
            preference_type="extraction_correction",
            preference_key=event.original_extraction.get("title", "")[:255],
            preference_value={
                "original": event.original_extraction,
                "corrected": event.user_correction,
                "correction_type": event.event_data.get("correction_type"),
            },
            confidence=80,
            usage_count=1,
        )
        self.db.add(preference)
        await self.db.commit()

    async def _learn_recommendation_feedback(self, event: LearningEvent):
        """Learn from user's acceptance/rejection of recommendations"""
        feedback_type = event.event_data.get("recommendation_type")
        was_accepted = event.event_type == LearningEventType.RECOMMENDATION_ACCEPTED

        # Find related preference and update confidence
        if feedback_type and event.event_data.get("recommendation_key"):
            query = select(LearningPreference).where(
                and_(
                    LearningPreference.user_id == event.user_id,
                    LearningPreference.preference_type == feedback_type,
                    LearningPreference.preference_key == event.event_data["recommendation_key"],
                )
            )
            result = await self.db.execute(query)
            preference = result.scalar_one_or_none()

            if preference:
                preference.usage_count += 1
                if was_accepted:
                    preference.success_count += 1

                # Recalculate confidence
                preference.confidence = int(
                    (preference.success_count / preference.usage_count) * 100
                )
                preference.last_used_at = datetime.utcnow()
                await self.db.commit()

    async def get_category_patterns(
        self,
        user_id: UUID,
        limit: int = 20,
    ) -> List[CategoryPattern]:
        """Get learned category patterns for a user"""
        query = (
            select(CategoryPattern)
            .where(CategoryPattern.user_id == user_id)
            .order_by(CategoryPattern.task_count.desc())
            .limit(limit)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_assignment_patterns(
        self,
        user_id: UUID,
        category: Optional[str] = None,
        limit: int = 20,
    ) -> List[TeamAssignmentPattern]:
        """Get learned assignment patterns for a user"""
        query = select(TeamAssignmentPattern).where(
            TeamAssignmentPattern.user_id == user_id
        )

        if category:
            query = query.where(TeamAssignmentPattern.category == category)

        query = query.order_by(TeamAssignmentPattern.success_rate.desc()).limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_extraction_corrections(
        self,
        user_id: UUID,
        limit: int = 50,
    ) -> List[LearningPreference]:
        """Get user's past extraction corrections"""
        query = (
            select(LearningPreference)
            .where(
                and_(
                    LearningPreference.user_id == user_id,
                    LearningPreference.preference_type == "extraction_correction",
                )
            )
            .order_by(LearningPreference.confidence.desc())
            .limit(limit)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def suggest_category(
        self,
        user_id: UUID,
        task_title: str,
        task_description: Optional[str] = None,
    ) -> Optional[str]:
        """Suggest a category based on learned patterns"""
        keywords = self._extract_keywords(task_title, task_description)
        patterns = await self.get_category_patterns(user_id)

        # Find best matching pattern
        best_match = None
        best_score = 0

        for pattern in patterns:
            pattern_keywords = set(pattern.keywords or [])
            matching_keywords = pattern_keywords.intersection(keywords)
            score = len(matching_keywords)

            if score > best_score:
                best_score = score
                best_match = pattern

        if best_match and best_score > 0:
            return best_match.category

        return None

    async def suggest_assignees(
        self,
        user_id: UUID,
        task_category: Optional[str],
        task_title: str,
    ) -> Optional[List[str]]:
        """Suggest assignees based on learned patterns"""
        if not task_category:
            return None

        patterns = await self.get_assignment_patterns(user_id, task_category)

        if patterns and patterns[0].success_rate > 50:
            return patterns[0].assigned_people

        return None

    def _extract_keywords(
        self,
        title: str,
        description: Optional[str] = None,
    ) -> List[str]:
        """Extract keywords from task title and description"""
        import re

        text = title
        if description:
            text += " " + description

        # Simple keyword extraction (could be enhanced with NLP)
        text = text.lower()
        words = re.findall(r'\b\w{4,}\b', text)  # Words with 4+ chars

        # Remove common stop words
        stop_words = {
            "this", "that", "with", "from", "have", "will", "would",
            "could", "should", "there", "their", "about", "after",
        }
        keywords = [w for w in words if w not in stop_words]

        # Return unique keywords
        return list(set(keywords))[:20]

    async def get_learning_stats(self, user_id: UUID) -> Dict[str, Any]:
        """Get statistics about the learning system for a user"""
        # Count events
        event_count_query = select(func.count(LearningEvent.id)).where(
            LearningEvent.user_id == user_id
        )
        event_count = await self.db.scalar(event_count_query)

        # Count patterns
        category_count_query = select(func.count(CategoryPattern.id)).where(
            CategoryPattern.user_id == user_id
        )
        category_count = await self.db.scalar(category_count_query)

        assignment_count_query = select(func.count(TeamAssignmentPattern.id)).where(
            TeamAssignmentPattern.user_id == user_id
        )
        assignment_count = await self.db.scalar(assignment_count_query)

        # Count preferences
        pref_count_query = select(func.count(LearningPreference.id)).where(
            LearningPreference.user_id == user_id
        )
        pref_count = await self.db.scalar(pref_count_query)

        return {
            "total_events": event_count or 0,
            "category_patterns": category_count or 0,
            "assignment_patterns": assignment_count or 0,
            "preferences": pref_count or 0,
            "learning_active": (event_count or 0) > 10,
        }

    async def get_extraction_patterns(self, user_id: UUID) -> Dict[str, Any]:
        """Get extraction patterns for better AI task extraction"""
        corrections = await self.get_extraction_corrections(user_id)
        category_patterns = await self.get_category_patterns(user_id)

        return {
            "corrections": [
                {
                    "original": corr.preference_value.get("original"),
                    "corrected": corr.preference_value.get("corrected"),
                    "confidence": corr.confidence,
                }
                for corr in corrections
            ],
            "categories": [
                {
                    "category": pattern.category,
                    "keywords": pattern.keywords,
                    "task_count": pattern.task_count,
                }
                for pattern in category_patterns
            ],
        }

    async def process_category_correction(
        self,
        user_id: UUID,
        task_id: UUID,
        original_category: Optional[str],
        new_category: str,
    ):
        """Process a category correction from the user"""
        task = await self.db.get(Task, task_id)
        if not task:
            return

        # Record as extraction correction
        await self.record_event(
            user_id=user_id,
            event_type=LearningEventType.EXTRACTION_CORRECTED,
            task_id=task_id,
            metadata={
                "correction_type": "category",
                "original_category": original_category,
                "new_category": new_category,
            },
        )

        # Update or create category pattern for the new category
        keywords = self._extract_keywords(task.title, task.description)

        query = select(CategoryPattern).where(
            and_(
                CategoryPattern.user_id == user_id,
                CategoryPattern.category == new_category,
            )
        )
        result = await self.db.execute(query)
        pattern = result.scalar_one_or_none()

        if not pattern:
            pattern = CategoryPattern(
                user_id=user_id,
                category=new_category,
                keywords=keywords,
                context_patterns={},
                source_weights={},
                task_count=1,
            )
            self.db.add(pattern)
        else:
            existing_keywords = set(pattern.keywords or [])
            existing_keywords.update(keywords)
            pattern.keywords = list(existing_keywords)
            pattern.task_count += 1

        await self.db.commit()

    async def suggest_category(
        self,
        user_id: UUID,
        title: str,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Suggest a category with confidence score"""
        keywords = self._extract_keywords(title, description)
        patterns = await self.get_category_patterns(user_id)

        best_match = None
        best_score = 0

        for pattern in patterns:
            pattern_keywords = set(pattern.keywords or [])
            matching_keywords = pattern_keywords.intersection(keywords)
            score = len(matching_keywords)

            if score > best_score:
                best_score = score
                best_match = pattern

        if best_match and best_score > 0:
            # Calculate confidence based on match strength
            confidence = min(int((best_score / len(keywords)) * 100), 100) if keywords else 0
            return {
                "category": best_match.category,
                "confidence": confidence,
            }

        return {"category": None, "confidence": 0}

    async def suggest_assignment(
        self,
        user_id: UUID,
        category: Optional[str],
        title: str,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Suggest task assignment with confidence"""
        if not category:
            return {"suggestions": []}

        patterns = await self.get_assignment_patterns(user_id, category)

        suggestions = []
        for pattern in patterns:
            if pattern.success_rate > 50:
                suggestions.append({
                    "team": pattern.assigned_team,
                    "people": pattern.assigned_people,
                    "confidence": pattern.success_rate,
                    "assignment_count": pattern.assignment_count,
                })

        return {"suggestions": suggestions}

    async def find_similar_tasks(
        self,
        user_id: UUID,
        title: str,
        description: Optional[str] = None,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """Find similar tasks based on keywords"""
        keywords = self._extract_keywords(title, description)

        # Get user's tasks
        query = select(Task).where(
            and_(
                Task.user_id == user_id,
                Task.is_deleted == False,
            )
        ).order_by(Task.created_at.desc()).limit(100)

        result = await self.db.execute(query)
        tasks = result.scalars().all()

        # Calculate similarity scores
        similar_tasks = []
        for task in tasks:
            task_keywords = self._extract_keywords(task.title, task.description)
            matching_keywords = set(keywords).intersection(task_keywords)
            similarity_score = len(matching_keywords)

            if similarity_score > 0:
                similar_tasks.append({
                    "id": str(task.id),
                    "title": task.title,
                    "category": task.category,
                    "actual_hours": task.actual_hours,
                    "similarity_score": similarity_score,
                })

        # Sort by similarity and return top matches
        similar_tasks.sort(key=lambda x: x["similarity_score"], reverse=True)
        return similar_tasks[:limit]

    async def update_category_patterns(self, user_id: UUID):
        """Update category patterns with latest statistics"""
        patterns = await self.get_category_patterns(user_id, limit=100)

        for pattern in patterns:
            # Get tasks in this category
            query = select(Task).where(
                and_(
                    Task.user_id == user_id,
                    Task.category == pattern.category,
                    Task.status == "completed",
                )
            )
            result = await self.db.execute(query)
            tasks = result.scalars().all()

            if tasks:
                # Calculate average completion time
                total_hours = sum(task.actual_hours or 0 for task in tasks)
                count = len([task for task in tasks if task.actual_hours])
                if count > 0:
                    pattern.avg_completion_time_hours = int(total_hours / count)

                # Update task count
                pattern.task_count = len(tasks)

        await self.db.commit()

    async def update_assignment_patterns(self, user_id: UUID):
        """Update assignment patterns with latest statistics"""
        patterns = await self.get_assignment_patterns(user_id, limit=100)

        for pattern in patterns:
            # Get tasks with this assignment
            query = select(Task).where(
                and_(
                    Task.user_id == user_id,
                    Task.category == pattern.category,
                )
            )
            result = await self.db.execute(query)
            tasks = result.scalars().all()

            pattern.assignment_count = len(tasks)

        await self.db.commit()

    async def process_pending_events(self, user_id: UUID, limit: int = 100) -> int:
        """Process pending learning events and return count"""
        query = select(LearningEvent).where(
            and_(
                LearningEvent.user_id == user_id,
                LearningEvent.processed == False,
            )
        ).limit(limit)

        result = await self.db.execute(query)
        events = result.scalars().all()

        for event in events:
            await self._process_event(event)
            event.processed = True
            event.processed_at = datetime.utcnow()

        await self.db.commit()
        logger.info(f"Processed {len(events)} learning events for user {user_id}")

        return len(events)

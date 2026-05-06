import anthropic
from typing import List, Dict, Any, Optional
from app.core.config import settings
import json
import logging

logger = logging.getLogger(__name__)


class AIService:
    """Service for AI-powered task extraction and analysis using Claude"""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = "claude-4-6-sonnet-20250829"

    async def extract_tasks_from_content(
        self,
        content: str,
        source_type: str,
        context: Optional[Dict[str, Any]] = None,
        user_patterns: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Extract actionable tasks from unstructured content

        Args:
            content: The text content to analyze
            source_type: Type of source (email, teams_chat, transcript, etc.)
            context: Additional context (sender, subject, participants, etc.)
            user_patterns: Learned patterns from user's past behavior

        Returns:
            List of extracted tasks with metadata
        """

        system_prompt = self._build_extraction_system_prompt(source_type, user_patterns)
        user_prompt = self._build_extraction_user_prompt(content, context)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
            )

            result_text = response.content[0].text
            tasks = json.loads(result_text)

            return tasks.get("tasks", [])

        except Exception as e:
            logger.error(f"Error extracting tasks: {e}")
            return []

    def _build_extraction_system_prompt(
        self,
        source_type: str,
        user_patterns: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """Build system prompt for task extraction"""

        base_prompt = """You are an expert task extraction assistant. Your job is to analyze content and identify actionable tasks.

**Guidelines:**
1. Extract ONLY clear, actionable tasks (things that require doing)
2. Don't extract informational statements or questions that don't require action
3. Include context about who might need to do it or when it's due
4. Rate urgency on a scale of 0-100 based on language cues
5. Identify deadlines or time references
6. Suggest appropriate categories for the task
7. Estimate effort if possible (in hours)

**Output Format (JSON):**
```json
{
  "tasks": [
    {
      "title": "Brief, actionable task title",
      "description": "Full context and details",
      "urgency_score": 0-100,
      "confidence": 0-100,
      "deadline": "ISO datetime or null",
      "estimated_hours": number or null,
      "suggested_category": "category name",
      "keywords": ["relevant", "keywords"],
      "assigned_to": ["person names if mentioned"],
      "reasoning": "Why this is a task"
    }
  ]
}
```
"""

        # Add source-specific guidance
        source_guidance = {
            "email": "\n**Email-specific:** Look for action requests, follow-ups, commitments, deadlines in signatures.",
            "teams_chat": "\n**Teams Chat-specific:** Look for @mentions, direct requests, commitments in conversation.",
            "meeting_transcript": "\n**Transcript-specific:** Look for action items, decisions, volunteers, 'I will', 'We need to'.",
            "sharepoint": "\n**SharePoint-specific:** Look for task assignments, comments requesting action, tagged items.",
        }

        base_prompt += source_guidance.get(source_type, "")

        # Add user pattern learning
        if user_patterns:
            pattern_text = "\n\n**User's Learned Patterns:**\n"
            pattern_text += "Consider these patterns from the user's past task management:\n"
            for pattern in user_patterns[:5]:  # Top 5 patterns
                pattern_text += f"- Category '{pattern.get('category')}': keywords {pattern.get('keywords')}\n"
            base_prompt += pattern_text

        return base_prompt

    def _build_extraction_user_prompt(
        self,
        content: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Build user prompt with content and context"""

        prompt = "Analyze the following content and extract actionable tasks:\n\n"

        if context:
            prompt += "**Context:**\n"
            if context.get("sender"):
                prompt += f"From: {context['sender']}\n"
            if context.get("subject"):
                prompt += f"Subject: {context['subject']}\n"
            if context.get("participants"):
                prompt += f"Participants: {', '.join(context['participants'])}\n"
            if context.get("date"):
                prompt += f"Date: {context['date']}\n"
            prompt += "\n"

        prompt += f"**Content:**\n{content}\n\n"
        prompt += "Extract tasks in JSON format as specified."

        return prompt

    async def categorize_task(
        self,
        task_title: str,
        task_description: Optional[str],
        user_categories: List[str],
        category_patterns: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Categorize a task based on learned patterns"""

        system_prompt = "You are a task categorization expert. Categorize the given task into one of the provided categories based on patterns."

        user_prompt = f"""Task: {task_title}
Description: {task_description or 'N/A'}

Available categories: {', '.join(user_categories)}

"""
        if category_patterns:
            user_prompt += "\nLearned patterns:\n"
            for pattern in category_patterns[:10]:
                user_prompt += f"- {pattern.get('category')}: {', '.join(pattern.get('keywords', []))}\n"

        user_prompt += "\nRespond with JSON: {\"category\": \"category_name\", \"confidence\": 0-100, \"reasoning\": \"brief explanation\"}"

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
                temperature=0.2,
            )

            result = json.loads(response.content[0].text)
            return result

        except Exception as e:
            logger.error(f"Error categorizing task: {e}")
            return {"category": "Uncategorized", "confidence": 0}

    async def recommend_assignees(
        self,
        task_title: str,
        task_description: Optional[str],
        task_category: Optional[str],
        org_structure: Dict[str, Any],
        assignment_patterns: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """Recommend people or teams to assign the task to"""

        system_prompt = "You are an expert at recommending task assignments based on organizational context and patterns."

        user_prompt = f"""Task: {task_title}
Description: {task_description or 'N/A'}
Category: {task_category or 'N/A'}

**Organization Context:**
"""
        if org_structure.get("teams"):
            user_prompt += f"\nTeams: {', '.join([t.get('displayName', '') for t in org_structure['teams'][:10]])}"

        if org_structure.get("manager"):
            user_prompt += f"\nManager: {org_structure['manager'].get('displayName', 'N/A')}"

        if assignment_patterns:
            user_prompt += "\n\n**Past Assignment Patterns:**\n"
            for pattern in assignment_patterns[:5]:
                user_prompt += f"- {pattern.get('category')}: assigned to {pattern.get('assigned_team')} ({pattern.get('success_rate')}% kept)\n"

        user_prompt += """\n\nRecommend up to 3 people or teams with confidence scores.
Respond with JSON: {\"recommendations\": [{\"name\": \"person/team\", \"type\": \"person|team\", \"confidence\": 0-100, \"reasoning\": \"why\"}]}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
                temperature=0.3,
            )

            result = json.loads(response.content[0].text)
            return result.get("recommendations", [])

        except Exception as e:
            logger.error(f"Error recommending assignees: {e}")
            return []

    async def generate_monthly_insights(
        self,
        task_statistics: Dict[str, Any],
        time_investment: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate insights and automation recommendations for monthly report"""

        system_prompt = """You are an expert at analyzing work patterns and finding automation opportunities.
Provide actionable insights about task distribution, time investment, and areas for automation."""

        user_prompt = f"""Analyze this month's task data:

**Task Statistics:**
{json.dumps(task_statistics, indent=2)}

**Time Investment:**
{json.dumps(time_investment, indent=2)}

Provide:
1. Key insights about how time was spent
2. Patterns in task categories and sources
3. Specific automation opportunities (what tasks are repetitive?)
4. Time-saving recommendations
5. Areas where delegation might help

Respond with JSON:
```json
{{
  "insights": ["insight 1", "insight 2", ...],
  "automation_opportunities": [
    {{
      "pattern": "description of repetitive pattern",
      "frequency": "how often",
      "time_saved_hours": estimated_hours,
      "recommendation": "specific automation suggestion"
    }}
  ],
  "time_saving_tips": ["tip 1", "tip 2", ...],
  "delegation_opportunities": ["opportunity 1", ...]
}}
```"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
                temperature=0.4,
            )

            result = json.loads(response.content[0].text)
            return result

        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            return {
                "insights": [],
                "automation_opportunities": [],
                "time_saving_tips": [],
                "delegation_opportunities": [],
            }

    async def brainstorm_time_savings(
        self,
        user_context: str,
        task_patterns: Dict[str, Any],
        constraints: Optional[str] = None,
    ) -> List[str]:
        """Interactive brainstorming for time-saving ideas"""

        system_prompt = """You are a productivity coach specializing in time management and automation.
Have a creative, practical conversation about saving time."""

        user_prompt = f"""Help me brainstorm ways to save time based on my work patterns:

{user_context}

**My Task Patterns:**
{json.dumps(task_patterns, indent=2)}

"""
        if constraints:
            user_prompt += f"\n**Constraints:**\n{constraints}\n"

        user_prompt += "\nProvide 5-7 creative, actionable ideas as a JSON array of strings."

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
                temperature=0.7,
            )

            ideas = json.loads(response.content[0].text)
            return ideas if isinstance(ideas, list) else []

        except Exception as e:
            logger.error(f"Error brainstorming: {e}")
            return []

    async def extract_task(
        self,
        content: str,
        source_type: str,
        user_patterns: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Extract a single task from content"""

        system_prompt = """You are a task extraction assistant. Analyze content and extract actionable task information.

**Output Format (JSON):**
{
  "is_actionable": true/false,
  "title": "Task title",
  "description": "Full description",
  "priority": "low|medium|high|urgent",
  "urgency_score": 0-100,
  "confidence": 0-100,
  "deadline": "ISO datetime or null",
  "estimated_hours": number or null,
  "category": "suggested category",
  "tags": ["tag1", "tag2"],
  "reasoning": "Why this is/isn't actionable"
}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                messages=[{"role": "user", "content": f"Extract task from:\n\n{content}"}],
                temperature=0.3,
            )

            result = json.loads(response.content[0].text)
            return result

        except Exception as e:
            logger.error(f"Error extracting task: {e}")
            return {
                "is_actionable": False,
                "confidence": 0,
                "reasoning": f"Error: {str(e)}"
            }

    async def generate_monthly_insights(
        self,
        year: int,
        month: int,
        task_stats: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate monthly insights from task statistics"""

        system_prompt = """You are an expert at analyzing work patterns and productivity.
Provide actionable insights about task completion, time management, and automation opportunities."""

        user_prompt = f"""Analyze tasks for {year}-{month:02d}:

**Statistics:**
{json.dumps(task_stats, indent=2)}

Provide:
1. Key insights (3-5 bullet points)
2. Automation suggestions (tasks that repeat)
3. Repetitive patterns found
4. Time-saving opportunities

Respond with JSON:
{{
  "insights": ["insight 1", "insight 2"],
  "automation_suggestions": [
    {{"pattern": "description", "frequency": "weekly", "time_saved": 2}}
  ],
  "repetitive_patterns": [
    {{"description": "pattern", "occurrence_count": 5}}
  ],
  "time_saving_opportunities": [
    {{"opportunity": "description", "estimated_hours_saved": 3}}
  ]
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
                temperature=0.4,
            )

            result = json.loads(response.content[0].text)
            return result

        except Exception as e:
            logger.error(f"Error generating monthly insights: {e}")
            return {
                "insights": [],
                "automation_suggestions": [],
                "repetitive_patterns": [],
                "time_saving_opportunities": [],
            }

    async def brainstorm_time_savings(
        self,
        user_message: str,
        task_summary: Dict[str, Any],
        additional_context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Interactive brainstorming session for time-saving ideas"""

        system_prompt = """You are a productivity coach helping users find time-saving opportunities.
Be conversational, practical, and creative in your suggestions."""

        user_prompt = f"""User question: {user_message}

**Task Summary:**
{json.dumps(task_summary, indent=2)}

**Additional Context:**
{json.dumps(additional_context, indent=2)}

Provide a helpful response with specific suggestions and follow-up questions.

Respond with JSON:
{{
  "response": "conversational response text",
  "suggestions": [
    {{"suggestion": "specific idea", "estimated_time_saved": "2h/week", "difficulty": "easy|medium|hard"}}
  ],
  "follow_up_questions": ["question 1", "question 2"]
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1536,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
                temperature=0.7,
            )

            result = json.loads(response.content[0].text)
            return result

        except Exception as e:
            logger.error(f"Error in brainstorming: {e}")
            return {
                "response": "I'm having trouble generating suggestions right now. Please try again.",
                "suggestions": [],
                "follow_up_questions": [],
            }

<<<<<<< HEAD
"""
Health Agent – fitness, nutrition, wellness queries.
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.services.ai_service import AIService

SYSTEM_PROMPT = """You are a knowledgeable health and wellness coach AI.
You provide evidence-based advice on exercise, nutrition, sleep, and mental wellness.
Always recommend consulting a doctor for medical conditions or symptoms."""


class HealthAgent:
    def __init__(self, db: AsyncSession, user: User):
        self.db = db
        self.user = user
        self.ai = AIService()

    async def run(self, message: str, context: Optional[dict] = None) -> str:
        return await self.ai.complete(system=SYSTEM_PROMPT, user=message)
=======
from typing import Any
from loguru import logger

from app.services.ai_service import ai_service


SYSTEM_PROMPT = """You are a holistic health and wellness coach with expertise in sleep science,
nutrition, exercise physiology, and stress management. Provide evidence-based, personalized
recommendations. Always encourage healthy habits and remind users to consult a doctor for
medical concerns. User context: {context}"""


class HealthAgent:
    """Handles sleep, exercise, nutrition, stress, and wellness queries."""

    name = "health"
    keywords = ["sleep", "exercise", "diet", "stress", "calories", "water", "workout",
                "tired", "energy", "health", "weight", "steps", "heart", "burnout"]

    async def run(self, user_id: str, query: str, context: dict[str, Any]) -> dict[str, Any]:
        logger.info(f"HealthAgent processing query for user={user_id}")

        system = SYSTEM_PROMPT.format(context=self._summarize_context(context))
        response_text = await ai_service.chat(
            messages=[{"role": "user", "content": query}],
            system=system,
            temperature=0.4,
        )
        return {
            "agent": self.name,
            "content": response_text,
            "confidence": 0.91,
            "actions": self._extract_actions(response_text),
        }

    def _summarize_context(self, context: dict) -> str:
        habits = context.get("habit_patterns", [])
        return (
            f"User has {len(habits)} recent habit entries. "
            "Focus on practical, science-backed advice."
        )

    def _extract_actions(self, text: str) -> list[str]:
        lines = text.split("\n")
        return [l.strip("•- ").strip() for l in lines if l.strip().startswith(("-", "•", "*"))][:5]

    def matches(self, query: str) -> bool:
        q = query.lower()
        return any(kw in q for kw in self.keywords)
>>>>>>> 7c6fe786d0ebce90909c90ce7f1ac9867d4e86fd

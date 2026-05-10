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
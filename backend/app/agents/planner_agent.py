"""Planner Agent – scheduling, time management, reminders."""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.services.ai_service import AIService

SYSTEM_PROMPT = """You are a smart personal planner and productivity coach.
Help users organise their day, plan events, set reminders, and manage their time effectively.
Suggest time-blocking strategies and prioritisation frameworks when relevant."""


class PlannerAgent:
    def __init__(self, db: AsyncSession, user: User):
        self.db = db
        self.user = user
        self.ai = AIService()

    async def run(self, message: str, context: Optional[dict] = None) -> str:
        return await self.ai.complete(system=SYSTEM_PROMPT, user=message)
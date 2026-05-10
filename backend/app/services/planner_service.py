"""Planner Service – event/calendar management."""
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.ai_service import AIService


class PlannerService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.ai = AIService()

    async def list_events(self, user_id: int) -> List[dict]:
        return []

    async def create_event(self, user_id: int, title: str, date: str, time: str, notes: str) -> dict:
        return {"created": True, "title": title, "date": date, "time": time, "notes": notes}

    async def get_today_plan(self, user_id: int) -> dict:
        return {"events": [], "tasks": [], "reminders": []}

    async def ai_suggest_schedule(self, user_id: int) -> dict:
        suggestion = await self.ai.complete(
            system="You are a productivity and scheduling expert.",
            user="Suggest an optimal daily schedule for a knowledge worker.",
        )
        return {"suggestion": suggestion}
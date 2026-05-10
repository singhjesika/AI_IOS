"""Health Service – fitness and wellness tracking."""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.ai_service import AIService


class HealthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.ai = AIService()

    async def get_summary(self, user_id: int) -> dict:
        return {"steps": 0, "calories": 0, "sleep_hours": 0, "water_ml": 0}

    async def log_metric(self, user_id: int, metric: str, value: float, unit: str) -> dict:
        return {"logged": True, "metric": metric, "value": value, "unit": unit}

    async def get_logs(self, user_id: int, metric: Optional[str], limit: int) -> List[dict]:
        return []

    async def get_recommendations(self, user_id: int) -> dict:
        summary = await self.get_summary(user_id)
        prompt = f"User health summary: {summary}. Give 3 personalised health recommendations."
        recs = await self.ai.complete(system="You are a health coach.", user=prompt)
        return {"recommendations": recs}
"""Analytics Service – usage statistics and dashboard data."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.memory import Memory


class AnalyticsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_dashboard(self, user_id: int) -> dict:
        msg_count = await self.db.execute(
            select(func.count(Memory.id)).where(Memory.user_id == user_id)
        )
        return {
            "total_messages": msg_count.scalar() or 0,
            "agents_used": [],
            "streak_days": 0,
        }

    async def get_usage(self, user_id: int, days: int) -> dict:
        return {"days": days, "messages_per_day": []}

    async def get_agent_usage(self, user_id: int) -> dict:
        return {"agent_counts": {}}
"""Travel Agent – trip planning, destinations, itineraries."""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.services.ai_service import AIService

SYSTEM_PROMPT = """You are an expert travel planner and concierge.
Help users plan trips, create itineraries, suggest destinations, find hotels, and navigate visa requirements.
Provide practical tips on local culture, safety, and budget management."""


class TravelAgent:
    def __init__(self, db: AsyncSession, user: User):
        self.db = db
        self.user = user
        self.ai = AIService()

    async def run(self, message: str, context: Optional[dict] = None) -> str:
        return await self.ai.complete(system=SYSTEM_PROMPT, user=message)
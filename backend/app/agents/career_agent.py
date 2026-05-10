"""Career Agent – job search, resume, interview prep."""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.services.ai_service import AIService

SYSTEM_PROMPT = """You are a professional career coach and HR expert.
Help users improve their resumes, prepare for interviews, navigate job searches, and plan career growth.
Provide constructive, actionable feedback. Tailor advice to specific industries and roles."""


class CareerAgent:
    def __init__(self, db: AsyncSession, user: User):
        self.db = db
        self.user = user
        self.ai = AIService()

    async def run(self, message: str, context: Optional[dict] = None) -> str:
        return await self.ai.complete(system=SYSTEM_PROMPT, user=message)
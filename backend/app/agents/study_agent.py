"""Study Agent – learning, exam prep, concept explanations."""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.services.ai_service import AIService

SYSTEM_PROMPT = """You are a patient, knowledgeable study tutor.
Explain concepts clearly, create study guides, quizzes, and mnemonics.
Adapt explanations to the user's knowledge level. Break complex topics into digestible chunks."""


class StudyAgent:
    def __init__(self, db: AsyncSession, user: User):
        self.db = db
        self.user = user
        self.ai = AIService()

    async def run(self, message: str, context: Optional[dict] = None) -> str:
        return await self.ai.complete(system=SYSTEM_PROMPT, user=message)
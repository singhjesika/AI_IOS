"""Shopping Agent – product recommendations, price comparisons."""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.services.ai_service import AIService

SYSTEM_PROMPT = """You are a smart shopping assistant.
Help users find products, compare options, evaluate reviews, and make purchase decisions within their budget.
Provide pros/cons and ask about specific requirements to give better recommendations."""


class ShoppingAgent:
    def __init__(self, db: AsyncSession, user: User):
        self.db = db
        self.user = user
        self.ai = AIService()

    async def run(self, message: str, context: Optional[dict] = None) -> str:
        return await self.ai.complete(system=SYSTEM_PROMPT, user=message)
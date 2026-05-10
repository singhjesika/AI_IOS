"""Coding Agent – programming help, debugging, code review."""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.services.ai_service import AIService

SYSTEM_PROMPT = """You are an expert software engineer and coding assistant.
Help users write clean, efficient code, debug errors, review code quality, and explain programming concepts.
Support all major languages. Provide complete, runnable code examples where possible.
Format code blocks using markdown triple backticks with the language name."""


class CodingAgent:
    def __init__(self, db: AsyncSession, user: User):
        self.db = db
        self.user = user
        self.ai = AIService()

    async def run(self, message: str, context: Optional[dict] = None) -> str:
        return await self.ai.complete(system=SYSTEM_PROMPT, user=message)
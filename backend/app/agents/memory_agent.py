"""Memory Agent – recall saved notes and conversation history."""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.services.ai_service import AIService
from app.services.memory_service import MemoryService

SYSTEM_PROMPT = """You are a memory and note-taking assistant.
Help users recall past conversations, saved notes, and important information they asked you to remember.
Be concise and precise when recalling information."""


class MemoryAgent:
    def __init__(self, db: AsyncSession, user: User):
        self.db = db
        self.user = user
        self.ai = AIService()
        self.memory_svc = MemoryService(db)

    async def run(self, message: str, context: Optional[dict] = None) -> str:
        history = await self.memory_svc.get_history(self.user.id, limit=20)
        history_text = "\n".join(
            [f"{h['role'].upper()}: {h['content']}" for h in history]
        )
        enhanced_message = f"User's recent history:\n{history_text}\n\nUser says: {message}"
        return await self.ai.complete(system=SYSTEM_PROMPT, user=enhanced_message)
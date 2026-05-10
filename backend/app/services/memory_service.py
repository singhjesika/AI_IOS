"""
Memory Service – persist and retrieve chat history.
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.models.memory import Memory


class MemoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_message(self, user_id: int, role: str, content: str) -> Memory:
        msg = Memory(user_id=user_id, role=role, content=content)
        self.db.add(msg)
        await self.db.commit()
        await self.db.refresh(msg)
        return msg

    async def get_history(self, user_id: int, limit: int = 20) -> List[dict]:
        result = await self.db.execute(
            select(Memory)
            .where(Memory.user_id == user_id)
            .order_by(Memory.created_at.desc())
            .limit(limit)
        )
        rows = result.scalars().all()
        return [
            {"role": m.role, "content": m.content, "created_at": str(m.created_at)}
            for m in reversed(rows)
        ]

    async def clear_history(self, user_id: int) -> None:
        await self.db.execute(delete(Memory).where(Memory.user_id == user_id))
        await self.db.commit()
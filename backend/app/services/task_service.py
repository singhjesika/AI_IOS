"""
Task Service – CRUD for tasks.
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_tasks(self, user_id: int) -> List[Task]:
        result = await self.db.execute(
            select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
        )
        return result.scalars().all()

    async def create_task(self, user_id: int, payload: TaskCreate) -> Task:
        task = Task(user_id=user_id, **payload.model_dump())
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def get_task(self, task_id: int, user_id: int) -> Optional[Task]:
        result = await self.db.execute(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def update_task(self, task_id: int, user_id: int, payload: TaskUpdate) -> Optional[Task]:
        task = await self.get_task(task_id, user_id)
        if not task:
            return None
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete_task(self, task_id: int, user_id: int) -> bool:
        task = await self.get_task(task_id, user_id)
        if not task:
            return False
        await self.db.delete(task)
        await self.db.commit()
        return True
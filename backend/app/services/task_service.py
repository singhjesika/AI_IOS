<<<<<<< HEAD
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
=======
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from fastapi import HTTPException, status
from datetime import datetime, timezone

from app.models.task_model import Task, TaskStatus, Priority
from app.schemas.task_schemas import TaskCreate, TaskUpdate, TaskFilter
from app.utils.helper import paginate


class TaskService:

    @staticmethod
    async def create_task(db: AsyncSession, owner_id: str, payload: TaskCreate) -> Task:
        task = Task(owner_id=owner_id, **payload.model_dump())
        db.add(task)
        await db.flush()
        await db.refresh(task)
        return task

    @staticmethod
    async def get_task(db: AsyncSession, task_id: str, owner_id: str) -> Task:
        result = await db.execute(
            select(Task).where(Task.id == task_id, Task.owner_id == owner_id)
        )
        task = result.scalar_one_or_none()
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return task

    @staticmethod
    async def list_tasks(
        db: AsyncSession,
        owner_id: str,
        filters: TaskFilter,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Task], int]:
        conditions = [Task.owner_id == owner_id]
        if filters.status:
            conditions.append(Task.status == filters.status)
        if filters.priority:
            conditions.append(Task.priority == filters.priority)
        if filters.category:
            conditions.append(Task.category == filters.category)
        if filters.due_before:
            conditions.append(Task.due_date <= filters.due_before)
        where_clause = and_(*conditions)
        count_result = await db.execute(select(func.count()).where(where_clause).select_from(Task))
        total = count_result.scalar_one()
        pg = paginate(page, page_size)
        result = await db.execute(
            select(Task)
            .where(where_clause)
            .order_by(Task.due_date.asc().nullslast(), Task.created_at.desc())
            .offset(pg["offset"])
            .limit(pg["limit"])
        )
        tasks = result.scalars().all()
        return list(tasks), total

    @staticmethod
    async def update_task(db: AsyncSession, task: Task, payload: TaskUpdate) -> Task:
        updates = payload.model_dump(exclude_none=True)
        if updates.get("status") == TaskStatus.COMPLETED and not task.completed_at:
            updates["completed_at"] = datetime.now(timezone.utc)
        for field, value in updates.items():
            setattr(task, field, value)
        await db.flush()
        await db.refresh(task)
        return task

    @staticmethod
    async def delete_task(db: AsyncSession, task: Task) -> None:
        await db.delete(task)
        await db.flush()

    @staticmethod
    async def bulk_complete(db: AsyncSession, task_ids: list[str], owner_id: str) -> int:
        result = await db.execute(
            select(Task).where(Task.id.in_(task_ids), Task.owner_id == owner_id)
        )
        tasks = result.scalars().all()
        now = datetime.now(timezone.utc)
        for t in tasks:
            t.status = TaskStatus.COMPLETED
            t.completed_at = now
        await db.flush()
        return len(tasks)
>>>>>>> 7c6fe786d0ebce90909c90ce7f1ac9867d4e86fd

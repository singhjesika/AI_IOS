"""
Task management routes (CRUD).
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter()


@router.get("/", response_model=List[TaskRead])
async def list_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    svc = TaskService(db)
    return await svc.list_tasks(current_user.id)


@router.post("/", response_model=TaskRead, status_code=201)
async def create_task(
    payload: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    svc = TaskService(db)
    return await svc.create_task(current_user.id, payload)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    svc = TaskService(db)
    task = await svc.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    svc = TaskService(db)
    task = await svc.update_task(task_id, current_user.id, payload)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    svc = TaskService(db)
    deleted = await svc.delete_task(task_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
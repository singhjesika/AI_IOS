<<<<<<< HEAD
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
=======
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.services.task_service import TaskService
from app.services.ai_service import ai_service
from app.models.task_model import Priority, TaskStatus, Task
from app.schemas.task_schemas import (
    TaskCreate, TaskUpdate, TaskFilter,
    TaskResponse, TaskListResponse, AISuggestRequest,
)
from app.api.routes.user import get_current_user
from app.models.user_model import User
>>>>>>> 7c6fe786d0ebce90909c90ce7f1ac9867d4e86fd

router = APIRouter()


<<<<<<< HEAD
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
=======
#------task belongs to current user ───────────────────────────────
async def get_owned_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Task:
    return await TaskService.get_task(db, task_id, current_user.id)


# ── CRUD ──────────────────────────────────────────────────────────────────────
@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    payload: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await TaskService.create_task(db, current_user.id, payload)


@router.get("/", response_model=TaskListResponse)
async def list_tasks(
    status_filter: Optional[TaskStatus] = Query(None, alias="status"),
    priority: Optional[Priority] = Query(None),
    category: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    filters = TaskFilter(status=status_filter, priority=priority, category=category)
    tasks, total = await TaskService.list_tasks(db, current_user.id, filters, page, page_size)
    return TaskListResponse(items=tasks, total=total, page=page, page_size=page_size)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task: Task = Depends(get_owned_task)):
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    payload: TaskUpdate,
    task: Task = Depends(get_owned_task),
    db: AsyncSession = Depends(get_db),
):
    return await TaskService.update_task(db, task, payload)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task: Task = Depends(get_owned_task),
    db: AsyncSession = Depends(get_db),
):
    await TaskService.delete_task(db, task)


# ── Bulk operations ───────────────────────────────────────────────────────────
@router.post("/bulk/complete", status_code=status.HTTP_200_OK)
async def bulk_complete(
    task_ids: list[str],
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    count = await TaskService.bulk_complete(db, task_ids, current_user.id)
    return {"completed": count}


# ── AI-powered endpoints ──────────────────────────────────────────────────────
@router.post("/ai/suggest", response_model=list[TaskResponse], status_code=status.HTTP_201_CREATED)
async def ai_suggest_tasks(
    payload: AISuggestRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    
    suggested = await ai_service.suggest_tasks(payload.goal, payload.agent_type)
    created: list[Task] = []
    for s in suggested:
        from app.schemas.task_model import TaskCreate
        from app.models.task_model import Priority
        try:
            tc = TaskCreate(
                title=s.get("title", "Untitled Task"),
                description=s.get("description"),
                priority=Priority(s.get("priority", "medium")),
                estimated_minutes=int(s.get("estimated_minutes", 30)),
                category=s.get("category"),
            )
            task = await TaskService.create_task(db, current_user.id, tc)
            task.ai_suggested = True
            await db.flush()
            await db.refresh(task)
            created.append(task)
        except Exception:
            continue          
    return created


@router.get("/ai/insight", response_model=dict)
async def daily_insight(current_user: User = Depends(get_current_user)):
    """Generate a personalized daily productivity insight for the current user."""
    context = {
        "user": current_user.full_name,
        "productivity_goal": current_user.productivity_goal,
        "timezone": current_user.timezone,
        "wake_time": current_user.preferred_wake_time,
    }
    insight = await ai_service.generate_daily_insight(context)
    return {"insight": insight, "user": current_user.full_name}
>>>>>>> 7c6fe786d0ebce90909c90ce7f1ac9867d4e86fd

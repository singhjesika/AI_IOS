"""
Planner / calendar routes.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.services.planner_service import PlannerService

router = APIRouter()


@router.get("/events")
async def list_events(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    svc = PlannerService(db)
    return await svc.list_events(current_user.id)


@router.post("/events")
async def create_event(
    title: str,
    date: str,
    time: str = None,
    notes: str = "",
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    svc = PlannerService(db)
    return await svc.create_event(current_user.id, title, date, time, notes)


@router.get("/today")
async def today_plan(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    svc = PlannerService(db)
    return await svc.get_today_plan(current_user.id)


@router.get("/suggest")
async def suggest_schedule(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    svc = PlannerService(db)
    return await svc.ai_suggest_schedule(current_user.id)
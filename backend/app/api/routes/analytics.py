"""
Analytics / dashboard statistics routes.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.services.analytics_service import AnalyticsService

router = APIRouter()


@router.get("/dashboard")
async def dashboard_stats(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    svc = AnalyticsService(db)
    return await svc.get_dashboard(current_user.id)


@router.get("/usage")
async def usage_stats(
    days: int = 7,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    svc = AnalyticsService(db)
    return await svc.get_usage(current_user.id, days)


@router.get("/agents")
async def agent_usage(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    svc = AnalyticsService(db)
    return await svc.get_agent_usage(current_user.id)
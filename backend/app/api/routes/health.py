"""
Health tracking routes.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.services.health_service import HealthService

router = APIRouter()


@router.get("/summary")
async def health_summary(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    svc = HealthService(db)
    return await svc.get_summary(current_user.id)


@router.post("/log")
async def log_health(
    metric: str,
    value: float,
    unit: str = "",
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    svc = HealthService(db)
    return await svc.log_metric(current_user.id, metric, value, unit)


@router.get("/logs")
async def get_logs(
    metric: str = None,
    limit: int = 30,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    svc = HealthService(db)
    return await svc.get_logs(current_user.id, metric, limit)


@router.get("/recommendations")
async def health_recommendations(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    svc = HealthService(db)
    return await svc.get_recommendations(current_user.id)
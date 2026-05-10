"""
Finance API routes.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.services.finance_service import FinanceService

router = APIRouter()


@router.get("/summary")
async def finance_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    svc = FinanceService(db)
    return await svc.get_summary(current_user.id)


@router.post("/expense")
async def add_expense(
    amount: float,
    category: str,
    description: str = "",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    svc = FinanceService(db)
    return await svc.add_expense(current_user.id, amount, category, description)


@router.get("/expenses")
async def list_expenses(
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    svc = FinanceService(db)
    return await svc.list_expenses(current_user.id, limit)


@router.get("/budget")
async def get_budget(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    svc = FinanceService(db)
    return await svc.get_budget(current_user.id)


@router.get("/insights")
async def finance_insights(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """AI-generated financial insights."""
    svc = FinanceService(db)
    return await svc.generate_insights(current_user.id)
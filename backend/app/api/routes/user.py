"""
User profile routes.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserRead)
async def get_profile(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.put("/me", response_model=UserRead)
async def update_profile(
    payload: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    if payload.name is not None:
        current_user.name = payload.name
    if payload.avatar_url is not None:
        current_user.avatar_url = payload.avatar_url
    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.delete("/me", status_code=204)
async def delete_account(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    await db.delete(current_user)
    await db.commit()
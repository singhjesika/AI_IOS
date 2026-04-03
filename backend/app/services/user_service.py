from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user_model import User
from app.schemas.user_schemas import UserCreate, UserUpdate
from app.utils.helper import hash_password, verify_password, create_access_token


class UserService:

    @staticmethod
    async def create_user(db: AsyncSession, payload: UserCreate) -> User:
        # Check duplicate email
        existing = await db.execute(select(User).where(User.email == payload.email))
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )
        user = User(
            email=payload.email,
            full_name=payload.full_name,
            hashed_password=hash_password(payload.password),
            timezone=payload.timezone,
        )
        db.add(user)
        await db.flush()          # populate id without committing
        await db.refresh(user)
        return user

    @staticmethod
    async def authenticate(db: AsyncSession, email: str, password: str) -> tuple[User, str]:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
        token = create_access_token({"sub": user.id})
        return user, token

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: str) -> User:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    @staticmethod
    async def update_user(db: AsyncSession, user: User, payload: UserUpdate) -> User:
        for field, value in payload.model_dump(exclude_none=True).items():
            setattr(user, field, value)
        await db.flush()
        await db.refresh(user)
        return user

    @staticmethod
    async def change_password(
        db: AsyncSession, user: User, current: str, new: str
    ) -> None:
        if not verify_password(current, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect",
            )
        user.hashed_password = hash_password(new)
        await db.flush()

    @staticmethod
    async def deactivate(db: AsyncSession, user: User) -> None:
        user.is_active = False
        await db.flush()

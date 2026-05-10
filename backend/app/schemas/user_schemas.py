from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional


# ── Request schemas ───────────────────────────────────────────────────────────
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)
    timezone: str = "UTC"


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=255)
    timezone: Optional[str] = None
    preferred_wake_time: Optional[str] = Field(None, pattern=r"^\d{2}:\d{2}$")
    productivity_goal: Optional[int] = Field(None, ge=0, le=100)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)


# ── Response schemas ──────────────────────────────────────────────────────────
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    full_name: str
    is_active: bool
    timezone: str
    preferred_wake_time: str
    productivity_goal: int
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class UserPublic(BaseModel):
    """Minimal public-facing user info (e.g. in task owner field)."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    full_name: str
    email: str

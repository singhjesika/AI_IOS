"""User Pydantic schemas."""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    avatar_url: Optional[str] = None


class UserRead(BaseModel):
    id: int
    name: str
    email: str
    avatar_url: Optional[str] = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
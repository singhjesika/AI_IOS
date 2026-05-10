"""Task Pydantic schemas."""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskRead(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    is_completed: bool
    priority: str
    due_date: Optional[datetime]
    created_at: datetime

    model_config = {"from_attributes": True}
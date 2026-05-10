from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from app.models.task_model import Priority, TaskStatus


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    due_date: Optional[datetime] = None
    estimated_minutes: int = Field(default=30, ge=5, le=480)
    category: Optional[str] = Field(None, max_length=64)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    priority: Optional[Priority] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None
    estimated_minutes: Optional[int] = Field(None, ge=5, le=480)
    actual_minutes: Optional[int] = Field(None, ge=1)
    category: Optional[str] = Field(None, max_length=64)


class TaskFilter(BaseModel):
    status: Optional[TaskStatus] = None
    priority: Optional[Priority] = None
    category: Optional[str] = None
    due_before: Optional[datetime] = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    owner_id: str
    title: str
    description: Optional[str]
    priority: Priority
    status: TaskStatus
    due_date: Optional[datetime]
    estimated_minutes: int
    actual_minutes: Optional[int]
    ai_suggested: bool
    ai_priority_score: Optional[float]
    category: Optional[str]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]


class TaskListResponse(BaseModel):
    items: list[TaskResponse]
    total: int
    page: int
    page_size: int


class AISuggestRequest(BaseModel):
    goal: str = Field(..., min_length=5, max_length=500)
    agent_type: str = Field(default="productivity", pattern=r"^(productivity|study|health|finance)$")
 

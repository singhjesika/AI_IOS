"""
AI chat / completion routes.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.schemas.ai import ChatRequest, ChatResponse
from app.agents.orchestrator import Orchestrator
from app.services.memory_service import MemoryService

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Send a message and get an AI response routed to the correct agent."""
    orchestrator = Orchestrator(db=db, user=current_user)
    response = await orchestrator.handle(payload.message, payload.context)
    return ChatResponse(reply=response["reply"], agent=response.get("agent", "general"))


@router.get("/history")
async def chat_history(
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve recent chat history for the current user."""
    svc = MemoryService(db=db)
    history = await svc.get_history(user_id=current_user.id, limit=limit)
    return {"history": history}


@router.delete("/history")
async def clear_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Clear chat history for the current user."""
    svc = MemoryService(db=db)
    await svc.clear_history(user_id=current_user.id)
    return {"message": "History cleared"}
<<<<<<< HEAD
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
=======
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import Any

from app.agents import orchestrator
from app.api.routes.user import get_current_user
from app.models.user_model import User
>>>>>>> 7c6fe786d0ebce90909c90ce7f1ac9867d4e86fd

router = APIRouter()


<<<<<<< HEAD
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
=======
# ── Request / Response schemas (inline, lightweight) ─────────────────────────
class AgentQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    agent_override: str | None = Field(
        None,
        pattern=r"^(productivity|study|health|finance)$",
        description="Force a specific agent instead of auto-routing",
    )


class AgentQueryResponse(BaseModel):
    agent: str
    content: str
    confidence: float
    actions: list[str]


class VoiceQueryRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)


# ── Endpoints ─────────────────────────────────────────────────────────────────
@router.post("/chat", response_model=AgentQueryResponse)
async def agent_chat(
    payload: AgentQueryRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Route a natural-language query to the best AI agent.
    The orchestrator auto-detects intent (health / finance / productivity)
    or you can force a specific agent via `agent_override`.
    """
    # Build a minimal context object (extend with real habit data later)
    context: dict[str, Any] = {
        "user_id": current_user.id,
        "user_name": current_user.full_name,
        "productivity_goal": current_user.productivity_goal,
        "conversation_history": [],
        "habit_patterns": [],
    }

    if payload.agent_override:
        # Temporarily patch query so orchestrator picks the right agent
        query = f"[{payload.agent_override}] {payload.query}"
    else:
        query = payload.query

    result = await orchestrator.route(current_user.id, query, context)
    return AgentQueryResponse(**result)


@router.post("/voice", response_model=AgentQueryResponse)
async def voice_query(
    payload: VoiceQueryRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Same as /chat but intended for voice-to-text input from the frontend.
    The speech transcript is sent here and handled identically.
    """
    context: dict[str, Any] = {
        "user_id": current_user.id,
        "user_name": current_user.full_name,
        "productivity_goal": current_user.productivity_goal,
        "conversation_history": [],
        "habit_patterns": [],
    }
    result = await orchestrator.route(current_user.id, payload.text, context)
    return AgentQueryResponse(**result)


@router.get("/agents")
async def list_agents(_: User = Depends(get_current_user)):
    """Return the available agent types and their keyword triggers."""
    return {
        "agents": [
            {
                "name": "health",
                "description": "Sleep, exercise, nutrition, stress & wellness",
                "keywords": ["sleep", "exercise", "diet", "stress", "calories"],
            },
            {
                "name": "finance",
                "description": "Budgeting, saving, investing & expense tracking",
                "keywords": ["money", "budget", "spend", "save", "invest"],
            },
            {
                "name": "productivity",
                "description": "Task planning, focus, scheduling & goal setting (default)",
                "keywords": ["task", "focus", "schedule", "deadline", "plan"],
            },
        ]
    }
>>>>>>> 7c6fe786d0ebce90909c90ce7f1ac9867d4e86fd

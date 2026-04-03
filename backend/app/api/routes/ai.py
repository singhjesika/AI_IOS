from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import Any

from app.agents import orchestrator
from app.api.routes.user import get_current_user
from app.models.user_model import User

router = APIRouter()


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

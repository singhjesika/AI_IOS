<<<<<<< HEAD
"""
Orchestrator: classifies intent and routes to the correct specialist agent.
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.services.ai_service import AIService
from app.services.memory_service import MemoryService
from app.agents.finance_agent import FinanceAgent
from app.agents.health_agent import HealthAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.coding_agent import CodingAgent
from app.agents.study_agent import StudyAgent
from app.agents.travel_agent import TravelAgent
from app.agents.shopping_agent import ShoppingAgent
from app.agents.career_agent import CareerAgent
from app.agents.memory_agent import MemoryAgent
from app.utils.logger import logger

INTENT_KEYWORDS = {
    "finance":  ["money", "budget", "expense", "invest", "saving", "salary", "bank", "financial"],
    "health":   ["health", "workout", "sleep", "calories", "weight", "exercise", "diet", "fitness"],
    "planner":  ["plan", "schedule", "reminder", "calendar", "event", "meeting", "deadline"],
    "coding":   ["code", "bug", "function", "python", "javascript", "debug", "program", "error"],
    "study":    ["study", "learn", "exam", "topic", "explain", "course", "quiz"],
    "travel":   ["travel", "trip", "flight", "hotel", "visa", "destination", "tour"],
    "shopping": ["buy", "shop", "product", "price", "order", "cart", "deal"],
    "career":   ["job", "resume", "career", "interview", "cv", "linkedin", "hire", "salary"],
    "memory":   ["remember", "recall", "saved", "note", "history"],
}


class Orchestrator:
    def __init__(self, db: AsyncSession, user: User):
        self.db = db
        self.user = user
        self.ai_service = AIService()
        self.memory_svc = MemoryService(db)

    def _detect_intent(self, message: str) -> str:
        lower = message.lower()
        scores = {intent: 0 for intent in INTENT_KEYWORDS}
        for intent, keywords in INTENT_KEYWORDS.items():
            for kw in keywords:
                if kw in lower:
                    scores[intent] += 1
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else "general"

    def _get_agent(self, intent: str):
        agents = {
            "finance":  FinanceAgent(self.db, self.user),
            "health":   HealthAgent(self.db, self.user),
            "planner":  PlannerAgent(self.db, self.user),
            "coding":   CodingAgent(self.db, self.user),
            "study":    StudyAgent(self.db, self.user),
            "travel":   TravelAgent(self.db, self.user),
            "shopping": ShoppingAgent(self.db, self.user),
            "career":   CareerAgent(self.db, self.user),
            "memory":   MemoryAgent(self.db, self.user),
        }
        return agents.get(intent)

    async def handle(self, message: str, context: Optional[dict] = None) -> dict:
        intent = self._detect_intent(message)
        logger.info(f"Intent detected: {intent} for user {self.user.id}")

        agent = self._get_agent(intent)
        if agent:
            reply = await agent.run(message, context)
        else:
            reply = await self.ai_service.complete(
                system="You are a helpful AI assistant.",
                user=message,
            )

        await self.memory_svc.save_message(
            user_id=self.user.id,
            role="user",
            content=message,
        )
        await self.memory_svc.save_message(
            user_id=self.user.id,
            role="assistant",
            content=reply,
        )

        return {"reply": reply, "agent": intent}
=======
from app.agents.finance_agent import FinanceAgent
from app.agents.health_agent import HealthAgent
from app.agents.planner_agent import PlannerAgent

agents = {
    "finance": FinanceAgent(),
    "health": HealthAgent(),
    "planner": PlannerAgent(),
}


async def run_agent(agent_type: str, message: str, context: dict = {}) -> str:
    agent = agents.get(agent_type)
    if not agent:
        return f"Agent '{agent_type}' not found."
    return await agent.run(message, context)
>>>>>>> 7c6fe786d0ebce90909c90ce7f1ac9867d4e86fd

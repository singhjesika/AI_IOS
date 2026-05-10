"""
Finance Agent – handles money, budgeting, investment queries.
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.services.ai_service import AIService
from app.services.finance_service import FinanceService

SYSTEM_PROMPT = """You are an expert personal finance advisor AI.
You help users with budgeting, expense tracking, savings goals, and investment basics.
Always give practical, actionable advice. Ask clarifying questions when needed.
Never give specific stock picks or regulated financial advice; recommend consulting a professional for complex decisions."""


class FinanceAgent:
    def __init__(self, db: AsyncSession, user: User):
        self.db = db
        self.user = user
        self.ai = AIService()
        self.finance_svc = FinanceService(db)

    async def run(self, message: str, context: Optional[dict] = None) -> str:
        # Pull user's financial context for grounding
        try:
            summary = await self.finance_svc.get_summary(self.user.id)
            finance_context = (
                f"User's current financial snapshot: {summary}"
            )
        except Exception:
            finance_context = ""

        system = SYSTEM_PROMPT
        if finance_context:
            system += f"\n\n{finance_context}"

        return await self.ai.complete(system=system, user=message)
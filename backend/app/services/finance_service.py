"""
Finance Service – expense tracking and budgeting logic.
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.services.ai_service import AIService


class FinanceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.ai = AIService()

    async def get_summary(self, user_id: int) -> dict:
        # Placeholder – extend with real DB model queries
        return {
            "total_expenses_this_month": 0.0,
            "budget_remaining": 0.0,
            "top_categories": [],
        }

    async def add_expense(self, user_id: int, amount: float, category: str, description: str) -> dict:
        return {
            "status": "added",
            "amount": amount,
            "category": category,
            "description": description,
        }

    async def list_expenses(self, user_id: int, limit: int) -> List[dict]:
        return []

    async def get_budget(self, user_id: int) -> dict:
        return {"monthly_budget": 0.0, "spent": 0.0, "remaining": 0.0}

    async def generate_insights(self, user_id: int) -> dict:
        summary = await self.get_summary(user_id)
        prompt = f"Here is the user's financial summary: {summary}. Give 3 actionable insights."
        insight = await self.ai.complete(
            system="You are a financial advisor AI.",
            user=prompt,
        )
        return {"insights": insight}
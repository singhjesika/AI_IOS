from typing import Any
from loguru import logger

from app.services.ai_service import ai_service


SYSTEM_PROMPT = """You are an expert personal finance coach with deep knowledge of budgeting,
investing, saving strategies, and debt management. You provide clear, actionable, and
evidence-based financial advice tailored to the user's situation.
Always be specific, practical, and supportive. Never give overly risky advice.
User context: {context}"""


class FinanceAgent:
    """Handles all finance-related AI interactions: budgets, savings, investments."""

    name = "finance"
    keywords = ["money", "budget", "spend", "save", "invest", "debt", "salary", "expense", "income"]

    async def run(self, user_id: str, query: str, context: dict[str, Any]) -> dict[str, Any]:
        logger.info(f"FinanceAgent processing query for user={user_id}")

        system = SYSTEM_PROMPT.format(context=self._summarize_context(context))
        response_text = await ai_service.chat(
            messages=[{"role": "user", "content": query}],
            system=system,
            temperature=0.3,
        )
        return {
            "agent": self.name,
            "content": response_text,
            "confidence": 0.88,
            "actions": self._extract_actions(response_text),
        }

    def _summarize_context(self, context: dict) -> str:
        habits = context.get("habit_patterns", [])
        return f"Recent activity: {len(habits)} habit entries logged."

    def _extract_actions(self, text: str) -> list[str]:
        """Return any action bullet points the AI mentioned."""
        lines = text.split("\n")
        return [l.strip("•- ").strip() for l in lines if l.strip().startswith(("-", "•", "*"))][:5]

    def matches(self, query: str) -> bool:
        q = query.lower()
        return any(kw in q for kw in self.keywords)

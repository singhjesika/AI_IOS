from typing import Any
from loguru import logger
import math
from datetime import datetime

from app.services.ai_service import ai_service


SYSTEM_PROMPT = """You are a world-class productivity coach and strategic planner.
You help users prioritize tasks, manage time, avoid burnout, and achieve deep focus.
Apply frameworks like GTD, Time-Blocking, Eisenhower Matrix, and Parkinson's Law.
Be specific, actionable, and realistic. User context: {context}"""


class PlannerAgent:
    """Default agent — handles productivity, scheduling, focus, and planning."""

    name = "productivity"
    keywords = ["task", "focus", "schedule", "deadline", "plan", "work",
                "prioritize", "goal", "habit", "routine", "time", "procrastinat"]

    async def run(self, user_id: str, query: str, context: dict[str, Any]) -> dict[str, Any]:
        logger.info(f"PlannerAgent processing query for user={user_id}")

        system = SYSTEM_PROMPT.format(context=self._summarize_context(context))
        response_text = await ai_service.chat(
            messages=[{"role": "user", "content": query}],
            system=system,
            temperature=0.4,
        )
        return {
            "agent": self.name,
            "content": response_text,
            "confidence": 0.90,
            "actions": self._extract_actions(response_text),
        }

    # ── Spaced-repetition helper (bonus utility) ──────────────────────────────
    @staticmethod
    def forgetting_curve_retention(days_since_study: int) -> float:
        """Ebbinghaus forgetting curve: R = e^(-t/S), S=10 days."""
        return round(math.exp(-0.1 * days_since_study) * 100, 1)

    @staticmethod
    def next_review_day(last_reviewed: datetime, review_count: int) -> int:
        """SM-2-inspired interval: 1, 3, 7, 14, 30 … days."""
        intervals = [1, 3, 7, 14, 30, 60, 120]
        idx = min(review_count, len(intervals) - 1)
        return intervals[idx]

    def _summarize_context(self, context: dict) -> str:
        history = context.get("conversation_history", [])
        habits = context.get("habit_patterns", [])
        return (
            f"{len(history)} recent messages, {len(habits)} habit entries. "
            "Focus on actionable planning advice."
        )

    def _extract_actions(self, text: str) -> list[str]:
        lines = text.split("\n")
        return [l.strip("•- ").strip() for l in lines if l.strip().startswith(("-", "•", "*"))][:5]

    def matches(self, query: str) -> bool:
        q = query.lower()
        return any(kw in q for kw in self.keywords)

<<<<<<< HEAD
import os
from groq import Groq
from dotenv import load_dotenv
from app.utils.logger import logger

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class AIService:
    def __init__(self):
        self.model = "llama3-70b-8192"

    async def chat(self, message: str, agent: str = "General", system_prompt: str = None, history: list = None):
        try:
            if not system_prompt:
                system_prompt = f"""You are a friendly, smart {agent} AI assistant inside an app called AI_IOS, designed for students.
Always reply in simple, easy-to-understand language.
Always give REAL examples with specific details.
Use emojis to make responses friendly.
Be specific and helpful like a good teacher."""

            messages = [{"role": "system", "content": system_prompt}]

            # Add history if provided
            if history:
                for h in history[:-1]:  # exclude last since we add message below
                    messages.append({"role": h["role"], "content": h["content"]})

            messages.append({"role": "user", "content": message})

            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
            )
            reply = response.choices[0].message.content
            logger.info(f"AI response generated for agent: {agent}")
            return {"response": reply}

        except Exception as e:
            logger.error(f"AI service error: {e}")
            return {"response": f"Sorry, I encountered an error: {str(e)}"}


ai_service = AIService()
=======
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from typing import Any
from loguru import logger

from app.config import settings


class AIService:
    """Thin wrapper around OpenAI and Anthropic APIs."""

    def __init__(self):
        self._openai: AsyncOpenAI | None = None
        self._anthropic: AsyncAnthropic | None = None

    @property
    def openai(self) -> AsyncOpenAI:
        if self._openai is None:
            self._openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        return self._openai

    @property
    def anthropic(self) -> AsyncAnthropic:
        if self._anthropic is None:
            self._anthropic = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        return self._anthropic

    # ── Chat completions ──────────────────────────────────────────────────────
    async def chat(
        self,
        messages: list[dict],
        system: str = "",
        model: str | None = None,
        temperature: float = 0.4,
        max_tokens: int = 1024,
    ) -> str:
        """Call OpenAI chat completion and return the assistant text."""
        model = model or settings.OPENAI_MODEL
        full_messages = []
        if system:
            full_messages.append({"role": "system", "content": system})
        full_messages.extend(messages)

        try:
            resp = await self.openai.chat.completions.create(
                model=model,
                messages=full_messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return resp.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            raise

    async def claude_chat(
        self,
        messages: list[dict],
        system: str = "",
        max_tokens: int = 1024,
    ) -> str:
        """Call Anthropic Claude and return the assistant text."""
        try:
            resp = await self.anthropic.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=max_tokens,
                system=system or "You are a helpful AI life coach.",
                messages=messages,
            )
            return resp.content[0].text
        except Exception as e:
            logger.error(f"Anthropic error: {e}")
            raise

    # ── Structured task suggestions ───────────────────────────────────────────
    async def suggest_tasks(self, goal: str, agent_type: str) -> list[dict[str, Any]]:
        """Ask GPT to break a goal into actionable sub-tasks with priorities."""
        system = (
            f"You are an expert {agent_type} coach. "
            "Given a user goal, respond ONLY with a JSON array of tasks. "
            "Each task: {\"title\": str, \"description\": str, \"priority\": \"low|medium|high|urgent\", "
            "\"estimated_minutes\": int, \"category\": str}. No markdown fences."
        )
        raw = await self.chat(
            messages=[{"role": "user", "content": f"Goal: {goal}"}],
            system=system,
            temperature=0.3,
            max_tokens=1200,
        )
        import json
        try:
            tasks = json.loads(raw)
            return tasks if isinstance(tasks, list) else []
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse AI task suggestions: {raw[:200]}")
            return []

    # ── Productivity insights ─────────────────────────────────────────────────
    async def generate_daily_insight(self, user_context: dict) -> str:
        """Generate a personalized daily productivity insight."""
        system = (
            "You are an AI life optimization coach. "
            "Based on the user's data, provide a concise (2-3 sentence) "
            "personalized insight or recommendation for today."
        )
        return await self.chat(
            messages=[{"role": "user", "content": str(user_context)}],
            system=system,
            temperature=0.6,
            max_tokens=256,
        )


ai_service = AIService()
>>>>>>> 7c6fe786d0ebce90909c90ce7f1ac9867d4e86fd

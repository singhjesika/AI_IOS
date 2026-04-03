from typing import Any
from loguru import logger

from app.agents.finance_agent import FinanceAgent
from app.agents.health_agent import HealthAgent
from app.agents.planner_agent import PlannerAgent


class AgentOrchestrator:
    """Routes a user query to the most relevant specialized agent."""

    def __init__(self):
        self._agents = [
            HealthAgent(),
            FinanceAgent(),
            PlannerAgent(),   # default / catch-all
        ]

    async def route(self, user_id: str, query: str, context: dict[str, Any]) -> dict[str, Any]:
        agent = self._pick_agent(query)
        logger.info(f"Routing to {agent.name} agent | user={user_id}")
        return await agent.run(user_id, query, context)

    def _pick_agent(self, query: str):
        for agent in self._agents[:-1]:   # skip default (last)
            if agent.matches(query):
                return agent
        return self._agents[-1]           # fallback: planner


orchestrator = AgentOrchestrator()

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
"""Tool Registry – centralised registry for AI tool/function calls."""
from typing import Callable, Dict, Any


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._schemas: Dict[str, dict] = {}

    def register(self, name: str, fn: Callable, schema: dict):
        self._tools[name] = fn
        self._schemas[name] = schema

    async def call(self, name: str, arguments: Dict[str, Any]) -> Any:
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' not found in registry")
        return await self._tools[name](**arguments)

    def get_schemas(self) -> list:
        return list(self._schemas.values())


tool_registry = ToolRegistry()
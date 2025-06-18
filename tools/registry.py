from typing import Callable, Dict, List

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._tool_categories: Dict[str, List[str]] = {}
    
    def register_tool(self, name: str, func: Callable, category: str = "general"):
        self._tools[name] = func
        if category not in self._tool_categories:
            self._tool_categories[category] = []
        self._tool_categories[category].append(name)
    
    def get_tools_for_agent(self, agent_type: str) -> List[Callable]:
        # Return appropriate tools based on agent type
        return [self._tools[name] for name in self._tool_categories.get(agent_type, [])]
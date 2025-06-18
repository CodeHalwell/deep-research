from typing import Dict, List, Any
from .web_search import DuckDuckGoWebSearch, TavilyWebSearch, WebScraper
from .literature_tools import LiteratureTools

class ToolRegistry:
    def __init__(self):
        self._tools = {
            "web_search": DuckDuckGoWebSearch(),
            "tavily_search": TavilyWebSearch(),
            "web_scraper": WebScraper(),
            "literature_search": LiteratureTools(),
        }
        
        self._agent_tools = {
            "ResearchAgent": ["web_search", "tavily_search", "literature_search", "web_scraper"],
            "FactCheckingAgent": ["web_search", "literature_search"],
            "FormattingAgent": ["citation_formatter", "template_engine"],
            "PlanningAgent": [],
            "WriteAgent": [],
            "ReviewAgent": [],
            "RevisionAgent": [],
            "SummaryAgent": [],
        }
    
    def get_tools_for_agent(self, agent_name: str) -> List[Any]:
        tool_names = self._agent_tools.get(agent_name, [])
        return [self._tools[name] for name in tool_names if name in self._tools]
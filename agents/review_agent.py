import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import List, Optional

from llama_index.core.agent.workflow import FunctionAgent
from models.agent import Agent

class ReviewAgent(Agent):
    def __init__(
        self,
        name: str = "ReviewAgent",
        description: str = "Useful for reviewing the report written by the WriteAgent and providing feedback.",
        system_prompt: str = (
            "You are the ReviewAgent that reviews the report written by the WriteAgent. "
            "You should provide constructive feedback and suggestions for improvement."
        ),
        llm: str = "gpt-3.5-turbo",
        tools: Optional[List[str]] = None,
        can_handoff_to: Optional[List[str]] = None
    ) -> None:
        if tools is None:
            tools = []
        if can_handoff_to is None:
            can_handoff_to = []
        super().__init__(name, description, system_prompt, llm, tools, can_handoff_to)

    def build_agent(self, api_key, config_path) -> FunctionAgent:
        """Builds the agent with the provided parameters."""
        return FunctionAgent(
            name=self.name,
            description=self.description,
            system_prompt=self.system_prompt,
            llm=self._get_llm_server(api_key=api_key, config_path=config_path),
            tools=[],  # Pass an empty list of the correct type
            can_handoff_to=self.can_handoff_to
        )
    
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import List, Optional

from llama_index.core.agent.workflow import FunctionAgent
from models.agent import Agent

class ResearchAgent(Agent):
    def __init__(
        self,
        name: str = "ResearchAgent",
        description: str = "Useful for searching the web for information on a given topic and recording notes on the topic.",
        system_prompt: str = (
            "You are the ResearchAgent that can search the web for information on a given topic and record notes on the topic. "
            "Once notes are recorded and you are satisfied, you should hand off control to the WriteAgent to write a report on the topic."
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

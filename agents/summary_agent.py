import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import List, Optional

from llama_index.core.agent.workflow import FunctionAgent
from models.agent import Agent

class SummaryAgent(Agent):
    def __init__(
        self,
        name: str = "SummaryAgent",
        description: str = "Useful for creating concise and accurate summaries of reports.",
        system_prompt = (
            "You are SummaryAgent, an autonomous agent specializing in creating concise and accurate summaries of reports. "
            "Your task is to read the full report and produce a clear, informative summary that captures the main findings, conclusions, and recommendations. "
            "Write the summary in accessible language appropriate for the intended audience, highlighting only the most important points and omitting minor details. "
            "Ensure the summary is standalone and understandable without reference to the full report. "
            "When your summary is complete, your task is finished."
        ),
        llm: str = "gpt-4.1-mini",
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
            tools=[],
            can_handoff_to=self.can_handoff_to
        )
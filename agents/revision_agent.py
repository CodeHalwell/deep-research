import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import List, Optional

from llama_index.core.agent.workflow import FunctionAgent
from models.agent import Agent

class RevisionAgent(Agent):
    def __init__(
        self,
        name: str = "RevisionAgent",
        description: str = "Useful for revising reports based on feedback from the ReviewAgent.",
        system_prompt = (
            "You are RevisionAgent, an autonomous agent specializing in revising reports based on feedback from the ReviewAgent. "
            "Your task is to carefully read the reviewers feedback and suggestions, then make appropriate improvements to the report. "
            "Revise sections for clarity, completeness, accuracy, and flow. "
            "Ensure that all actionable feedback is addressed. "
            "Maintain the reports original intent and structure, but improve the writing wherever possible. "
            "When your revisions are complete, your task is finished."
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
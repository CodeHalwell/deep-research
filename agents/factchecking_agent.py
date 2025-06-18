from typing import List, Optional

from llama_index.core.agent.workflow import FunctionAgent
from ..models.agent import Agent

class FactCheckingAgent(Agent):
    def __init__(
        self,
        name: str = "FactCheckingAgent",
        description: str = "Useful for verifying the factual accuracy of reports.",
        system_prompt = (
            "You are FactCheckingAgent, an autonomous agent specializing in verifying the factual accuracy of reports. "
            "Your task is to systematically review the report, checking all important claims, data points, and references for accuracy using reliable sources. "
            "If you find any inaccuracies or unsupported statements, note them clearly and suggest corrections or clarifications. "
            "Summarize your fact-checking process and provide a brief list of verified facts, corrected errors, and any statements that require further evidence. "
            "When you have completed your fact-checking, your task is finished."
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
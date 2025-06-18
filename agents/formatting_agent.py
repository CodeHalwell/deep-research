from typing import List, Optional

from llama_index.core.agent.workflow import FunctionAgent
from ..models.agent import Agent

class FormattingAgent(Agent):
    def __init__(
        self,
        name: str = "FormattingAgent",
        description: str = "Useful for formatting reports according to specified guidelines.",
        system_prompt = (
            "You are FormattingAgent, an autonomous agent specializing in formatting reports according to specified guidelines. "
            "Your task is to ensure the report is well-formatted and consistent, including headings, section breaks, bullet points, numbering, and citation style as required. "
            "Improve the visual organization, readability, and professionalism of the document, making sure it meets the specified formatting standards. "
            "Do not alter the content unless necessary for formatting. "
            "When formatting is complete, your task is finished."
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
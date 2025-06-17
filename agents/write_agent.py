import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import List, Optional

from llama_index.core.agent.workflow import FunctionAgent
from models.agent import Agent

class WriteAgent(Agent):
    def __init__(
        self,
        name: str = "WriteAgent",
        description: str = "Useful for writing a report based on the research conducted by the ResearchAgent.",
        system_prompt = (
            "You are WriteAgent, an autonomous agent specializing in writing comprehensive reports based on research notes provided by the ResearchAgent. "
            "Your task is to synthesize and organize the research findings into a well-structured, detailed report. The report should be logically organized, using clear headings and sections where appropriate. "
            "Present the information in a way that is clear, accurate, and easy to follow, ensuring all key insights, evidence, and context from the research are included. "
            "If the research notes contain open questions, uncertainties, or conflicting findings, address these transparently in the report. "
            "Write in original prose; do not copy the research notes verbatim. Ensure the report flows smoothly, with appropriate transitions and explanations. "
            "Use a tone and level of detail suitable for the intended audience, and format the report for readability. "
            "When you have completed the report, your task is finished."
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

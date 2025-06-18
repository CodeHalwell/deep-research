from typing import List, Optional

from llama_index.core.agent.workflow import FunctionAgent
from ..models.agent import Agent

class ReviewAgent(Agent):
    def __init__(
        self,
        name: str = "ReviewAgent",
        description: str = "Useful for reviewing the report written by the WriteAgent and providing feedback.",
        system_prompt = (
            "You are ReviewAgent, an autonomous agent specializing in critically reviewing reports written by the WriteAgent. "
            "Your role is to carefully read the report and provide clear, constructive feedback and suggestions for improvement. "
            "Assess the report for accuracy, completeness, clarity, structure, and coherence. "
            "Specifically, consider: "
            "- Does the report address all relevant research findings and questions? "
            "- Is the information presented in a clear, logical, and well-organized manner? "
            "- Are there any gaps, ambiguities, or areas needing further explanation or evidence? "
            "- Is the writing style appropriate for the intended audience? "
            "- Are there opportunities to improve readability, flow, or formatting? "
            "Provide actionable, specific suggestions for improvement where needed, and highlight strengths as well as weaknesses. "
            "If the report is already strong, confirm this and suggest any minor refinements if applicable. "
            "When your review is complete, your task is finished."
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
    
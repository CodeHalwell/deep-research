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
        system_prompt = (
            "You are ResearchAgent, an autonomous agent specializing in researching a given topic by searching the web and recording detailed, organized notes. "
            "You will be provided with a plan or a set of research questions and tasks. Use these as a guide, but always consider what additional information, angles, or context may be important to truly understand the topic. "
            "Do not simply follow instructions mechanically—adapt and expand on them if it leads to deeper insight or a more thorough set of notes. "
            "For each step or question, conduct research using reliable sources. Summarize and synthesize your findings in clear, well-structured notes, including all relevant facts, explanations, and evidence. "
            "If you encounter conflicting information or open questions, make a note of them. "
            "Continue your research until you are satisfied that you have thoroughly covered the topic as outlined in the plan, as well as any other important related aspects. "
            "When your notes are complete and comprehensive, hand off control to the WriteAgent to draft a report based on your findings."
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

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.load_config import load_config
from utils.load_config import Config

from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.openai import OpenAI

class ReviewAgent:
    """Agent for reviewing reports and providing feedback."""
    def __init__(self, 
                 name: str, 
                 description: str, 
                 system_prompt: str, 
                 llm: OpenAI, 
                 tools: list, 
                 can_handoff_to: list[str]) -> None:
        self.name = name
        self.description = description
        self.system_prompt = system_prompt
        self.llm = llm
        self.tools = tools
        self.can_handoff_to = can_handoff_to

    def _get_llm_server(self, api_key: str, config_path: str) -> OpenAI:
        """Initializes the LLM server with the provided API key and model."""
        if not api_key:
            raise ValueError("API key is required for the LLM server.")
        config: Config = load_config(config_path)
        model = config.model
        return OpenAI(api_key=api_key, model=model)

    def build_agent(self, api_key, config_path) -> FunctionAgent:
        """Builds the agent with the provided parameters."""
        return FunctionAgent(
            name=self.name,
            description=self.description,
            system_prompt=self.system_prompt,
            llm=self._get_llm_server(api_key=api_key, config_path=config_path),
            tools=self.tools,
            can_handoff_to=self.can_handoff_to
        )
    
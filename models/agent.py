from dataclasses import dataclass, field
from typing import List
from ..utils.config import Config, load_config
from llama_index.llms.openai import OpenAI
from abc import ABC
from ..utils.logging import setup_logger
# Initialize logging for this module
logger = setup_logger("agent", level="DEBUG", log_file="agent.log")

@dataclass
class _AgentConfig:
    name: str
    description: str
    system_prompt: str
    llm: str
    tools: List[str] = field(default_factory=list)
    can_handoff_to: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.name:
            raise ValueError("Agent name is required.")
        if not self.description:
            raise ValueError("Agent description is required.")
        if not self.system_prompt:
            raise ValueError("System prompt is required.")
        if not self.llm:
            raise ValueError("LLM is required.")
        if not isinstance(self.tools, list):
            raise TypeError("Tools must be a list.")
        if not isinstance(self.can_handoff_to, list):
            raise TypeError("can_handoff_to must be a list.")

class Agent(_AgentConfig, ABC):
    """Base class for agents with common properties and methods."""
    
    def _get_llm_server(self, api_key: str, config_path: str) -> OpenAI:
        """Initializes the LLM server with the provided API key and model."""
        if not api_key:
            raise ValueError("API key is required for the LLM server.")
        config: Config = load_config(config_path)
        model = config.model
        return OpenAI(api_key=api_key, model=model)
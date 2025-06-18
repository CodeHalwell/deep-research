from dataclasses import dataclass, field
from typing import List, Union, Callable, Any
from ..utils.config import Config, load_config
from llama_index.llms.openai import OpenAI
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools.types import BaseTool
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
    tools: List[str] | None = field(default_factory=list)
    can_handoff_to: List[str] | None = field(default_factory=list)

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
    
    def _resolve_tools(self, tool_names: List[str]) -> List[Union[BaseTool, Callable[..., Any]]]:
        """Resolve tool names to actual tool instances. Override in subclasses."""
        # Base implementation returns empty list - subclasses should override
        return []
    
    def build_agent(self, api_key: str, config_path: str) -> FunctionAgent:
        """Builds the agent with the provided parameters."""
        logger.info(f"Building {self.name} with LLM {self.llm}")
        resolved_tools = self._resolve_tools(self.tools or [])
        return FunctionAgent(
            name=self.name,
            description=self.description,
            system_prompt=self.system_prompt,
            llm=self._get_llm_server(api_key=api_key, config_path=config_path),
            tools=resolved_tools,
            can_handoff_to=self.can_handoff_to
        )
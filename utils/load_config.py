import yaml
from dataclasses import dataclass, field

@dataclass
class Config:
    """Configuration class for the application."""
    provider: str = "openai"
    model: str = "gpt-4.1-mini"
    temperature: float = 0.7
    max_tokens: int = 1000
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop: list[str | None] = field(default_factory=list)
    system_prompt: str = "You are a helpful assistant."
    max_context_length: int = 16000
    mcp_enabled: bool = True
    host: str = "127.0.0.1"
    port: int = 7860

def load_config(file_path: str) -> Config:
    """Load configuration from a YAML file."""
    with open(file_path, 'r') as file:
        config_data = yaml.safe_load(file)

    # Flatten the nested config structure
    provider = config_data.get("provider", {})
    model_settings = config_data.get("model_settings", {})
    context = config_data.get("context", {})
    mcp_server = config_data.get("mcp_server", {})

    return Config(
        provider=provider.get("name", "openai"),
        model=provider.get("model", "gpt-4.1-mini"),
        temperature=model_settings.get("temperature", 0.7),
        max_tokens=model_settings.get("max_tokens", 1000),
        top_p=model_settings.get("top_p", 1.0),
        frequency_penalty=model_settings.get("frequency_penalty", 0.0),
        presence_penalty=model_settings.get("presence_penalty", 0.0),
        stop=model_settings.get("stop_sequences", []),
        system_prompt=context.get("system_prompt", "You are a helpful assistant."),
        max_context_length=context.get("max_context_length", 16000),
        mcp_enabled=mcp_server.get("enabled", True),
        host=mcp_server.get("host", "127.0.0.1"),
        port=mcp_server.get("port", 7860),
    )

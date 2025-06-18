import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.config import load_config
import pytest
import sys
import os

@pytest.fixture
def config():
    """Fixture to load the configuration."""
    config_path = os.path.join(os.path.dirname(__file__), '.test_config/test_config.yaml')
    assert os.path.exists(config_path), f"Config file not found at {config_path}"
    return load_config(config_path)

def test_load_config(config):
    """Test that the configuration is loaded correctly."""
    assert config.provider == "openai"
    assert config.model == "gpt-4o-mini"
    assert config.temperature == 0.7
    assert config.max_tokens == 1000
    assert config.top_p == 1.0
    assert config.frequency_penalty == 0.0
    assert config.presence_penalty == 0.0
    assert isinstance(config.stop, list)
    assert config.system_prompt == "You are a helpful, conversational assistant with access to tools."
    assert config.max_context_length == 16000
    assert config.mcp_enabled is True
    assert config.host == "127.0.0.1"
    assert config.port == 7860
from tools.web_search import DuckDuckGoWebSearch, TavilyWebSearch, WebScraper
from dotenv import load_dotenv
import os
import asyncio
from llama_index.core.agent.workflow import (
    AgentInput,
    AgentOutput,
    ToolCall,
    ToolCallResult,
    AgentStream,
    AgentWorkflow,
    FunctionAgent, 
    ReActAgent
)

from llama_index.core.workflow import (
    Context,
    InputRequiredEvent,
    HumanResponseEvent,
    StartEvent,
    StopEvent,
    Workflow,
    Event,
    step,
)

from llama_index.utils.workflow import draw_all_possible_flows
from llama_index.tools.mcp import (
    get_tools_from_mcp_url,
    aget_tools_from_mcp_url,
    workflow_as_mcp
)

from mcp_server import server
from utils.load_config import load_config

load_dotenv()

config = load_config(file_path=".config/config.yaml")

if config.mcp_enabled:
    server.main()

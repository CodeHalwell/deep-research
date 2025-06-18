from dotenv import load_dotenv
from mcp_server import research_server, document_server
from utils.config import load_config
from utils.logging import setup_logger

# Initialize logging
logger = setup_logger("mcp_server", level="DEBUG", log_file="mcp_server.log")

load_dotenv()

try:
    config = load_config(file_path=".config/config.yaml")
except FileNotFoundError as e:
    logger.error(f"Configuration file not found: {e}")
    exit(1)

if config.mcp_enabled:
    logger.info("Starting MCP server...")
    try:
        research_server.start_server()
        document_server.start_server()
    except Exception as e:
        logger.error(f"Error initializing servers: {e}")
        exit(1)

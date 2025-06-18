from dotenv import load_dotenv
from mcp_server import server
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
    server.main()



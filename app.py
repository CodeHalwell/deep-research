from dotenv import load_dotenv



from mcp_server import server
from utils.load_config import load_config

load_dotenv()

config = load_config(file_path=".config/config.yaml")

if config.mcp_enabled:
    server.main()



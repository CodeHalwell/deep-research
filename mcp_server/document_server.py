import gradio as gr
import os

from dotenv import load_dotenv
from ..utils.logging import setup_logger

load_dotenv()
logger = setup_logger("document_server", level="DEBUG", log_file="document_server.log")


with gr.Blocks() as demo:
    gr.Markdown(
        """
        This is a demo of a MCP-only tool.
        This tool slices a list.
        This tool is MCP-only, so it does not have a UI.
        """
    )
    gr.api(
    )

def start_server():
    demo.launch(mcp_server=True,
                server_name=os.getenv("SERVER_NAME", "127.0.0.1"),
                server_port=int(os.getenv("SERVER_PORT", 7861)))

if __name__ == "__main__":
    start_server()

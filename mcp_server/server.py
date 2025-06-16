import gradio as gr
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.web_search import DuckDuckGoWebSearch, TavilyWebSearch, WebScraper
from dotenv import load_dotenv
import os
import asyncio

# load the scrape_website function from the tools.web_search WebScrape
load_dotenv()

async def scrape(url: str) -> str:
    """
    Scrape the content of a website.
    
    Args:
        url (str): The URL of the website to scrape.
    Returns:
        str: The scraped content of the website.
    """
    scraper = WebScraper()
    content = await scraper.scrape_website(url)
    if isinstance(content, Exception):
        return f"Error scraping website: {str(content)}"
    return content

with gr.Blocks() as demo:
    gr.Markdown(
        """
        This is a demo of a MCP-only tool.
        This tool slices a list.
        This tool is MCP-only, so it does not have a UI.
        """
    )
    gr.api(
        scrape
    )

def main():
    demo.launch(mcp_server=True)

if __name__ == "__main__":
    main()

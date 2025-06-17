import gradio as gr
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.web_search import DuckDuckGoWebSearch, TavilyWebSearch, WebScraper
from dotenv import load_dotenv
import os

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

async def ddg_search(query: str) -> str:
    """
    Perform a web search using DuckDuckGo or Tavily.
    
    Args:
        query (str): The search query.
    Returns:
        str: The search results.
    """
    try:
        search_engine = DuckDuckGoWebSearch()
        results = await search_engine.search(query)
        return results
    except Exception as e:
        return f"Error during web search: {str(e)}"
    
async def tavily_search(query: str) -> str:
    """
    Perform a web search using Tavily.
    
    Args:
        query (str): The search query.
    Returns:
        str: The search results.
    """
    try:
        search_engine = TavilyWebSearch(os.getenv("TAVILY_API_KEY"))
        results = await search_engine.search(query)
        return results
    except Exception as e:  
        return f"Error during web search: {str(e)}"

with gr.Blocks() as demo:
    gr.Markdown(
        """
        This is a demo of a MCP-only tool.
        This tool slices a list.
        This tool is MCP-only, so it does not have a UI.
        """
    )
    gr.api(
        scrape,
        ddg_search,
        tavily_search,
    )

def main():
    demo.launch(mcp_server=True)

if __name__ == "__main__":
    main()

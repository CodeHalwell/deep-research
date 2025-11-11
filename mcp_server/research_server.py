import gradio as gr
import os
import json
from tools.web_search import DuckDuckGoWebSearch, TavilyWebSearch, WebScraper
from tools.literature_tools import LiteratureTools
from dotenv import load_dotenv
from utils.logging import setup_logger

# Initialize logging for this module
logger = setup_logger("research_server", level="DEBUG", log_file="research_server.log")

load_dotenv()


async def scrape(url: str) -> str:
    """
    Scrape the content of a website.

    Args:
        url (str): The URL of the website to scrape.

    Returns:
        str: The scraped content of the website.
    """
    try:
        scraper = WebScraper()
        content = await scraper.scrape_website(url)
        if isinstance(content, Exception):
            return f"Error scraping website: {str(content)}"
        logger.info(f"Successfully scraped {url}")
        return content
    except Exception as e:
        logger.error(f"Error scraping {url}: {str(e)}")
        return f"Error scraping website: {str(e)}"


async def ddg_search(query: str, max_results: int = 5) -> str:
    """
    Perform a web search using DuckDuckGo.

    Args:
        query (str): The search query.
        max_results (int): Maximum number of results to return.

    Returns:
        str: The search results in JSON format.
    """
    try:
        search_engine = DuckDuckGoWebSearch()
        results = await search_engine.search(query, max_results=max_results)
        logger.info(f"DuckDuckGo search completed for: {query}")
        return json.dumps(results) if isinstance(results, dict) else str(results)
    except Exception as e:
        logger.error(f"Error during DuckDuckGo search: {str(e)}")
        return f"Error during web search: {str(e)}"


async def tavily_search(query: str, max_results: int = 5) -> str:
    """
    Perform a web search using Tavily.

    Args:
        query (str): The search query.
        max_results (int): Maximum number of results to return.

    Returns:
        str: The search results in JSON format.
    """
    try:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "Error: TAVILY_API_KEY not set"

        search_engine = TavilyWebSearch(api_key)
        results = await search_engine.search(query, max_results=max_results)
        logger.info(f"Tavily search completed for: {query}")
        return json.dumps(results) if isinstance(results, list) else str(results)
    except Exception as e:
        logger.error(f"Error during Tavily search: {str(e)}")
        return f"Error during web search: {str(e)}"


async def scholar_search(query: str, max_results: int = 5) -> str:
    """
    Perform an academic search using Google Scholar API (via SerpAPI).

    Args:
        query (str): The research query.
        max_results (int): Maximum number of results to return.

    Returns:
        str: The search results in JSON format.
    """
    try:
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            return "Error: SERPAPI_API_KEY not set"

        lit_tools = LiteratureTools(api_key)
        results = await lit_tools.search_google_scholar(query, max_results=max_results)
        logger.info(f"Scholar search completed for: {query}")
        return json.dumps(results) if isinstance(results, dict) else str(results)
    except Exception as e:
        logger.error(f"Error during Scholar search: {str(e)}")
        return f"Error during scholar search: {str(e)}"


async def arxiv_search(query: str, max_results: int = 5) -> str:
    """
    Search arXiv for academic papers.

    Args:
        query (str): The research query.
        max_results (int): Maximum number of results to return.

    Returns:
        str: The search results in JSON format.
    """
    try:
        lit_tools = LiteratureTools()
        results = await lit_tools.search_arxiv(query, max_results=max_results)
        logger.info(f"arXiv search completed for: {query}")
        return json.dumps(results) if isinstance(results, dict) else str(results)
    except Exception as e:
        logger.error(f"Error during arXiv search: {str(e)}")
        return f"Error during arXiv search: {str(e)}"


async def semantic_scholar_search(query: str, max_results: int = 5) -> str:
    """
    Search Semantic Scholar for academic papers.

    Args:
        query (str): The research query.
        max_results (int): Maximum number of results to return.

    Returns:
        str: The search results in JSON format.
    """
    try:
        lit_tools = LiteratureTools()
        results = await lit_tools.search_semantic_scholar(query, max_results=max_results)
        logger.info(f"Semantic Scholar search completed for: {query}")
        return json.dumps(results) if isinstance(results, dict) else str(results)
    except Exception as e:
        logger.error(f"Error during Semantic Scholar search: {str(e)}")
        return f"Error during Semantic Scholar search: {str(e)}"


with gr.Blocks() as demo:
    gr.Markdown(
        """
        # Research Tools (MCP Server)

        This is a Gradio MCP server providing research and data gathering tools:
        - Web search (DuckDuckGo, Tavily)
        - Academic search (Google Scholar, arXiv, Semantic Scholar)
        - Web scraping

        All tools are available via MCP protocol.
        """
    )
    gr.api(
        scrape,
        ddg_search,
        tavily_search,
        scholar_search,
        arxiv_search,
        semantic_scholar_search,
    )


def start_server():
    demo.launch(
        mcp_server=True,
        server_name=os.getenv("SERVER_NAME", "127.0.0.1"),
        server_port=int(os.getenv("RESEARCH_SERVER_PORT", 7860)),
    )


if __name__ == "__main__":
    start_server()


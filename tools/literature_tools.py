import requests
from serpapi.client import SerpAPI  # type: ignore
import asyncio
import aiohttp
import os
import dotenv
from xml.etree import ElementTree as ET
from typing import Any
from utils.logging import setup_logger
from llama_index.tools.valyu import ValyuToolSpec  # type: ignore
from llama_index.tools.wolfram_alpha import WolframAlphaToolSpec  # type: ignore
from llama_index.tools.wikipedia import WikipediaToolSpec  # type: ignore


# Initialize logging for this module
logger = setup_logger("literature_tools", level="DEBUG", log_file="literature_tools.log")

# Load environment variables from .env file
dotenv.load_dotenv()

class LiteratureTools:
    """A class to encapsulate literature-related tools and methods."""

    @staticmethod
    async def get_serpapi_results(query: str) -> list[dict[str, Any]]:
        """Fetches search results from SerpAPI for a given query."""
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            raise ValueError("SERPAPI_API_KEY environment variable is not set")
        
        params = {
            "engine": "google_scholar",
            "q": query,
        }
        
        serp = SerpAPI(api_key=api_key)

        results = await serp.search(params=params)
        if "organic_results" in results:
            return results["organic_results"]
        else:
            return []

    @staticmethod
    async def get_semantic_scholar_results(query: str) -> list:
        """Fetches search results from Semantic Scholar for a given query."""
        
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        query_params = {
            "query": query,
            "fields": "title,url,publicationTypes,publicationDate,openAccessPdf",
            "year": "2023-"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=query_params) as response:
                if response.status != 200:
                    logger.error(f"Error fetching data from Semantic Scholar: {response.status}")
                    return []
                
                # Parse the JSON response
                response_json = await response.json()
                if "data" not in response_json:
                    logger.error("No 'data' field found in the response")
                    return []

                # Return the list of results
                return response_json.get("data", [])


    @staticmethod
    async def get_arxiv_results(query: str, max_results: int = 10) -> list:
        """Fetches search results from arXiv for a given query."""
        
        url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    logger.error(f"Error fetching data from arXiv: {response.status}")
                    return []
                
                try:
                    # Parse the XML response
                    content = await response.text()
                    root = ET.fromstring(content)
                    ns = {'atom': 'http://www.w3.org/2005/Atom'}
                    results = []
                    
                    for entry in root.findall('atom:entry', ns):
                        title_elem = entry.find('atom:title', ns)
                        id_elem = entry.find('atom:id', ns)
                        summary_elem = entry.find('atom:summary', ns)

                        title = title_elem.text.strip() if title_elem is not None else "No title"
                        id_ = id_elem.text.strip() if id_elem is not None else "No ID"
                        summary = summary_elem.text.strip() if summary_elem is not None else "No summary"

                        results.append({
                            "title": title,
                            "id": id_,
                            "summary": summary
                        })
                    
                    return results
                    
                except ET.ParseError as e:
                    logger.error(f"Error parsing XML response from arXiv: {e}")
                    return []
                except Exception as e:
                    logger.error(f"Unexpected error processing arXiv response: {e}")
                    return []

class LlamaIndexTools:
    """A class to encapsulate LlamaIndex tools."""

    @staticmethod
    def get_valyu_tool_spec() -> ValyuToolSpec:
        """Returns the Valyu tool specification."""
        return ValyuToolSpec()

    @staticmethod
    def get_wolfram_alpha_tool_spec() -> WolframAlphaToolSpec:
        """Returns the Wolfram Alpha tool specification."""
        return WolframAlphaToolSpec()

    @staticmethod
    def get_wikipedia_tool_spec() -> WikipediaToolSpec:
        """Returns the Wikipedia tool specification."""
        return WikipediaToolSpec()
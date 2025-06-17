import requests
from serpapi.client import SerpAPI  # type: ignore
import os
import dotenv
from xml.etree import ElementTree as ET
import urllib.request as libreq
import xml.dom.minidom
import io
# Load environment variables from .env file
dotenv.load_dotenv()


class LiteratureTools:
    """A class to encapsulate literature-related tools and methods."""

    @staticmethod
    def get_serpapi_results(query: str) -> list:
        """Fetches search results from SerpAPI for a given query."""
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            raise ValueError("SERPAPI_API_KEY environment variable is not set")
        
        params = {
            "engine": "google_scholar",
            "q": query,
        }
        
        serp = SerpAPI(api_key=api_key)

        results = serp.search(params=params)
        if "organic_results" in results:
            return results["organic_results"]
        else:
            return []

    @staticmethod
    def get_semantic_scholar_results(query: str) -> list:
        """Fetches search results from Semantic Scholar for a given query."""
        
        url = "http://api.semanticscholar.org/graph/v1/paper/search/bulk"
        query_params = {
            "query": query,
            "fields": "title,url,publicationTypes,publicationDate,openAccessPdf",
            "year": "2023-"
        }
        
        response = requests.get(url, params=query_params)
        return response.json().get("data", [])


    @staticmethod
    def get_arxiv_results(query: str, max_results: int = 10) -> list:
        """Fetches search results from arXiv for a given query."""
        
        url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the XML response
            tree = ET.ElementTree(ET.fromstring(response.content))
            root = tree.getroot()
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            results = []
            for entry in root.findall('atom:entry', ns):
                title_elem = entry.find('atom:title', ns)
                id_elem = entry.find('atom:id', ns)
                summary_elem = entry.find('atom:summary', ns)

                title = title_elem.text if title_elem is not None else "No title"
                id_ = id_elem.text if id_elem is not None else "No ID"
                summary = summary_elem.text if summary_elem is not None else "No summary"

                results.append({
                    "title": title,
                    "id": id_,
                    "summary": summary
                })
            return results
        else:
            raise Exception(f"Error fetching data from arXiv: {response.status_code}")

from tavily import AsyncTavilyClient # type: ignore
import aiohttp
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from urllib.parse import urljoin
from duckduckgo_search import DDGS
from duckduckgo_search.duckduckgo_search import (
    RatelimitException, 
    DuckDuckGoSearchException, 
    TimeoutException, 
    LHTMLParser)

load_dotenv()

class TavilyWebSearch:
    def __init__(self, api_key: str | None):
        if api_key is None:
            raise ValueError("API key is required")
        self.client = AsyncTavilyClient(api_key=api_key)

    async def search(self, query: str, max_results: int = 10):
        """
        Perform a web search using the Tavily API.

        Args:
            query (str): The search query.
            max_results (int): The maximum number of results to return.

        Returns:
            list: A list of search results.
        """
        if not query:
            raise ValueError("Search query cannot be empty")
        results = await self.client.search(query, max_results=max_results)
        return results

class DuckDuckGoWebSearch(DDGS):
    def __init__(self):
        """
        Initialize the DuckDuckGoWebSearch with necessary configurations.
        """
        super().__init__()
        self.data_dir = "data"
        self.ddgs = DDGS()

    async def search(self, query: str, max_results: int = 10):
        """
        Perform a web search using DuckDuckGo.

        Args:
            query (str): The search query.
            max_results (int): The maximum number of results to return.

        Returns:
            list: A list of search results.
        """
        results = []
        if not query:
            raise ValueError("Search query cannot be empty")
        try:
            for result in self.ddgs.text(query, max_results=max_results):
                if isinstance(result, LHTMLParser):
                    results.append({
                        "title": result.title,
                        "url": result.url,
                        "snippet": result.snippet
                    })
                else:
                    results.append(result)
        except (RatelimitException, DuckDuckGoSearchException, TimeoutException) as e:
            print(f"Error during search: {str(e)}")
        
        return results


class WebScraper:
    def __init__(self):
        """
        Initialize the WebScraper with necessary configurations.
        """
        self.data_dir = "data"
        
    async def _scrape_website(self, url: str) -> str | Exception:
        """
        Fetch the content of a website, focusing on main article content.

        Args:
            url (str): The URL of the website including the http or https. e.g. "https://example.com"

        Returns:
            str: The main content of the website.
        """
        if not url:
            raise ValueError("URL cannot be empty")
        if not url.startswith(('http://', 'https://')):
            raise ValueError("Invalid URL format. Must start with http:// or https://")
        try:
            timeout = aiohttp.ClientTimeout(total=5)  # Set a timeout for the request
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        content: str = await response.text()
                        soup: BeautifulSoup = BeautifulSoup(content, 'html.parser')
                        
                        # Remove unwanted elements globally
                        for element in soup.find_all([
                            'script', 'style', 'nav', 'header', 'footer', 'aside',
                            'form', 'button', 'iframe', 'noscript', 'svg', 'meta',
                            'link', 'input', 'select', 'textarea'
                        ]):
                            element.decompose()
                        
                        # Remove common navigation/promotional elements
                        for element in soup.find_all(attrs={
                            'class': lambda x: bool(x and any(
                                term in ' '.join(x).lower() for term in [
                                    'nav', 'menu', 'sidebar', 'footer', 'header', 'ad',
                                    'advertisement', 'promo', 'banner', 'social', 'share',
                                    'comment', 'cookie', 'popup', 'modal'
                                ]
                            ))
                        }):
                            element.decompose()
                        
                        # Try multiple selectors to find main content
                        content_selectors = [
                            'main',
                            'article', 
                            '[role="main"]',
                            '.content',
                            '.article',
                            '.post',
                            '.entry',
                            '#content',
                            '#main',
                            '.main-content',
                            'body'
                        ]
                        
                        main_content = None
                        for selector in content_selectors:
                            main_content = soup.select_one(selector)
                            if main_content:
                                break
                        
                        if main_content is None:
                            main_content = soup.body or soup
                        
                        # Extract title
                        title = ""
                        title_element = (soup.find('h1') or 
                                       soup.find('title') or 
                                       main_content.find('h1'))
                        if title_element:
                            title = title_element.get_text(strip=True)
                        
                        # Extract all meaningful text content
                        text_elements = main_content.find_all([
                            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
                            'p', 'div', 'span', 'li', 'td', 'th'
                        ])
                        
                        # Collect all text and links
                        content_parts = []
                        links = []
                        seen_texts = set()
                        
                        for element in text_elements:
                            text = element.get_text(strip=True)
                            
                            # Skip empty, very short, or duplicate text
                            if not text or len(text) < 10 or text in seen_texts:
                                continue
                            
                            seen_texts.add(text)
                            
                            # Add heading formatting
                            if element.name.startswith('h'): # type: ignore
                                content_parts.append(f"\n{text}\n")
                            else:
                                content_parts.append(text)
                            
                            # Extract links from this element
                            for link in element.find_all('a', href=True):
                                href = link.get('href')
                                link_text = link.get_text(strip=True)
                                
                                if href and link_text:
                                    # Convert relative URLs to absolute
                                    if href.startswith('/'):
                                        href = urljoin(url, href)
                                    
                                    links.append({
                                        "url": href,
                                        "text": link_text
                                    })
                        
                        # Extract lists separately for better structure
                        lists = []
                        for ul in main_content.find_all(['ul', 'ol']):
                            list_items = []
                            for li in ul.find_all('li'):
                                item_text = li.get_text(strip=True)
                                if item_text and len(item_text) > 3:
                                    list_items.append(item_text)
                            
                            if list_items:
                                lists.append({
                                    "type": "ordered" if ul.name == 'ol' else "unordered",
                                    "items": list_items
                                })
                        
                        # Build result object
                        result = {
                            "url": url,
                            "title": title,
                            "content": "\n".join(content_parts),
                            "links": links[:50],  # Limit to first 50 links
                            "lists": lists[:10],  # Limit to first 10 lists
                            "word_count": len(' '.join(content_parts).split())
                        }
                        
                        return json.dumps(result, indent=2, ensure_ascii=False)
                    elif response.status == 404:
                        raise Exception
                    elif response.status == 403:
                        raise Exception
                    elif response.status == 408:
                        raise Exception
                    elif response.status == 429:
                        raise Exception
                    else:
                        return Exception(f"Error fetching {url}: HTTP {response.status}")
        except Exception as e:
            raise Exception(f"Error fetching {url}: {str(e)}")
        

    async def scrape_website(self, url: str) -> str | Exception:
        """
        Scrape a website for its main content.

        Args:
            url (str): The URL of the website to scrape.

        Returns:
            str: The main content of the website.
        """
        if not url:
            raise ValueError("URL cannot be empty")
        
        try:
            content: str | Exception = await self._scrape_website(url)
        except Exception as e:
            return Exception(f"Error scraping {url}: {str(e)}")
        
        # Parse the JSON string to access the title
        try:
            content_dict = json.loads(content)
            title = content_dict.get("title", "untitled")
        except (json.JSONDecodeError, TypeError):
            title = "untitled"

        file_name = title.replace(" ", "_").replace("/", "_").replace(":", "_") + ".json"
        file_name = file_name[:15]  # Limit filename length

        with open(f"{self.data_dir}/{file_name}", "w", encoding="utf-8") as f:
            f.write(content)

        return content
    
    async def download_files(self, urls: list[str]) -> list[str]:
        """
        Download files like pdfs, txt etc if present from a list of URLs
        Args:
            urls (list[str]): List of URLs to download files from.
        Returns:
            list[str]: List of file paths where the files were saved.
        """
        file_paths = []
        # Define supported file types
        supported_extensions = {'.pdf', '.txt', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.csv', '.json', '.xml', '.zip'}
        
        async with aiohttp.ClientSession() as session:
            for url in urls:
                try:
                    # Check if URL has a supported file extension
                    file_extension = None
                    for ext in supported_extensions:
                        if url.lower().endswith(ext) or ext[1:] in url.lower():
                            file_extension = ext
                            break
                    
                    if not file_extension:
                        print(f"Skipping {url}: Unsupported file type")
                        continue
                    
                    async with session.get(url) as response:
                        if response.status == 200:
                            # Verify content type matches file extension
                            content_type = response.headers.get('content-type', '').lower()
                            
                            # Basic content type validation
                            valid_content = False
                            if file_extension == '.pdf' and 'pdf' in content_type:
                                valid_content = True
                            elif file_extension in ['.txt', '.csv'] and ('text' in content_type or 'csv' in content_type):
                                valid_content = True
                            elif file_extension in ['.doc', '.docx'] and ('word' in content_type or 'document' in content_type):
                                valid_content = True
                            elif file_extension in ['.xls', '.xlsx'] and ('excel' in content_type or 'spreadsheet' in content_type):
                                valid_content = True
                            elif file_extension in ['.json', '.xml'] and ('json' in content_type or 'xml' in content_type):
                                valid_content = True
                            elif file_extension == '.zip' and 'zip' in content_type:
                                valid_content = True
                            else:
                                # Allow download if content type is generic binary or octet-stream
                                if 'octet-stream' in content_type or 'binary' in content_type:
                                    valid_content = True
                            
                            if not valid_content:
                                print(f"Warning: Content type mismatch for {url}. Expected {file_extension}, got {content_type}")
                            
                            content = await response.read()
                            file_name = url.split("/")[-1]
                            
                            # Ensure the filename has the correct extension
                            if not file_name.lower().endswith(file_extension):
                                file_name += file_extension
                            
                            file_path = f"{self.data_dir}/{file_name}"
                            with open(file_path, "wb") as f:
                                f.write(content)
                            file_paths.append(file_path)
                            print(f"Downloaded: {file_name}")
                        else:
                            print(f"Failed to download {url}: {response.status}")
                except Exception as e:
                    print(f"Error downloading {url}: {str(e)}")
        return file_paths

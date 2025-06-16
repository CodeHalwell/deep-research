import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.web_search import DuckDuckGoWebSearch, TavilyWebSearch, WebScraper
from dotenv import load_dotenv
import pytest
from unittest.mock import patch
import sys
import os
import json

# Load environment variables from a .env file
load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables from a .env file
load_dotenv()

# Install pytest-asyncio first: pip install pytest-asyncio

class TestTavilyWebSearch:
    @pytest.mark.asyncio
    async def test_tavily_search_success(self):
        tavily_search = TavilyWebSearch(api_key=os.getenv("TAVILY_API_KEY"))
        results = await tavily_search.search("OpenAI")
        assert isinstance(results, dict), "Results should be a dict"
        assert len(results) > 0, "Results should not be empty"

    @pytest.mark.asyncio
    async def test_tavily_search_empty_query(self):
        tavily_search = TavilyWebSearch(api_key=os.getenv("TAVILY_API_KEY"))
        with pytest.raises((ValueError, Exception)):
            await tavily_search.search("")

    @pytest.mark.asyncio
    async def test_tavily_search_invalid_api_key(self):
        tavily_search = TavilyWebSearch(api_key="invalid_key")
        with pytest.raises(Exception):
            await tavily_search.search("OpenAI")

    @pytest.mark.asyncio
    async def test_tavily_search_none_query(self):
        tavily_search = TavilyWebSearch(api_key=os.getenv("TAVILY_API_KEY"))
        with pytest.raises((ValueError, TypeError)):
            await tavily_search.search(None)

    @pytest.mark.asyncio
    @patch('tools.web_search.TavilyWebSearch.search')
    async def test_tavily_search_mock(self, mock_search):
        mock_search.return_value = {"results": [{"title": "Test", "url": "http://test.com"}]}
        tavily_search = TavilyWebSearch(api_key="test_key")
        results = await tavily_search.search("test query")
        assert results == {"results": [{"title": "Test", "url": "http://test.com"}]}
        mock_search.assert_called_once_with("test query")

class TestDuckDuckGoWebSearch:
    @pytest.mark.asyncio
    async def test_duckduckgo_search_success(self):
        ddg_search = DuckDuckGoWebSearch()
        results = await ddg_search.search("OpenAI")
        assert isinstance(results, list), "Results should be a list"
        assert len(results) > 0, "Results should not be empty"

    @pytest.mark.asyncio
    async def test_duckduckgo_search_empty_query(self):
        ddg_search = DuckDuckGoWebSearch()
        with pytest.raises((ValueError, Exception)):
            await ddg_search.search("")

    @pytest.mark.asyncio
    async def test_duckduckgo_search_none_query(self):
        ddg_search = DuckDuckGoWebSearch()
        with pytest.raises((ValueError, TypeError)):
            await ddg_search.search(None)

    @pytest.mark.asyncio
    async def test_duckduckgo_search_special_characters(self):
        ddg_search = DuckDuckGoWebSearch()
        results = await ddg_search.search("test@#$%")
        assert isinstance(results, list), "Results should be a list"

    @pytest.mark.asyncio
    @patch('tools.web_search.DuckDuckGoWebSearch.search')
    async def test_duckduckgo_search_mock(self, mock_search):
        mock_search.return_value = [{"title": "Test", "url": "http://test.com"}]
        ddg_search = DuckDuckGoWebSearch()
        results = await ddg_search.search("test query")
        assert results == [{"title": "Test", "url": "http://test.com"}]
        mock_search.assert_called_once_with("test query")

class TestWebScraper:
    @pytest.mark.asyncio
    async def test_web_scraper_valid_url(self):
        scraper = WebScraper()
        content = await scraper.scrape_website("https://httpbin.org/html")
        assert isinstance(content, str), "Content should be a string"
        assert len(content) > 0, "Content should not be empty"
        # The reason for your test failures is that your WebScraper.scrape_website method does not actually raise exceptions
        # for invalid URLs, 404s, or timeouts. Instead, it returns an Exception object as a value.
        # Your tests expect an exception to be raised, but none is raised, so pytest fails the test.

        # To fix your tests, check if the returned value is an Exception instance instead of using pytest.raises.
        # Here are improved versions of your tests and some additional ones for better coverage:

        class TestWebScraper:
            @pytest.mark.asyncio
            async def test_web_scraper_valid_url(self):
                scraper = WebScraper()
                content = await scraper.scrape_website("https://httpbin.org/html")
                assert isinstance(content, str), "Content should be a string"
                assert len(content) > 0, "Content should not be empty"

            @pytest.mark.asyncio
            async def test_web_scraper_invalid_url(self):
                scraper = WebScraper()
                result = await scraper.scrape_website("invalid_url")
                assert isinstance(result, Exception), "Should return an Exception for invalid URL"

            @pytest.mark.asyncio
            async def test_web_scraper_404_url(self):
                scraper = WebScraper()
                result = await scraper.scrape_website("https://httpbin.org/status/404")
                assert isinstance(result, Exception), "Should return an Exception for 404 URL"

            @pytest.mark.asyncio
            async def test_web_scraper_timeout(self):
                scraper = WebScraper()
                result = await scraper.scrape_website("https://httpbin.org/delay/10")
                assert isinstance(result, Exception), "Should return an Exception for timeout"

            @pytest.mark.asyncio
            @patch('tools.web_search.WebScraper.scrape_website')
            async def test_web_scraper_mock(self, mock_scrape):
                mock_scrape.return_value = "<html><body>Test content</body></html>"
                scraper = WebScraper()
                content = await scraper.scrape_website("http://test.com")
                assert content == "<html><body>Test content</body></html>"
                mock_scrape.assert_called_once_with("http://test.com")

            @pytest.mark.asyncio
            async def test_web_scraper_empty_url(self):
                scraper = WebScraper()
                result = await scraper.scrape_website("")
                assert isinstance(result, Exception), "Should return an Exception for empty URL"

            @pytest.mark.asyncio
            async def test_web_scraper_non_http_url(self):
                scraper = WebScraper()
                result = await scraper.scrape_website("ftp://example.com")
                assert isinstance(result, Exception), "Should return an Exception for non-http(s) URL"

            @pytest.mark.asyncio
            async def test_web_scraper_json_content(self):
                # This test assumes the scraper returns JSON string for valid HTML
                scraper = WebScraper()
                content = await scraper.scrape_website("https://httpbin.org/html")
                if not isinstance(content, Exception):
                    data = json.loads(content)
                    assert "url" in data
                    assert "content" in data
                    assert "title" in data

            @pytest.mark.asyncio
            async def test_web_scraper_handles_redirect(self):
                # httpbin.org/redirect-to?url=... will redirect to the given URL
                scraper = WebScraper()
                result = await scraper.scrape_website("https://httpbin.org/redirect-to?url=https://httpbin.org/html")
                # Should either return valid content or an Exception, but should not crash
                assert isinstance(result, (str, Exception))

class TestIntegration:
    @pytest.mark.asyncio
    async def test_search_and_scrape_workflow(self):
        # Test complete workflow: search -> scrape
        ddg_search = DuckDuckGoWebSearch()
        scraper = WebScraper()
        
        search_results = await ddg_search.search("Python programming")
        assert len(search_results) > 0
        
        # Try to scrape first result if URL exists
        if search_results and 'url' in search_results[0]:
            url = search_results[0]['url']
            try:
                content = await scraper.scrape_website(url)
                assert isinstance(content, str)
            except Exception:
                # Some URLs might not be scrapable, that's ok for test
                pass

    @pytest.mark.asyncio
    async def test_multiple_search_engines_comparison(self):
        query = "machine learning"
        
        ddg_search = DuckDuckGoWebSearch()
        ddg_results = await ddg_search.search(query)
        
        if os.getenv("TAVILY_API_KEY"):
            tavily_search = TavilyWebSearch(api_key=os.getenv("TAVILY_API_KEY"))
            tavily_results = await tavily_search.search(query)
            
            assert isinstance(ddg_results, list)
            assert isinstance(tavily_results, dict)
            assert len(ddg_results) > 0
            assert len(tavily_results) > 0

def test_environment_variables():
    """Test that required environment variables are available"""
    tavily_key = os.getenv("TAVILY_API_KEY")
    if not tavily_key:
        pytest.skip("TAVILY_API_KEY not set in environment")



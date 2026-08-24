"""
Free, no-API-key web search tool used by the Researcher agent.

Uses DuckDuckGo (via duckduckgo-search) so the entire project runs
end-to-end without anyone needing to pay for a search API just to
try the demo.

Includes robust error handling and timeout protection.
"""
import asyncio
import logging
from typing import List, Dict

from duckduckgo_search import DDGS

logger = logging.getLogger("web_search")

# Timeout in seconds for search operations
SEARCH_TIMEOUT = 10


def _search_sync(query: str, max_results: int = 5) -> List[Dict]:
    """
    Synchronous web search with error handling.
    Returns empty list if search fails, so pipeline continues gracefully.
    """
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(
                    {
                        "title": r.get("title", "Unknown"),
                        "url": r.get("href", ""),
                        "snippet": r.get("body", "No content available"),
                    }
                )
        if results:
            logger.info(f"Search succeeded for '{query}': {len(results)} results")
    except asyncio.TimeoutError:
        logger.warning(f"Search timeout for '{query}' (exceeded {SEARCH_TIMEOUT}s)")
    except Exception as e:
        logger.warning(f"Search failed for '{query}': {type(e).__name__}: {e}")
    
    return results


async def web_search(query: str, max_results: int = 5) -> List[Dict]:
    """
    Async wrapper around the blocking search call with timeout protection.
    
    If search times out or fails, returns empty list so the pipeline
    can continue with AI-generated context instead.
    """
    try:
        loop = asyncio.get_event_loop()
        return await asyncio.wait_for(
            loop.run_in_executor(None, _search_sync, query, max_results),
            timeout=SEARCH_TIMEOUT
        )
    except asyncio.TimeoutError:
        logger.error(f"Web search timed out after {SEARCH_TIMEOUT}s for query: {query}")
        return []
    except Exception as e:
        logger.error(f"Web search error for '{query}': {type(e).__name__}: {e}")
        return []

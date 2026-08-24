"""
Free, no-API-key web search tool used by the Researcher agent.

Uses DuckDuckGo (via duckduckgo-search) so the entire project runs
end-to-end without anyone needing to pay for a search API just to
try the demo.
"""
import asyncio
import logging
from typing import List, Dict

from duckduckgo_search import DDGS

logger = logging.getLogger("web_search")


def _search_sync(query: str, max_results: int = 5) -> List[Dict]:
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(
                    {
                        "title": r.get("title", ""),
                        "url": r.get("href", ""),
                        "snippet": r.get("body", ""),
                    }
                )
    except Exception as e:
        logger.warning(f"Search failed for '{query}': {e}")
    return results


async def web_search(query: str, max_results: int = 5) -> List[Dict]:
    """Async wrapper around the blocking search call."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _search_sync, query, max_results)

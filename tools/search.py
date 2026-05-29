import os
from typing import List, Dict
from tavily import TavilyClient

_client = None


def get_client() -> TavilyClient:
    global _client
    if _client is None:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY not set in environment")
        _client = TavilyClient(api_key=api_key)
    return _client


def tavily_search(query: str, max_results: int = 5) -> List[Dict]:
    try:
        client = get_client()
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results,
            include_answer=False,
            include_raw_content=False,
        )
        return response.get("results", [])
    except Exception as e:
        print(f"   ⚠️  Search error for '{query}': {e}")
        return []
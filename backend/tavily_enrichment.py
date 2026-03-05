"""
tavily_enrichment.py
--------------------
Real-time market context enrichment using Tavily Search API.
Used in two places:
  1. /predict  → appends market_context to each prediction response
  2. /chat     → replaces static CAMPAIGN_KNOWLEDGE with live web data
"""

import os
from functools import lru_cache
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


@lru_cache(maxsize=128)
def fetch_market_context(region: str, traffic_type: str) -> dict:
    """
    Fetch real-time market trends for a visitor segment.
    LRU-cached so identical inputs reuse results (saves credits).

    Returns:
        {
            "summary": str,       # 3-bullet plain-text summary
            "sources": [str],     # source URLs
            "enriched": bool      # False if Tavily call failed
        }
    """
    query = f"online shopping purchase intent {region} {traffic_type} 2025 trends"
    try:
        results = get_client().search(
            query=query,
            search_depth="basic",
            max_results=3
        )
        hits = results.get("results", [])

        bullets = []
        sources = []
        for r in hits:
            title = r.get("title", "").strip()
            snippet = r.get("content", "")[:180].strip()
            url = r.get("url", "")
            if title and snippet:
                bullets.append(f"• {title}: {snippet}")
                sources.append(url)

        return {
            "query": query,
            "summary": "\n".join(bullets),
            "sources": sources,
            "enriched": True
        }
    except Exception as e:
        return {
            "query": query,
            "summary": "",
            "sources": [],
            "enriched": False,
            "error": str(e)
        }


def fetch_campaign_knowledge() -> str:
    """
    Used by rag_engine.py to replace static CAMPAIGN_KNOWLEDGE
    with live web intelligence about digital campaign targeting trends.
    Falls back to empty string if Tavily unavailable.
    """
    queries = [
        "digital campaign targeting conversion rate optimization 2025",
        "online shopper purchase intent signals machine learning 2025",
        "ad spend ROI improvement AI targeting ecommerce 2025"
    ]
    sections = []
    try:
        client = get_client()
        for q in queries:
            results = client.search(query=q, search_depth="basic", max_results=2)
            for r in results.get("results", []):
                snippet = r.get("content", "")[:300].strip()
                if snippet:
                    sections.append(snippet)
        return "\n\n".join(sections)
    except Exception:
        return ""  # rag_engine will fall back to static knowledge

"""
===========================================================
QuantFormer Backend — Financial News Loader
===========================================================

Fetches live financial news from News API (newsapi.org).
Implements TTL-based caching for resilience.

IMPORTANT (Change 1):
  Financial PhraseBank is a TRAINING DATASET ONLY and is
  NEVER used as a runtime fallback. If the news provider
  is unavailable:
    1. Return cached recent news if available.
    2. If cache is empty, return:
       "No recent financial news available."

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

import time
import logging
from typing import Dict, List, Optional, Any

import httpx

logger = logging.getLogger(__name__)


class NewsLoader:
    """
    Fetches financial news headlines from News API with
    TTL-based in-memory caching.

    Usage:
        loader = NewsLoader(api_key="...", cache_ttl=300)
        articles = await loader.fetch(query="stock market", limit=10)
    """

    def __init__(
        self,
        api_key: str = "",
        api_url: str = "https://newsapi.org/v2/everything",
        cache_ttl: int = 300,
    ):
        self._api_key = api_key
        self._api_url = api_url
        self._cache_ttl = cache_ttl
        self._cache: List[Dict[str, Any]] = []
        self._cache_timestamp: float = 0.0

    def _is_cache_valid(self) -> bool:
        """Check if cached news data is still within TTL."""
        if not self._cache:
            return False
        age = time.time() - self._cache_timestamp
        return age < self._cache_ttl

    async def fetch(
        self,
        query: str = "stock market finance",
        limit: int = 10,
    ) -> Dict[str, Any]:
        """
        Fetch latest financial news articles.

        Returns
        -------
        dict with keys:
            articles : list of article dicts
            total_articles : int
            source : str (live_api / cache / unavailable)
            cached : bool
            message : str or None
        """
        # Return cached data if still valid
        if self._is_cache_valid():
            logger.info("Returning cached financial news")
            return {
                "articles": self._cache[:limit],
                "total_articles": min(len(self._cache), limit),
                "source": "cache",
                "cached": True,
                "message": None,
            }

        # Attempt live fetch from News API
        try:
            articles = await self._fetch_from_api(query, limit)

            if articles:
                # Update cache
                self._cache = articles
                self._cache_timestamp = time.time()
                logger.info(f"Fetched {len(articles)} articles from News API")

                return {
                    "articles": articles[:limit],
                    "total_articles": min(len(articles), limit),
                    "source": "live_api",
                    "cached": False,
                    "message": None,
                }

        except Exception as e:
            logger.warning(f"News API unavailable: {e}")

        # Fallback to stale cache
        if self._cache:
            logger.info("Returning stale cached financial news")
            return {
                "articles": self._cache[:limit],
                "total_articles": min(len(self._cache), limit),
                "source": "cache",
                "cached": True,
                "message": "Using cached news data. Live news feed is temporarily unavailable.",
            }

        # No cache available — return empty with message
        logger.warning("No financial news available (no cache, no API)")
        return {
            "articles": [],
            "total_articles": 0,
            "source": "unavailable",
            "cached": False,
            "message": "No recent financial news available.",
        }

    async def _fetch_from_api(
        self, query: str, limit: int
    ) -> List[Dict[str, Any]]:
        """
        Fetch news from newsapi.org using httpx async client.
        """
        if not self._api_key:
            logger.warning(
                "NEWS_API_KEY not configured. Cannot fetch live news."
            )
            return []

        params = {
            "q": query,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": min(limit, 100),
            "apiKey": self._api_key,
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(self._api_url, params=params)
            response.raise_for_status()
            data = response.json()

        raw_articles = data.get("articles", [])

        articles = []
        for article in raw_articles:
            articles.append({
                "headline": article.get("title", ""),
                "source": (
                    article.get("source", {}).get("name")
                    if isinstance(article.get("source"), dict)
                    else article.get("source")
                ),
                "published_at": article.get("publishedAt"),
                "url": article.get("url"),
                "description": article.get("description"),
            })

        return articles

    def get_latest_headline(self) -> Optional[str]:
        """Return the most recent cached headline, or None."""
        if self._cache:
            return self._cache[0].get("headline")
        return None

    def clear_cache(self) -> None:
        """Clear the news cache."""
        self._cache.clear()
        self._cache_timestamp = 0.0

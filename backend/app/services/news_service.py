"""
===========================================================
QuantFormer Backend — News Service
===========================================================

Business logic for financial news aggregation and caching.
Delegates fetching to the NewsLoader.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

import logging
from typing import Dict, Any

from app.loaders.news_loader import NewsLoader
from app.utils.helpers import utc_now_iso

logger = logging.getLogger(__name__)


class NewsService:
    """
    Financial news service layer.

    Coordinates between the NewsLoader and API endpoints.
    """

    def __init__(self, news_loader: NewsLoader):
        self._loader = news_loader

    async def get_latest_news(
        self,
        query: str = "stock market finance",
        limit: int = 10,
    ) -> Dict[str, Any]:
        """
        Fetch latest financial news.

        Parameters
        ----------
        query : str — Search query for news
        limit : int — Maximum number of articles

        Returns
        -------
        dict ready for NewsResponse schema
        """
        result = await self._loader.fetch(query=query, limit=limit)

        return {
            "success": True,
            "total_articles": result["total_articles"],
            "articles": result["articles"],
            "source": result["source"],
            "cached": result["cached"],
            "message": result.get("message"),
            "timestamp": utc_now_iso(),
        }

    def get_latest_headline(self) -> str:
        """Get the most recent cached headline for insight analysis."""
        headline = self._loader.get_latest_headline()
        return headline if headline else ""

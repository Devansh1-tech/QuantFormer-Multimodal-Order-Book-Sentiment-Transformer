from typing import Dict, Any, List
from backend.app.loaders.news_loader import fetch_news_cascade

async def get_latest_news(ticker: str, limit: int = 10) -> Dict[str, Any]:
    """
    Fetches latest financial news using the resilient 7-tier provider cascade.
    """
    return await fetch_news_cascade(ticker, limit)

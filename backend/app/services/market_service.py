from typing import Dict, Any, List
import asyncio
from backend.app.loaders.market_loader import fetch_market_data

async def get_market_summary(ticker: str) -> Dict[str, Any]:
    """
    Fetches market summary for the dashboard or prediction endpoints.
    """
    return await fetch_market_data(ticker)

async def get_market_features(ticker: str) -> List[List[float]]:
    """
    Fetches just the 100x143 feature tensor for the prediction service.
    """
    data = await fetch_market_data(ticker)
    return data["features"]

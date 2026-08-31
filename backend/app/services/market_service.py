"""
===========================================================
QuantFormer Backend — Market Service
===========================================================

Business logic for market data processing.
Delegates fetching to the MarketLoader and transforms
data into response schemas.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

import logging
from typing import Dict, Any

from app.loaders.market_loader import MarketLoader, MarketDataUnavailable
from app.utils.helpers import utc_now_iso

logger = logging.getLogger(__name__)


class MarketService:
    """
    Market data service layer.

    Coordinates between the MarketLoader and API endpoints.
    """

    def __init__(self, market_loader: MarketLoader):
        self._loader = market_loader

    async def get_market_data(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch market data for the given symbol.

        Parameters
        ----------
        symbol : str — Stock ticker symbol

        Returns
        -------
        dict ready for MarketResponse schema

        Raises
        ------
        MarketDataUnavailable
            If no data is available (→ HTTP 503)
        """
        data = await self._loader.fetch(symbol)

        return {
            "success": True,
            "symbol": symbol.upper(),
            "data": data,
            "source": "yahoo_finance",
            "cached": data.get("cached", False),
            "timestamp": utc_now_iso(),
        }

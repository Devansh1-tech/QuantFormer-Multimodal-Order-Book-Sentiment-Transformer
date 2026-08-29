"""
===========================================================
QuantFormer Backend — Market Data Loader
===========================================================

Fetches live market data from Yahoo Finance for any dynamic
stock symbol. Implements a TTL-based in-memory cache.

IMPORTANT (Change 1):
  FI-2010 is a TRAINING DATASET ONLY and is NEVER used as
  a runtime fallback. If Yahoo Finance is unavailable:
    1. Return cached data if available.
    2. Otherwise raise MarketDataUnavailable (→ HTTP 503).

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

import time
import logging
from typing import Dict, Optional, Any

logger = logging.getLogger(__name__)


class MarketDataUnavailable(Exception):
    """Raised when market data cannot be fetched and no cache exists."""
    pass


class MarketLoader:
    """
    Fetches live stock quotes from Yahoo Finance with
    TTL-based in-memory caching per symbol.

    Usage:
        loader = MarketLoader(cache_ttl=60)
        data = await loader.fetch("AAPL")
    """

    def __init__(self, cache_ttl: int = 60):
        self._cache_ttl = cache_ttl
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_timestamps: Dict[str, float] = {}

    def _is_cache_valid(self, symbol: str) -> bool:
        """Check if cached data for a symbol is still within TTL."""
        if symbol not in self._cache_timestamps:
            return False
        age = time.time() - self._cache_timestamps[symbol]
        return age < self._cache_ttl

    async def fetch(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch live market data for the given symbol.

        Returns cached data if Yahoo Finance is unavailable
        but cache is still populated. Raises MarketDataUnavailable
        if neither live data nor cache is available.

        Parameters
        ----------
        symbol : str
            Stock ticker symbol (e.g. AAPL, RELIANCE.NS)

        Returns
        -------
        dict with keys: symbol, company_name, price, open, high,
             low, close, volume, daily_change, daily_change_percent,
             market_cap, currency, exchange, timestamp, cached

        Raises
        ------
        MarketDataUnavailable
            If Yahoo Finance is unreachable and no cache exists.
        """
        symbol = symbol.upper().strip()

        # Return cached data if still valid
        if self._is_cache_valid(symbol):
            logger.info(f"Returning cached market data for {symbol}")
            cached = self._cache[symbol].copy()
            cached["cached"] = True
            return cached

        # Attempt live fetch from Yahoo Finance
        try:
            data = await self._fetch_from_yahoo(symbol)
            # Update cache
            self._cache[symbol] = data
            self._cache_timestamps[symbol] = time.time()
            data["cached"] = False
            logger.info(f"Fetched live market data for {symbol}")
            return data

        except Exception as e:
            logger.warning(
                f"Yahoo Finance unavailable for {symbol}: {e}"
            )

            # Fallback to stale cache if any data was previously fetched
            if symbol in self._cache:
                logger.info(
                    f"Returning stale cached market data for {symbol}"
                )
                cached = self._cache[symbol].copy()
                cached["cached"] = True
                return cached

            # No cache available — raise 503
            raise MarketDataUnavailable(
                f"Market data unavailable for {symbol}. "
                f"Yahoo Finance is unreachable and no cached data exists."
            )

    async def _fetch_from_yahoo(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch real-time stock data from Yahoo Finance using yfinance.

        Runs the synchronous yfinance calls in a thread pool to avoid
        blocking the async event loop.
        """
        import asyncio
        import yfinance as yf
        from datetime import datetime, timezone

        def _sync_fetch() -> Dict[str, Any]:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            if not info or info.get("regularMarketPrice") is None:
                # yfinance sometimes returns empty info for invalid symbols
                raise ValueError(f"No data returned for symbol: {symbol}")

            price = info.get("regularMarketPrice", 0.0)
            prev_close = info.get("regularMarketPreviousClose", 0.0)
            daily_change = round(price - prev_close, 4) if prev_close else 0.0
            daily_change_pct = (
                round((daily_change / prev_close) * 100, 4) if prev_close else 0.0
            )

            return {
                "symbol": symbol,
                "company_name": info.get("shortName", info.get("longName", symbol)),
                "price": round(price, 4),
                "open": round(info.get("regularMarketOpen", 0.0), 4),
                "high": round(info.get("regularMarketDayHigh", 0.0), 4),
                "low": round(info.get("regularMarketDayLow", 0.0), 4),
                "close": round(prev_close, 4),
                "volume": int(info.get("regularMarketVolume", 0)),
                "daily_change": daily_change,
                "daily_change_percent": daily_change_pct,
                "market_cap": info.get("marketCap"),
                "currency": info.get("currency", "USD"),
                "exchange": info.get("exchange"),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _sync_fetch)

    def get_cached(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Return cached data for a symbol, or None."""
        symbol = symbol.upper().strip()
        if symbol in self._cache:
            data = self._cache[symbol].copy()
            data["cached"] = True
            return data
        return None

    def clear_cache(self, symbol: Optional[str] = None) -> None:
        """Clear cache for a specific symbol or all symbols."""
        if symbol:
            symbol = symbol.upper().strip()
            self._cache.pop(symbol, None)
            self._cache_timestamps.pop(symbol, None)
        else:
            self._cache.clear()
            self._cache_timestamps.clear()

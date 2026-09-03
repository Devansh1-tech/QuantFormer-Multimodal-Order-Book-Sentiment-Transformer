import yfinance as yf
import pandas as pd
import asyncio
from typing import Optional, Dict, Any

from backend.app.loaders.indicators import synthesize_market_features
from backend.app.core.exceptions import MarketDataException

async def fetch_market_data(ticker: str, interval: str = "5m", period: str = "1d") -> Dict[str, Any]:
    """
    Fetches real-time market data from Yahoo Finance asynchronously.
    """
    try:
        # yfinance is synchronous, so we run it in a threadpool to prevent blocking the event loop
        loop = asyncio.get_event_loop()
        ticker_obj = yf.Ticker(ticker)
        
        # Fetch history
        df = await loop.run_in_executor(None, lambda: ticker_obj.history(period=period, interval=interval))
        
        if df.empty:
            raise MarketDataException(f"No data returned for ticker {ticker}.")
            
        # Synthesize features to match TFT 100x143 requirement
        features = synthesize_market_features(df, target_sequence_length=100, target_features=143)
        
        # Get latest info for display
        latest = df.iloc[-1]
        
        return {
            "ticker": ticker,
            "current_price": float(latest['Close']),
            "volume": int(latest['Volume']),
            "high": float(latest['High']),
            "low": float(latest['Low']),
            "features": features.tolist(),
            "timestamp": str(latest.name)
        }
        
    except Exception as e:
        if isinstance(e, MarketDataException):
            raise
        raise MarketDataException(f"Failed to fetch market data: {str(e)}")

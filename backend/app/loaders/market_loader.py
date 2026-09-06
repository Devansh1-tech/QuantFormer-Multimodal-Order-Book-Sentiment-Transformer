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
        first_open = float(df.iloc[0]['Open'])
        current_close = float(latest['Close'])
        daily_change = current_close - first_open
        daily_change_percent = (daily_change / first_open * 100) if first_open > 0 else 0.0
        
        return {
            "ticker": ticker,
            "current_price": round(current_close, 2),
            "open": round(first_open, 2),
            "high": round(float(df['High'].max()), 2),
            "low": round(float(df['Low'].min()), 2),
            "close": round(current_close, 2),
            "volume": int(df['Volume'].sum()) if df['Volume'].sum() > 0 else int(latest['Volume']),
            "daily_change": round(daily_change, 2),
            "daily_change_percent": round(daily_change_percent, 2),
            "features": features.tolist(),
            "timestamp": str(latest.name)
        }
        
    except Exception as e:
        if isinstance(e, MarketDataException):
            raise
        raise MarketDataException(f"Failed to fetch market data: {str(e)}")

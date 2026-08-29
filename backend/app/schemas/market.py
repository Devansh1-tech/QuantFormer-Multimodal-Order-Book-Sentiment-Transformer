"""
===========================================================
QuantFormer Backend — Market Data Schemas
===========================================================

Schemas for live market data from Yahoo Finance.
Supports dynamic stock symbols via ?symbol= query param.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from typing import Optional

from pydantic import BaseModel, Field


class MarketQuote(BaseModel):
    """Live stock quote data."""

    symbol: str = Field(description="Stock ticker symbol (e.g. AAPL)")
    company_name: str = Field(description="Company name")
    price: float = Field(description="Current / last traded price")
    open: float = Field(description="Market open price")
    high: float = Field(description="Day high price")
    low: float = Field(description="Day low price")
    close: float = Field(description="Previous close price")
    volume: int = Field(description="Trading volume")
    daily_change: float = Field(description="Price change from previous close")
    daily_change_percent: float = Field(description="Percentage change from previous close")
    market_cap: Optional[float] = Field(default=None, description="Market capitalization")
    currency: str = Field(default="USD", description="Trading currency")
    exchange: Optional[str] = Field(default=None, description="Stock exchange name")
    timestamp: str = Field(description="Data timestamp (ISO 8601)")


class MarketResponse(BaseModel):
    """Response for GET /api/v1/market?symbol=."""

    success: bool = Field(default=True)
    symbol: str = Field(description="Requested stock symbol")
    data: MarketQuote = Field(description="Market quote data")
    source: str = Field(default="yahoo_finance", description="Data source")
    cached: bool = Field(default=False, description="Whether data is from cache")
    timestamp: str = Field(description="Response timestamp (ISO 8601)")

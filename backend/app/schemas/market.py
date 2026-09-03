from pydantic import BaseModel
from typing import Optional

class BackendMarketQuote(BaseModel):
    symbol: str
    company_name: str
    price: float
    open: float
    high: float
    low: float
    close: float
    volume: int
    daily_change: float
    daily_change_percent: float
    timestamp: str

class BackendMarketResponse(BaseModel):
    success: bool
    symbol: str
    data: BackendMarketQuote
    source: str
    cached: bool
    timestamp: str

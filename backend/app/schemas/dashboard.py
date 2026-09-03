from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from backend.app.schemas.market import BackendMarketQuote
from backend.app.schemas.news import BackendNewsArticle

class BackendDashboardSystemStatus(BaseModel):
    status: str
    uptime: str
    models_loaded: int
    total_models: int
    gpu_available: bool
    device: str

class BackendDashboardResponse(BaseModel):
    success: bool
    symbol: str
    market: Optional[BackendMarketQuote] = None
    news: Optional[Dict[str, Any]] = None
    prediction: Optional[Dict[str, Any]] = None
    sentiment: Optional[Dict[str, Any]] = None
    insight: Optional[Dict[str, Any]] = None
    system: BackendDashboardSystemStatus
    response_time_ms: float
    timestamp: str

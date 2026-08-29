"""
===========================================================
QuantFormer Backend — Dashboard Aggregator Schemas
===========================================================

Response schema for GET /api/v1/dashboard?symbol=

Aggregates market data, news, TFT prediction, FinBERT
sentiment, Fusion AI insight, system status, response time,
and model versions into a single response.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class DashboardMarket(BaseModel):
    """Market data section of the dashboard."""

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
    currency: str = "USD"


class DashboardNews(BaseModel):
    """News section of the dashboard."""

    total_articles: int
    articles: List[Dict]
    source: str
    message: Optional[str] = None


class DashboardPrediction(BaseModel):
    """TFT prediction section of the dashboard."""

    prediction: str
    market_trend: str
    confidence: float
    probabilities: Dict[str, float]
    model_name: str
    model_version: str
    latency_ms: float


class DashboardSentiment(BaseModel):
    """FinBERT sentiment section of the dashboard."""

    sentiment: str
    confidence: float
    scores: Dict[str, float]
    analyzed_text: Optional[str] = None


class DashboardInsight(BaseModel):
    """Multimodal AI insight section of the dashboard."""

    overall_insight: str
    market_trend: str
    news_sentiment: str
    explanation: List[str]
    disclaimer: str


class DashboardSystemStatus(BaseModel):
    """System status section of the dashboard."""

    status: str
    uptime: str
    models_loaded: int
    total_models: int
    gpu_available: bool
    device: str


class DashboardResponse(BaseModel):
    """
    Complete aggregated dashboard response for
    GET /api/v1/dashboard?symbol=

    This is the primary endpoint consumed by the React frontend.
    """

    success: bool = Field(default=True)
    symbol: str = Field(description="Requested stock symbol")
    market: Optional[DashboardMarket] = Field(
        default=None, description="Live market data"
    )
    news: Optional[DashboardNews] = Field(
        default=None, description="Latest financial news"
    )
    prediction: Optional[DashboardPrediction] = Field(
        default=None, description="TFT market prediction"
    )
    sentiment: Optional[DashboardSentiment] = Field(
        default=None, description="FinBERT news sentiment"
    )
    insight: Optional[DashboardInsight] = Field(
        default=None, description="Multimodal AI insight"
    )
    system: DashboardSystemStatus = Field(
        description="System status"
    )
    response_time_ms: float = Field(
        description="Total dashboard aggregation time in milliseconds"
    )
    timestamp: str = Field(description="Response timestamp (ISO 8601)")

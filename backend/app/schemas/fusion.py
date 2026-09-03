from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class InsightRequest(BaseModel):
    ticker: Optional[str] = None
    symbol: Optional[str] = None
    headline: Optional[str] = None
    market_prediction: Optional[str] = None
    news_text: Optional[str] = None
    market_confidence: Optional[float] = None

class BackendInsightResponse(BaseModel):
    success: bool
    market_trend: str
    news_sentiment: str
    news_confidence: float
    overall_insight: str
    disclaimer: str
    latency_ms: float
    timestamp: str

class ExplainRequest(BaseModel):
    market_prediction: str
    confidence: float
    news_text: str

class BackendExplainResponse(BaseModel):
    success: bool
    market_prediction: str
    confidence: float
    news_sentiment: str
    overall_insight: str
    explanation: List[str]
    disclaimer: str
    latency_ms: float
    timestamp: str

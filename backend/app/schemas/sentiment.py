from pydantic import BaseModel
from typing import Dict, Optional

class SentimentRequest(BaseModel):
    text: str
    ticker: Optional[str] = None

class BackendSentimentResponse(BaseModel):
    success: bool
    text: str
    sentiment: str
    confidence: float
    scores: Dict[str, float]
    explanation: str
    latency_ms: float
    timestamp: str

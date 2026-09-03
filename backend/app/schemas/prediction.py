from pydantic import BaseModel
from typing import Dict, Optional, List

class PredictionRequest(BaseModel):
    symbol: Optional[str] = None
    ticker: Optional[str] = None
    features: Optional[List[List[float]]] = None

class BackendPredictResponse(BaseModel):
    success: bool
    prediction: str
    market_trend: str
    confidence: float
    probabilities: Dict[str, float]
    latency_ms: float
    model_name: str
    model_version: str
    timestamp: str

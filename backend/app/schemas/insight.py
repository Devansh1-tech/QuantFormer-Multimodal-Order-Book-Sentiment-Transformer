"""
===========================================================
QuantFormer Backend — Multimodal Insight Schemas
===========================================================

Request and response schemas for the AI Insight endpoint.
POST /api/v1/insight

Combines TFT market prediction + FinBERT news sentiment
+ Fusion model internally to produce an overall AI insight.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from typing import Optional

from pydantic import BaseModel, Field


class InsightRequest(BaseModel):
    """
    Request body for POST /api/v1/insight.

    Requires a market trend from the TFT prediction and
    news text for FinBERT sentiment analysis.
    """

    market_prediction: str = Field(
        description="TFT market prediction (Bullish / Neutral / Bearish)"
    )
    news_text: str = Field(
        description="Financial news text for sentiment analysis",
        min_length=1,
        max_length=2048,
    )
    market_confidence: Optional[float] = Field(
        default=None,
        description="TFT prediction confidence (0-100)"
    )


class InsightResponse(BaseModel):
    """Response body for POST /api/v1/insight."""

    success: bool = Field(default=True)
    market_trend: str = Field(
        description="Market trend from TFT (Bullish / Neutral / Bearish)"
    )
    market_confidence: Optional[float] = Field(
        default=None,
        description="TFT prediction confidence"
    )
    news_sentiment: str = Field(
        description="News sentiment from FinBERT (positive / negative / neutral)"
    )
    news_confidence: float = Field(
        description="FinBERT sentiment confidence"
    )
    overall_insight: str = Field(
        description=(
            "Synthesized AI insight "
            "(Strong Bullish / Bullish / Slightly Bullish / Neutral / "
            "Slightly Bearish / Bearish / Strong Bearish)"
        )
    )
    disclaimer: str = Field(
        description="Mandatory compliance disclaimer"
    )
    latency_ms: float = Field(
        description="Total inference latency in milliseconds"
    )
    timestamp: str = Field(description="Analysis timestamp (ISO 8601)")

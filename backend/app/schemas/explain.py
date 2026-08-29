"""
===========================================================
QuantFormer Backend — Explainability Schemas
===========================================================

Request and response schemas for the Explainability endpoint.
POST /api/v1/explain

Combines TFT prediction + FinBERT sentiment + Fusion insight
into structured human-readable explanations.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class ExplainRequest(BaseModel):
    """
    Request body for POST /api/v1/explain.

    Requires market prediction context and news text to
    generate a comprehensive multimodal explanation.
    """

    market_prediction: str = Field(
        description="TFT market prediction (Bullish / Neutral / Bearish)"
    )
    confidence: float = Field(
        description="TFT prediction confidence (0-100)"
    )
    news_text: str = Field(
        description="Financial news text for sentiment analysis",
        min_length=1,
        max_length=2048,
    )


class ExplainResponse(BaseModel):
    """
    Response body for POST /api/v1/explain.

    Provides structured reasoning combining market dynamics,
    news sentiment, and fusion confidence into a list of
    human-readable explanation statements.
    """

    success: bool = Field(default=True)
    market_prediction: str = Field(
        description="Market prediction (Bullish / Neutral / Bearish)"
    )
    confidence: float = Field(
        description="TFT prediction confidence (0-100)"
    )
    news_sentiment: str = Field(
        description="FinBERT sentiment (positive / negative / neutral)"
    )
    overall_insight: str = Field(
        description="Synthesized AI insight label"
    )
    explanation: List[str] = Field(
        description="List of human-readable reasoning statements"
    )
    disclaimer: str = Field(
        description="Mandatory compliance disclaimer"
    )
    latency_ms: float = Field(
        description="Total inference latency in milliseconds"
    )
    timestamp: str = Field(description="Explanation timestamp (ISO 8601)")

"""
===========================================================
QuantFormer Backend — Sentiment Schemas
===========================================================

Request and response schemas for the FinBERT sentiment
analysis endpoint.  POST /api/v1/sentiment

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from typing import Dict

from pydantic import BaseModel, Field


class SentimentRequest(BaseModel):
    """
    Request body for POST /api/v1/sentiment.

    Accepts a financial news headline or text passage.
    """

    text: str = Field(
        description="Financial news text to analyze",
        min_length=1,
        max_length=2048,
    )


class SentimentResponse(BaseModel):
    """Response body for POST /api/v1/sentiment."""

    success: bool = Field(default=True)
    text: str = Field(description="Original input text")
    sentiment: str = Field(
        description="Predicted sentiment label (positive / negative / neutral)"
    )
    confidence: float = Field(
        description="Sentiment confidence as percentage (0-100)"
    )
    scores: Dict[str, float] = Field(
        description="Per-class scores {positive: %, negative: %, neutral: %}"
    )
    explanation: str = Field(
        description="Human-readable explanation of the sentiment result"
    )
    model_name: str = Field(
        default="FinBERT",
        description="Model used for sentiment analysis"
    )
    latency_ms: float = Field(
        description="Inference latency in milliseconds"
    )
    timestamp: str = Field(description="Analysis timestamp (ISO 8601)")

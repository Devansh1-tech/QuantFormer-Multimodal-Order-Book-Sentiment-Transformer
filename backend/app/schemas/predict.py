"""
===========================================================
QuantFormer Backend — Prediction Schemas
===========================================================

Request and response schemas for the TFT prediction endpoint.
POST /api/v1/predict

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    """
    Request body for POST /api/v1/predict.

    Accepts market features as a 2D array of shape (100, 143)
    representing a sequence of 100 time steps with 143 features
    from Level-2 Limit Order Book data.
    """

    features: List[List[float]] = Field(
        description=(
            "Market feature sequence of shape (100, 143). "
            "Each inner list is a 143-dimensional feature vector."
        ),
    )
    symbol: Optional[str] = Field(
        default=None,
        description="Stock symbol for context labeling (optional)",
    )


class PredictResponse(BaseModel):
    """Response body for POST /api/v1/predict."""

    success: bool = Field(default=True)
    prediction: str = Field(
        description="Predicted market direction (Down / Stable / Up)"
    )
    market_trend: str = Field(
        description="Human-readable trend (Bearish / Neutral / Bullish)"
    )
    confidence: float = Field(
        description="Prediction confidence as percentage (0-100)"
    )
    probabilities: Dict[str, float] = Field(
        description="Class probabilities as percentages {Down: %, Stable: %, Up: %}"
    )
    latency_ms: float = Field(
        description="Inference latency in milliseconds"
    )
    model_name: str = Field(
        default="Temporal Fusion Transformer",
        description="Name of the model used for prediction"
    )
    model_version: str = Field(
        default="1.0.0",
        description="Model version"
    )
    symbol: Optional[str] = Field(
        default=None,
        description="Stock symbol context"
    )
    timestamp: str = Field(description="Prediction timestamp (ISO 8601)")

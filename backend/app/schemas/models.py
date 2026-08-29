"""
===========================================================
QuantFormer Backend — Model Registry Schemas
===========================================================

Schemas for the GET /api/v1/models endpoint that returns
detailed information about all loaded AI models.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class ModelDetail(BaseModel):
    """Detailed information about a single AI model."""

    name: str = Field(description="Model display name")
    key: str = Field(description="Internal model key (tft/finbert/fusion)")
    version: str = Field(description="Model version")
    architecture: str = Field(description="Model architecture description")
    role: str = Field(description="Model's role in the system")
    loaded: bool = Field(description="Whether model is loaded and ready")
    checkpoint_path: str = Field(description="Checkpoint file path")
    checkpoint_exists: bool = Field(description="Whether checkpoint file exists on disk")
    device: str = Field(description="Device the model is on (cpu/cuda)")
    accuracy: Optional[float] = Field(default=None, description="Validation accuracy (%)")
    output_classes: Optional[int] = Field(default=None, description="Number of output classes")
    embedding_dim: Optional[int] = Field(default=None, description="Embedding dimension (for FinBERT)")


class ModelsResponse(BaseModel):
    """Response for GET /api/v1/models."""

    total_models: int = Field(description="Total number of models in registry")
    loaded_models: int = Field(description="Number of successfully loaded models")
    models: List[ModelDetail] = Field(description="Detailed model information")
    timestamp: str = Field(description="ISO 8601 timestamp")

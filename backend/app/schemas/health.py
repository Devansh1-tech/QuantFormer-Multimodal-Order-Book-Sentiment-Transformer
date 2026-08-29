"""
===========================================================
QuantFormer Backend — Health Schemas
===========================================================

Expanded health and system status response schemas.
Includes model status, GPU, CPU, RAM, Kafka, and uptime.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ModelHealthStatus(BaseModel):
    """Status of a single loaded model."""

    name: str = Field(description="Model display name")
    loaded: bool = Field(description="Whether the model is loaded successfully")
    checkpoint_exists: bool = Field(description="Whether the checkpoint file exists on disk")
    checkpoint_path: str = Field(description="Path to the checkpoint file")
    device: str = Field(description="Device the model is loaded on (cpu/cuda)")
    version: str = Field(default="1.0.0", description="Model version")


class GPUStatus(BaseModel):
    """GPU hardware status."""

    available: bool = Field(description="Whether CUDA GPU is available")
    device_name: Optional[str] = Field(default=None, description="GPU device name")
    memory_allocated_mb: Optional[float] = Field(default=None)
    memory_total_mb: Optional[float] = Field(default=None)
    cuda_version: Optional[str] = Field(default=None)


class SystemStatus(BaseModel):
    """CPU and RAM usage status."""

    cpu_usage_percent: float = Field(description="Current CPU usage percentage")
    ram_total_mb: float = Field(description="Total RAM in MB")
    ram_used_mb: float = Field(description="Used RAM in MB")
    ram_usage_percent: float = Field(description="RAM usage percentage")


class KafkaStatus(BaseModel):
    """Kafka connection and topic status."""

    enabled: bool = Field(description="Whether Kafka is enabled in configuration")
    connected: bool = Field(description="Whether Kafka broker is reachable")
    topics: List[str] = Field(default_factory=list, description="Configured Kafka topics")


class HealthResponse(BaseModel):
    """
    Comprehensive health check response returned by
    GET /api/v1/health.
    """

    status: str = Field(description="Overall backend status (healthy/degraded/unhealthy)")
    app_name: str = Field(description="Application name")
    version: str = Field(description="Application version")
    environment: str = Field(description="Current environment (development/production)")
    uptime: str = Field(description="Human-readable uptime")
    uptime_seconds: float = Field(description="Uptime in seconds")
    models: List[ModelHealthStatus] = Field(description="Status of all loaded models")
    gpu: GPUStatus = Field(description="GPU hardware status")
    system: SystemStatus = Field(description="CPU and RAM status")
    kafka: KafkaStatus = Field(description="Kafka connection status")
    timestamp: str = Field(description="ISO 8601 timestamp")

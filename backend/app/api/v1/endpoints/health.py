"""
===========================================================
QuantFormer Backend — Health Endpoint
===========================================================

GET /api/v1/health

Returns comprehensive system health including:
  - Backend status
  - Loaded models & checkpoint status
  - GPU status
  - CPU & RAM usage
  - Kafka status & topics
  - Application uptime

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from fastapi import APIRouter, Depends

from app.api.deps import (
    get_model_manager,
    get_streaming_service,
    get_settings,
)
from app.core.config import Settings
from app.models.model_manager import ModelManager
from app.kafka.streaming_service import StreamingService
from app.schemas.health import (
    HealthResponse,
    ModelHealthStatus,
    GPUStatus,
    SystemStatus,
    KafkaStatus,
)
from app.utils.helpers import (
    get_gpu_info,
    get_system_info,
    get_uptime_seconds,
    get_uptime_human,
    utc_now_iso,
)

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="System Health Check",
    description="Comprehensive health check including models, GPU, CPU, RAM, Kafka, and uptime.",
)
async def health_check(
    manager: ModelManager = Depends(get_model_manager),
    streaming: StreamingService = Depends(get_streaming_service),
    settings: Settings = Depends(get_settings),
) -> HealthResponse:
    """Return comprehensive system health status."""

    # Model status
    model_health = manager.get_health_status()
    models = [
        ModelHealthStatus(**status) for status in model_health.values()
    ]

    # Determine overall status
    if manager.all_loaded:
        status = "healthy"
    elif manager.is_healthy:
        status = "degraded"
    else:
        status = "unhealthy"

    # GPU info
    gpu_info = get_gpu_info()
    gpu = GPUStatus(**gpu_info)

    # System info
    sys_info = get_system_info()
    system = SystemStatus(**sys_info)

    # Kafka status
    kafka_status = streaming.get_status()
    kafka = KafkaStatus(**kafka_status)

    return HealthResponse(
        status=status,
        app_name=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
        uptime=get_uptime_human(),
        uptime_seconds=get_uptime_seconds(),
        models=models,
        gpu=gpu,
        system=system,
        kafka=kafka,
        timestamp=utc_now_iso(),
    )

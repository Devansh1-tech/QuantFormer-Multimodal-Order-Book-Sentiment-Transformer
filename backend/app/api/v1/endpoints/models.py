"""
===========================================================
QuantFormer Backend — Models Endpoint
===========================================================

GET /api/v1/models

Returns detailed information about all loaded AI models.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from fastapi import APIRouter, Depends

from backend.app.api.deps import get_model_manager
from backend.app.models.model_manager import ModelManager
from backend.app.schemas.models import ModelsResponse, ModelDetail
from backend.app.utils.constants import MODEL_INFO
from backend.app.utils.helpers import utc_now_iso

router = APIRouter()


@router.get(
    "/models",
    response_model=ModelsResponse,
    summary="Model Registry",
    description="Returns detailed information about all loaded AI models.",
)
async def get_models(
    manager: ModelManager = Depends(get_model_manager),
) -> ModelsResponse:
    """Return status and metadata of all registered models."""

    health = manager.get_health_status()
    models = []

    for key, info in MODEL_INFO.items():
        model_health = health.get(key, {})

        models.append(
            ModelDetail(
                name=info["name"],
                key=key,
                version=info["version"],
                architecture=info["architecture"],
                role=info["role"],
                loaded=model_health.get("loaded", False),
                checkpoint_path=model_health.get("checkpoint_path", ""),
                checkpoint_exists=model_health.get("checkpoint_exists", False),
                device=model_health.get("device", "cpu"),
                accuracy=info.get("accuracy"),
                output_classes=info.get("output_classes"),
                embedding_dim=info.get("embedding_dim"),
            )
        )

    return ModelsResponse(
        total_models=len(models),
        loaded_models=manager.loaded_count,
        models=models,
        timestamp=utc_now_iso(),
    )

"""
===========================================================
QuantFormer Backend — Insight Endpoint
===========================================================

POST /api/v1/insight

Generates multimodal AI insight combining TFT prediction,
FinBERT sentiment, and Fusion model (internal).

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from fastapi import APIRouter, Depends, HTTPException

from backend.app.api.deps import get_insight_service
from backend.app.services.insight_service import InsightService
from backend.app.schemas.insight import InsightRequest, InsightResponse

router = APIRouter()


@router.post(
    "/insight",
    response_model=InsightResponse,
    summary="Multimodal AI Insight",
    description=(
        "Generate an overall AI insight by combining TFT market prediction "
        "and FinBERT news sentiment. The Fusion model is used internally "
        "for enrichment."
    ),
)
async def generate_insight(
    request: InsightRequest,
    service: InsightService = Depends(get_insight_service),
) -> InsightResponse:
    """Generate multimodal AI market insight."""

    try:
        result = service.generate_insight(
            market_prediction=request.market_prediction,
            news_text=request.news_text,
            market_confidence=request.market_confidence,
        )
        return InsightResponse(**result)

    except RuntimeError as e:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "Model Unavailable",
                "message": str(e),
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Insight Generation Failed",
                "message": f"An error occurred: {str(e)}",
            },
        )

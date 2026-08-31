"""
===========================================================
QuantFormer Backend — Prediction Endpoint
===========================================================

POST /api/v1/predict

Run Temporal Fusion Transformer inference.
This is the ONLY production prediction endpoint.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_prediction_service
from app.services.prediction_service import PredictionService
from app.schemas.predict import PredictRequest, PredictResponse

router = APIRouter()


@router.post(
    "/predict",
    response_model=PredictResponse,
    summary="TFT Market Prediction",
    description=(
        "Run market direction prediction using the Temporal Fusion Transformer. "
        "Accepts a (100, 143) feature matrix from Level-2 Limit Order Book data."
    ),
)
async def predict(
    request: PredictRequest,
    service: PredictionService = Depends(get_prediction_service),
) -> PredictResponse:
    """Run TFT market prediction."""

    try:
        result = service.predict(
            features=request.features,
            symbol=request.symbol,
        )
        return PredictResponse(**result)

    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "Validation Error",
                "message": str(e),
            },
        )
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
                "error": "Prediction Failed",
                "message": f"An error occurred during prediction: {str(e)}",
            },
        )

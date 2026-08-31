"""
===========================================================
QuantFormer Backend — Sentiment Endpoint
===========================================================

POST /api/v1/sentiment

Run FinBERT sentiment analysis on financial text.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_sentiment_service
from app.services.sentiment_service import SentimentService
from app.schemas.sentiment import SentimentRequest, SentimentResponse

router = APIRouter()


@router.post(
    "/sentiment",
    response_model=SentimentResponse,
    summary="News Sentiment Analysis",
    description="Analyze financial text sentiment using FinBERT.",
)
async def analyze_sentiment(
    request: SentimentRequest,
    service: SentimentService = Depends(get_sentiment_service),
) -> SentimentResponse:
    """Analyze sentiment of financial text."""

    try:
        result = service.analyze(request.text)

        return SentimentResponse(
            success=result["success"],
            text=result["text"],
            sentiment=result["sentiment"],
            confidence=result["confidence"],
            scores=result["scores"],
            explanation=result["explanation"],
            model_name=result["model_name"],
            latency_ms=result["latency_ms"],
            timestamp=result["timestamp"],
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
                "error": "Sentiment Analysis Failed",
                "message": f"An error occurred: {str(e)}",
            },
        )

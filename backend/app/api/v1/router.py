"""
===========================================================
QuantFormer Backend — API v1 Router
===========================================================

Aggregates all v1 endpoint routers into a single router
mounted at /api/v1.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from fastapi import APIRouter

from backend.app.api.v1.endpoints import (
    health,
    models,
    market,
    news,
    predict,
    sentiment,
    insight,
    explain,
    dashboard,
)

api_v1_router = APIRouter(prefix="/api/v1", tags=["v1"])

# Health & System
api_v1_router.include_router(health.router, tags=["Health"])
api_v1_router.include_router(models.router, tags=["Models"])

# Data
api_v1_router.include_router(market.router, tags=["Market"])
api_v1_router.include_router(news.router, tags=["News"])

# AI Inference
api_v1_router.include_router(predict.router, tags=["Prediction"])
api_v1_router.include_router(sentiment.router, tags=["Sentiment"])
api_v1_router.include_router(insight.router, tags=["Insight"])
api_v1_router.include_router(explain.router, tags=["Explainability"])

# Dashboard
api_v1_router.include_router(dashboard.router, tags=["Dashboard"])

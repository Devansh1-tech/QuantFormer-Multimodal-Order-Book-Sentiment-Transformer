"""
===========================================================
QuantFormer Backend — Main Application
===========================================================

FastAPI application entry point with lifespan management,
CORS configuration, and root endpoint.

Run with:
  uvicorn backend.app.main:app --reload

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import get_settings
from backend.app.core.logging import setup_logging
from backend.app.api.deps import (
    initialize_dependencies,
    get_model_manager,
    get_streaming_service,
)
from backend.app.api.v1.router import api_v1_router
from backend.app.utils.helpers import mark_startup, utc_now_iso

logger = logging.getLogger(__name__)


# ===========================================================
# Lifespan Manager
# ===========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.

    Startup:
      1. Configure structured logging
      2. Initialize dependencies (singletons)
      3. Load all AI models
      4. Start Kafka streaming (if enabled)

    Shutdown:
      1. Stop Kafka streaming
      2. Log shutdown
    """
    settings = get_settings()

    # ---- STARTUP ----
    setup_logging()
    mark_startup()

    logger.info("=" * 60)
    logger.info(f"  {settings.app_name} v{settings.app_version}")
    logger.info(f"  Environment: {settings.app_env}")
    logger.info("=" * 60)

    # Initialize singletons
    initialize_dependencies(settings)

    # Load AI models
    manager = get_model_manager()
    await manager.load_all_models(settings)

    # Start Kafka (if enabled)
    streaming = get_streaming_service()
    await streaming.start()

    logger.info("=" * 60)
    logger.info("  QuantFormer Backend is READY")
    logger.info(f"  Docs: http://{settings.host}:{settings.port}/docs")
    logger.info("=" * 60)

    yield  # Application runs here

    # ---- SHUTDOWN ----
    logger.info("Shutting down QuantFormer Backend...")
    await streaming.stop()
    logger.info("QuantFormer Backend stopped.")


# ===========================================================
# FastAPI Application
# ===========================================================

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description=(
        "QuantFormer — Multimodal Order Book & Sentiment Transformer. "
        "An AI-powered financial analysis platform combining "
        "Deep Learning (TFT), NLP (FinBERT), and Multimodal Fusion "
        "for market prediction and news sentiment analysis."
    ),
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# ===========================================================
# CORS Middleware
# ===========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===========================================================
# Root Endpoint
# ===========================================================

@app.get(
    "/",
    summary="QuantFormer API Information",
    description="Returns project information and available endpoints.",
)
async def root():
    """QuantFormer API root endpoint."""
    return {
        "project": settings.app_name,
        "description": (
            "Multimodal Order Book & Sentiment Transformer — "
            "AI-powered financial analysis platform"
        ),
        "version": settings.app_version,
        "status": "running",
        "documentation": "/docs",
        "endpoints": {
            "health": "GET /api/v1/health",
            "models": "GET /api/v1/models",
            "market": "GET /api/v1/market?symbol=AAPL",
            "news": "GET /api/v1/news",
            "predict": "POST /api/v1/predict",
            "sentiment": "POST /api/v1/sentiment",
            "insight": "POST /api/v1/insight",
            "explain": "POST /api/v1/explain",
            "dashboard": "GET /api/v1/dashboard?symbol=AAPL",
        },
    }


# ===========================================================
# Include API Routers
# ===========================================================

app.include_router(api_v1_router)

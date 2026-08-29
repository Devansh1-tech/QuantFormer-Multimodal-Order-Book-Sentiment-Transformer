"""
===========================================================
QuantFormer Backend — Dashboard Endpoint
===========================================================

GET /api/v1/dashboard?symbol=AAPL

Aggregated endpoint returning all dashboard components
in a single JSON response for the React frontend.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from fastapi import APIRouter, Depends, Query

from backend.app.api.deps import get_dashboard_service, get_settings
from backend.app.core.config import Settings
from backend.app.services.dashboard_service import DashboardService

router = APIRouter()


@router.get(
    "/dashboard",
    summary="Dashboard Aggregator",
    description=(
        "Primary endpoint for the React dashboard. "
        "Aggregates live market data, news, TFT prediction, "
        "FinBERT sentiment, Fusion AI insight, and system status "
        "into a single response."
    ),
)
async def get_dashboard(
    symbol: str = Query(
        default=None,
        description="Stock ticker symbol (e.g. AAPL, RELIANCE.NS)",
    ),
    service: DashboardService = Depends(get_dashboard_service),
    settings: Settings = Depends(get_settings),
):
    """Aggregate all dashboard data for the frontend."""

    if not symbol:
        symbol = settings.default_symbol

    result = await service.aggregate(symbol)
    return result

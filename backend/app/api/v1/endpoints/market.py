"""
===========================================================
QuantFormer Backend — Market Endpoint
===========================================================

GET /api/v1/market?symbol=AAPL

Returns live stock data from Yahoo Finance.
Supports dynamic stock symbols (Change 5).
Returns HTTP 503 if data is unavailable (Change 1).

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from fastapi import APIRouter, Depends, Query, HTTPException

from backend.app.api.deps import get_market_service, get_settings
from backend.app.core.config import Settings
from backend.app.services.market_service import MarketService
from backend.app.loaders.market_loader import MarketDataUnavailable
from backend.app.schemas.market import MarketResponse, MarketQuote

router = APIRouter()


@router.get(
    "/market",
    response_model=MarketResponse,
    summary="Live Market Data",
    description="Fetch live stock data from Yahoo Finance for any symbol.",
)
async def get_market_data(
    symbol: str = Query(
        default=None,
        description="Stock ticker symbol (e.g. AAPL, MSFT, RELIANCE.NS)",
    ),
    service: MarketService = Depends(get_market_service),
    settings: Settings = Depends(get_settings),
) -> MarketResponse:
    """Fetch live market data for the given stock symbol."""

    # Use default symbol if none provided
    if not symbol:
        symbol = settings.default_symbol

    try:
        result = await service.get_market_data(symbol)

        return MarketResponse(
            success=True,
            symbol=result["symbol"],
            data=MarketQuote(**result["data"]),
            source=result["source"],
            cached=result["cached"],
            timestamp=result["timestamp"],
        )

    except MarketDataUnavailable as e:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "Service Unavailable",
                "message": str(e),
                "symbol": symbol.upper(),
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal Server Error",
                "message": f"Failed to fetch market data: {str(e)}",
                "symbol": symbol.upper(),
            },
        )

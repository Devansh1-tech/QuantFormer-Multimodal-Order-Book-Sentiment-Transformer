"""
===========================================================
QuantFormer Backend — Market Data Tests
===========================================================

Tests for:
  - GET /api/v1/market (Default symbol)
  - GET /api/v1/market?symbol=MSFT (Dynamic symbols)
  - HTTP 503 when market data unavailable and cache empty

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from unittest.mock import AsyncMock, patch
from app.loaders.market_loader import MarketDataUnavailable


def test_get_market_data_success(test_client):
    """Test successful retrieval of live stock quote with dynamic symbol."""
    mock_market_data = {
        "symbol": "AAPL",
        "company_name": "Apple Inc.",
        "price": 185.50,
        "open": 184.20,
        "high": 186.00,
        "low": 183.90,
        "close": 184.00,
        "volume": 45000000,
        "daily_change": 1.50,
        "daily_change_percent": 0.8152,
        "market_cap": 2850000000000,
        "currency": "USD",
        "exchange": "NMS",
        "timestamp": "2026-08-29T12:00:00Z",
        "cached": False,
    }

    with patch("app.loaders.market_loader.MarketLoader.fetch", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = mock_market_data

        response = test_client.get("/api/v1/market?symbol=AAPL")
        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert data["symbol"] == "AAPL"
        assert data["data"]["price"] == 185.50
        assert data["data"]["daily_change"] == 1.50
        assert data["data"]["volume"] == 45000000
        assert data["source"] == "yahoo_finance"


def test_get_market_data_indian_stock(test_client):
    """Test dynamic stock symbol for NSE ticker (e.g. RELIANCE.NS)."""
    mock_market_data = {
        "symbol": "RELIANCE.NS",
        "company_name": "Reliance Industries Limited",
        "price": 2950.00,
        "open": 2930.00,
        "high": 2965.00,
        "low": 2920.00,
        "close": 2925.00,
        "volume": 8500000,
        "daily_change": 25.00,
        "daily_change_percent": 0.8547,
        "market_cap": 20000000000000,
        "currency": "INR",
        "exchange": "NSE",
        "timestamp": "2026-08-29T12:00:00Z",
        "cached": False,
    }

    with patch("app.loaders.market_loader.MarketLoader.fetch", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = mock_market_data

        response = test_client.get("/api/v1/market?symbol=RELIANCE.NS")
        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "RELIANCE.NS"
        assert data["data"]["currency"] == "INR"


def test_market_data_unavailable_returns_503(test_client):
    """Test that failure to fetch market data when cache is empty returns HTTP 503."""
    with patch("app.loaders.market_loader.MarketLoader.fetch", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.side_effect = MarketDataUnavailable("Market data unavailable. Yahoo Finance is unreachable.")

        response = test_client.get("/api/v1/market?symbol=INVALID_TICKER")
        assert response.status_code == 503
        data = response.json()
        assert "detail" in data
        assert data["detail"]["error"] == "Service Unavailable"

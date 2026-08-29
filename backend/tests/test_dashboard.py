"""
===========================================================
QuantFormer Backend — Dashboard Aggregator Tests
===========================================================

Tests for GET /api/v1/dashboard?symbol=.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from unittest.mock import AsyncMock, patch


def test_dashboard_aggregation_success(test_client):
    """Test dashboard aggregation combining market, news, sentiment, insight, and status."""
    mock_market = {
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
        "currency": "USD",
        "cached": False,
    }

    mock_news = {
        "articles": [
            {
                "headline": "Apple Unveils New AI Features in Latest Release",
                "source": "TechCrunch",
                "published_at": "2026-08-29T10:00:00Z",
                "url": "https://example.com/apple-ai",
                "description": "Apple announced new generative AI features.",
            }
        ],
        "total_articles": 1,
        "source": "live_api",
        "cached": False,
        "message": None,
    }

    with patch("backend.app.loaders.market_loader.MarketLoader.fetch", new_callable=AsyncMock) as mock_market_fetch, \
         patch("backend.app.loaders.news_loader.NewsLoader.fetch", new_callable=AsyncMock) as mock_news_fetch:

        mock_market_fetch.return_value = mock_market
        mock_news_fetch.return_value = mock_news

        response = test_client.get("/api/v1/dashboard?symbol=AAPL")
        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert data["symbol"] == "AAPL"
        assert "market" in data
        assert data["market"]["price"] == 185.50
        assert "news" in data
        assert data["news"]["total_articles"] == 1
        assert "sentiment" in data
        assert "insight" in data
        assert "system" in data
        assert data["system"]["status"] in ("healthy", "degraded")
        assert "response_time_ms" in data

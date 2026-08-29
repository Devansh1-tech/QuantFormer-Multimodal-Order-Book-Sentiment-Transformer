"""
===========================================================
QuantFormer Backend — News Endpoint Tests
===========================================================

Tests for:
  - GET /api/v1/news (Live news items)
  - GET /api/v1/news (Fallback message when unavailable)

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from unittest.mock import AsyncMock, patch


def test_get_news_success(test_client):
    """Test retrieving news articles successfully."""
    mock_news = {
        "articles": [
            {
                "headline": "Fed Signals Potential Rate Cut Amid Cooling Inflation",
                "source": "Bloomberg",
                "published_at": "2026-08-29T10:00:00Z",
                "url": "https://example.com/news/1",
                "description": "Federal Reserve officials indicated openness to interest rate cuts.",
            }
        ],
        "total_articles": 1,
        "source": "live_api",
        "cached": False,
        "message": None,
    }

    with patch("backend.app.loaders.news_loader.NewsLoader.fetch", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = mock_news

        response = test_client.get("/api/v1/news?limit=5")
        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert data["total_articles"] == 1
        assert len(data["articles"]) == 1
        assert data["articles"][0]["headline"] == "Fed Signals Potential Rate Cut Amid Cooling Inflation"
        assert data["articles"][0]["source"] == "Bloomberg"


def test_news_unavailable_returns_empty_with_message(test_client):
    """Test that when news provider is down and cache is empty, returns clean message."""
    mock_empty_news = {
        "articles": [],
        "total_articles": 0,
        "source": "unavailable",
        "cached": False,
        "message": "No recent financial news available.",
    }

    with patch("backend.app.loaders.news_loader.NewsLoader.fetch", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = mock_empty_news

        response = test_client.get("/api/v1/news")
        assert response.status_code == 200
        data = response.json()

        assert data["total_articles"] == 0
        assert data["articles"] == []
        assert data["message"] == "No recent financial news available."

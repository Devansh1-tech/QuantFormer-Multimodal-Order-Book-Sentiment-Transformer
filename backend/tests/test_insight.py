"""
===========================================================
QuantFormer Backend — Multimodal Insight Tests
===========================================================

Tests for POST /api/v1/insight.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

def test_generate_multimodal_insight(test_client, sample_news_text):
    """Test multimodal insight synthesis with compliance disclaimer."""
    payload = {
        "market_prediction": "Bullish",
        "news_text": sample_news_text,
        "market_confidence": 91.3
    }

    response = test_client.post("/api/v1/insight", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["success"] is True
    assert data["market_trend"] == "Bullish"
    assert data["market_confidence"] == 91.3
    assert data["news_sentiment"] == "positive"
    assert "overall_insight" in data
    assert data["overall_insight"] == "Strong Bullish"
    assert "disclaimer" in data
    assert "financial advice" in data["disclaimer"].lower()
    assert "latency_ms" in data

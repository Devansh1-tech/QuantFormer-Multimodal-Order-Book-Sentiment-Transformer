"""
===========================================================
QuantFormer Backend — Explainability Endpoint Tests
===========================================================

Tests for POST /api/v1/explain.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

def test_explain_prediction(test_client, sample_news_text):
    """Test explainability endpoint generating structured reasoning statements."""
    payload = {
        "market_prediction": "Bullish",
        "confidence": 91.3,
        "news_text": sample_news_text
    }

    response = test_client.post("/api/v1/explain", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["success"] is True
    assert data["market_prediction"] == "Bullish"
    assert data["confidence"] == 91.3
    assert data["news_sentiment"] == "positive"
    assert data["overall_insight"] == "Strong Bullish"
    assert "explanation" in data
    assert isinstance(data["explanation"], list)
    assert len(data["explanation"]) >= 3
    assert "disclaimer" in data

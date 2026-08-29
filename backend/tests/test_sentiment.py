"""
===========================================================
QuantFormer Backend — FinBERT Sentiment Tests
===========================================================

Tests for POST /api/v1/sentiment.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

def test_sentiment_analysis_success(test_client, sample_news_text):
    """Test FinBERT sentiment analysis on news headline."""
    payload = {
        "text": sample_news_text
    }

    response = test_client.post("/api/v1/sentiment", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["success"] is True
    assert data["sentiment"] in ("positive", "negative", "neutral")
    assert 0 <= data["confidence"] <= 100
    assert "scores" in data
    assert "positive" in data["scores"]
    assert "negative" in data["scores"]
    assert "neutral" in data["scores"]
    assert "explanation" in data
    assert len(data["explanation"]) > 10
    assert data["model_name"] == "FinBERT"
    assert "latency_ms" in data

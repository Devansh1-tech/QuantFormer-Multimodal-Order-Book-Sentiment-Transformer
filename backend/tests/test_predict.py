"""
===========================================================
QuantFormer Backend — TFT Prediction Tests
===========================================================

Tests for POST /api/v1/predict.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

def test_predict_success(test_client, sample_features):
    """Test TFT prediction with valid (100, 143) market feature matrix."""
    payload = {
        "features": sample_features,
        "symbol": "AAPL"
    }

    response = test_client.post("/api/v1/predict", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["success"] is True
    assert data["prediction"] in ("Down", "Stable", "Up")
    assert data["market_trend"] in ("Bearish", "Neutral", "Bullish")
    assert 0 <= data["confidence"] <= 100
    assert "probabilities" in data
    assert "Down" in data["probabilities"]
    assert "Stable" in data["probabilities"]
    assert "Up" in data["probabilities"]
    assert "latency_ms" in data
    assert data["model_name"] == "Temporal Fusion Transformer"
    assert data["symbol"] == "AAPL"

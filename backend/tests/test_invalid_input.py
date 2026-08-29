"""
===========================================================
QuantFormer Backend — Invalid Input Tests
===========================================================

Tests for:
  - Wrong feature sequence length (not 100)
  - Wrong feature count (not 143)
  - Empty text for sentiment
  - Invalid JSON payloads

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

def test_predict_invalid_sequence_length(test_client):
    """Test POST /api/v1/predict with wrong sequence length (e.g. 50 instead of 100)."""
    # 50 rows of 143 features
    bad_features = [[0.0] * 143 for _ in range(50)]

    response = test_client.post("/api/v1/predict", json={"features": bad_features})
    assert response.status_code == 422
    data = response.json()
    assert "Expected sequence length 100" in str(data)


def test_predict_invalid_feature_count(test_client):
    """Test POST /api/v1/predict with wrong feature count (e.g. 50 instead of 143)."""
    # 100 rows of 50 features
    bad_features = [[0.0] * 50 for _ in range(100)]

    response = test_client.post("/api/v1/predict", json={"features": bad_features})
    assert response.status_code == 422
    data = response.json()
    assert "Expected 143 features" in str(data)


def test_sentiment_empty_text(test_client):
    """Test POST /api/v1/sentiment with empty text string."""
    response = test_client.post("/api/v1/sentiment", json={"text": ""})
    assert response.status_code == 422


def test_insight_missing_field(test_client):
    """Test POST /api/v1/insight with missing required fields."""
    response = test_client.post("/api/v1/insight", json={"market_prediction": "Bullish"})
    assert response.status_code == 422

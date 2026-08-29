"""
===========================================================
QuantFormer Backend — Models Registry Tests
===========================================================

Tests for GET /api/v1/models.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

def test_get_models_registry(test_client):
    """Test GET /api/v1/models returns details of registered models."""
    response = test_client.get("/api/v1/models")
    assert response.status_code == 200
    data = response.json()

    assert data["total_models"] == 3
    assert data["loaded_models"] >= 1
    assert "models" in data

    models_by_key = {m["key"]: m for m in data["models"]}
    assert "tft" in models_by_key
    assert "finbert" in models_by_key
    assert "fusion" in models_by_key

    # TFT details
    tft = models_by_key["tft"]
    assert tft["name"] == "Temporal Fusion Transformer"
    assert tft["role"] == "Primary Production Prediction Model"
    assert tft["accuracy"] == 84.51

    # FinBERT details
    finbert = models_by_key["finbert"]
    assert finbert["embedding_dim"] == 768

    # Fusion details
    fusion = models_by_key["fusion"]
    assert "Fusion" in fusion["name"]

"""
===========================================================
QuantFormer Backend — Missing Models Tests
===========================================================

Tests verifying HTTP 503 and degraded status when models
fail to load or are unavailable.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.api import deps


def test_predict_model_not_loaded_returns_503(sample_features):
    """Test that POST /api/v1/predict returns HTTP 503 when TFT is not loaded."""
    unhealthy_manager = MagicMock()
    unhealthy_manager.is_healthy = False
    unhealthy_manager.tft_loaded = False
    unhealthy_manager.predict_tft.side_effect = RuntimeError("TFT model is not loaded")

    app.dependency_overrides[deps.get_model_manager] = lambda: unhealthy_manager

    try:
        client = TestClient(app, raise_server_exceptions=False)
        response = client.post("/api/v1/predict", json={"features": sample_features})
        assert response.status_code == 503
        data = response.json()
        assert data["detail"]["error"] == "Model Unavailable"
    finally:
        app.dependency_overrides.clear()


def test_sentiment_model_not_loaded_returns_503(sample_news_text):
    """Test that POST /api/v1/sentiment returns HTTP 503 when FinBERT is not loaded."""
    unhealthy_manager = MagicMock()
    unhealthy_manager.is_healthy = False
    unhealthy_manager.finbert_loaded = False
    unhealthy_manager.analyze_sentiment.side_effect = RuntimeError("FinBERT model is not loaded")

    app.dependency_overrides[deps.get_model_manager] = lambda: unhealthy_manager

    try:
        client = TestClient(app, raise_server_exceptions=False)
        response = client.post("/api/v1/sentiment", json={"text": sample_news_text})
        assert response.status_code == 503
        data = response.json()
        assert data["detail"]["error"] == "Model Unavailable"
    finally:
        app.dependency_overrides.clear()

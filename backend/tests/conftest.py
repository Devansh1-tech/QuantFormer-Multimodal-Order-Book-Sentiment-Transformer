"""
===========================================================
QuantFormer Backend — Test Fixtures
===========================================================

Shared pytest fixtures for the test suite.
Uses FastAPI TestClient with mocked model loading for
unit tests that don't require real GPU inference.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

import sys
import os
import pytest
from unittest.mock import patch, MagicMock, AsyncMock

# Ensure project root is on sys.path
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
def mock_model_manager():
    """Create a mock ModelManager that doesn't load real models."""
    manager = MagicMock()
    manager.is_healthy = True
    manager.all_loaded = True
    manager.loaded_count = 3
    manager.tft_loaded = True
    manager.finbert_loaded = True
    manager.fusion_loaded = True
    manager.device = MagicMock()
    manager.device.type = "cpu"
    manager.device.__str__ = lambda self: "cpu"

    manager.get_health_status.return_value = {
        "tft": {
            "name": "Temporal Fusion Transformer",
            "loaded": True,
            "checkpoint_exists": True,
            "checkpoint_path": "checkpoints/best_tft_model.pth",
            "device": "cpu",
            "version": "1.0.0",
        },
        "finbert": {
            "name": "FinBERT",
            "loaded": True,
            "checkpoint_exists": True,
            "checkpoint_path": "saved_models/best_finbert_model.pth",
            "device": "cpu",
            "version": "1.0.0",
        },
        "fusion": {
            "name": "QuantFormer Fusion",
            "loaded": True,
            "checkpoint_exists": True,
            "checkpoint_path": "checkpoints/best_fusion_model.pth",
            "device": "cpu",
            "version": "1.0.0",
        },
    }

    manager.predict_tft.return_value = {
        "prediction": "Up",
        "trend": "Bullish",
        "confidence": 91.3,
        "probabilities": {"Down": 3.2, "Stable": 5.5, "Up": 91.3},
        "class_index": 2,
        "pooled_features": MagicMock(),
    }

    manager.analyze_sentiment.return_value = {
        "sentiment": "positive",
        "confidence": 87.5,
        "scores": {"positive": 87.5, "negative": 5.2, "neutral": 7.3},
        "class_index": 0,
        "embedding": MagicMock(),
    }

    return manager


@pytest.fixture
def mock_streaming_service():
    """Create a mock StreamingService."""
    service = MagicMock()
    service.is_enabled = False
    service.is_connected = False
    service.get_status.return_value = {
        "enabled": False,
        "connected": False,
        "topics": [],
    }
    return service


@pytest.fixture
def test_client(mock_model_manager, mock_streaming_service):
    """
    Create a FastAPI TestClient with mocked dependencies.

    This avoids loading real models during testing.
    """
    from fastapi.testclient import TestClient
    from app.main import app
    from app.api import deps

    # Override dependencies with mocks
    app.dependency_overrides[deps.get_model_manager] = lambda: mock_model_manager
    app.dependency_overrides[deps.get_streaming_service] = lambda: mock_streaming_service

    client = TestClient(app, raise_server_exceptions=False)
    yield client

    # Cleanup
    app.dependency_overrides.clear()


@pytest.fixture
def sample_features():
    """Generate sample (100, 143) feature matrix for testing."""
    import numpy as np
    np.random.seed(42)
    return np.random.randn(100, 143).tolist()


@pytest.fixture
def sample_news_text():
    """Sample financial news text for testing."""
    return "Apple Inc. reported record quarterly revenue of $123.9 billion, beating analyst expectations."

"""
===========================================================
QuantFormer Backend — Health Endpoint Tests
===========================================================

Tests for:
  - GET / (Root Information)
  - GET /api/v1/health (System telemetry, models, hardware, Kafka, uptime)

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

def test_root_endpoint(test_client):
    """Test root GET / returns project metadata and endpoint map."""
    response = test_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["project"] == "QuantFormer"
    assert data["status"] == "running"
    assert "endpoints" in data
    assert data["endpoints"]["health"] == "GET /api/v1/health"
    assert data["endpoints"]["predict"] == "POST /api/v1/predict"
    assert data["endpoints"]["dashboard"] == "GET /api/v1/dashboard?symbol=AAPL"


def test_health_endpoint(test_client):
    """Test GET /api/v1/health returns full system and model telemetry."""
    response = test_client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()

    assert data["status"] in ("healthy", "degraded", "unhealthy")
    assert data["app_name"] == "QuantFormer"
    assert "uptime" in data
    assert "uptime_seconds" in data

    # Model telemetry
    assert "models" in data
    assert len(data["models"]) >= 1
    model_names = [m["name"] for m in data["models"]]
    assert "Temporal Fusion Transformer" in model_names

    # Hardware & System telemetry
    assert "gpu" in data
    assert "system" in data
    assert "cpu_usage_percent" in data["system"]
    assert "ram_usage_percent" in data["system"]

    # Kafka telemetry
    assert "kafka" in data
    assert "enabled" in data["kafka"]

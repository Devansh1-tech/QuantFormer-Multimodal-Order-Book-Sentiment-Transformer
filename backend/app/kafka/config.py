"""
===========================================================
QuantFormer Backend — Kafka Configuration
===========================================================

Kafka topic definitions and cluster settings.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from app.core.config import get_settings


def get_kafka_config() -> dict:
    """Return Kafka configuration dictionary."""
    settings = get_settings()
    return {
        "enabled": settings.kafka_enabled,
        "bootstrap_servers": settings.kafka_bootstrap_servers,
        "topics": {
            "market": settings.kafka_market_topic,
            "news": settings.kafka_news_topic,
            "prediction": settings.kafka_prediction_topic,
        },
    }

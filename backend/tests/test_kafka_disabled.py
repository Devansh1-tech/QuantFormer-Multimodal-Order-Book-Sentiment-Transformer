"""
===========================================================
QuantFormer Backend — Kafka Disabled Mode Tests
===========================================================

Tests verifying backend robustness when Kafka is disabled.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from app.core.config import Settings
from app.kafka.streaming_service import StreamingService
from app.kafka.producer import KafkaProducer
from app.kafka.consumer import KafkaConsumer


def test_kafka_disabled_producer_safe_noop():
    """Test that KafkaProducer does not error when disabled."""
    producer = KafkaProducer(enabled=False)
    assert producer.is_connected is False

    # Sending should safely return False without error
    success = producer.send("market-data", {"test": "data"})
    assert success is False
    producer.close()


def test_kafka_disabled_consumer_safe_noop():
    """Test that KafkaConsumer does not error when disabled."""
    consumer = KafkaConsumer(enabled=False)
    assert consumer.is_running is False

    success = consumer.subscribe("market-data", lambda m: None)
    assert success is False
    consumer.stop()


def test_streaming_service_disabled():
    """Test StreamingService status when Kafka is disabled."""
    settings = Settings(KAFKA_ENABLED=False)
    streaming = StreamingService(settings)

    assert streaming.is_enabled is False
    assert streaming.is_connected is False

    status = streaming.get_status()
    assert status["enabled"] is False
    assert status["connected"] is False
    assert status["topics"] == []

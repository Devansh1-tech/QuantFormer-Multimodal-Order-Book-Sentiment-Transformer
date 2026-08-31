"""
===========================================================
QuantFormer Backend — Kafka Streaming Service
===========================================================

High-level orchestrator that manages Kafka producer and
consumer lifecycle. Provides a unified interface for the
rest of the backend.

If Kafka is disabled (KAFKA_ENABLED=false), the service
gracefully operates as a no-op.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

import logging
from typing import Any, Dict, List

from app.core.config import Settings
from app.kafka.producer import KafkaProducer
from app.kafka.consumer import KafkaConsumer

logger = logging.getLogger(__name__)


class StreamingService:
    """
    High-level Kafka streaming orchestrator.

    Manages the lifecycle of producers and consumers and
    provides health status for the /api/v1/health endpoint.
    """

    def __init__(self, settings: Settings):
        self._enabled = settings.kafka_enabled
        self._topics = [
            settings.kafka_market_topic,
            settings.kafka_news_topic,
            settings.kafka_prediction_topic,
        ]

        self._producer = KafkaProducer(
            bootstrap_servers=settings.kafka_bootstrap_servers,
            enabled=self._enabled,
        )
        self._consumer = KafkaConsumer(
            bootstrap_servers=settings.kafka_bootstrap_servers,
            enabled=self._enabled,
        )

    async def start(self) -> None:
        """Start Kafka streaming services."""
        if not self._enabled:
            logger.info("Kafka is disabled. Streaming service not started.")
            return

        logger.info("Starting Kafka streaming services...")
        # Consumers can be subscribed to topics here
        # For now, the subscriptions are done on-demand

    async def stop(self) -> None:
        """Stop all Kafka streaming services."""
        if not self._enabled:
            return

        logger.info("Stopping Kafka streaming services...")
        self._consumer.stop()
        self._producer.close()

    def publish(self, topic: str, message: Dict[str, Any]) -> bool:
        """Publish a message to a Kafka topic."""
        return self._producer.send(topic, message)

    def get_status(self) -> Dict[str, Any]:
        """Return Kafka health status for the health endpoint."""
        return {
            "enabled": self._enabled,
            "connected": self._producer.is_connected if self._enabled else False,
            "topics": self._topics if self._enabled else [],
        }

    @property
    def is_enabled(self) -> bool:
        return self._enabled

    @property
    def is_connected(self) -> bool:
        return self._producer.is_connected if self._enabled else False

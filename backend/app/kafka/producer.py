"""
===========================================================
QuantFormer Backend — Kafka Producer
===========================================================

Resilient Kafka producer with graceful degradation.
If Kafka is disabled or unreachable, operations are no-ops.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

import json
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class KafkaProducer:
    """
    Resilient Kafka producer wrapper.

    If Kafka is disabled or the broker is unreachable,
    all send operations gracefully degrade to no-ops.
    """

    def __init__(
        self,
        bootstrap_servers: str = "localhost:9092",
        enabled: bool = False,
    ):
        self._enabled = enabled
        self._bootstrap_servers = bootstrap_servers
        self._producer = None
        self._connected = False

        if self._enabled:
            self._connect()

    def _connect(self) -> None:
        """Attempt to connect to Kafka broker."""
        try:
            from kafka import KafkaProducer as _KafkaProducer

            self._producer = _KafkaProducer(
                bootstrap_servers=self._bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                request_timeout_ms=5000,
                max_block_ms=5000,
            )
            self._connected = True
            logger.info(
                f"Kafka Producer connected to {self._bootstrap_servers}"
            )
        except Exception as e:
            self._connected = False
            logger.warning(
                f"Kafka Producer connection failed: {e}. "
                f"Operating in local mode."
            )

    def send(self, topic: str, message: Dict[str, Any]) -> bool:
        """
        Send a message to a Kafka topic.

        Returns True if sent successfully, False otherwise.
        """
        if not self._enabled or not self._connected:
            return False

        try:
            self._producer.send(topic, value=message)
            self._producer.flush(timeout=5)
            logger.debug(f"Kafka message sent to topic: {topic}")
            return True
        except Exception as e:
            logger.warning(f"Kafka send failed for topic {topic}: {e}")
            return False

    @property
    def is_connected(self) -> bool:
        return self._connected

    def close(self) -> None:
        """Close the Kafka producer connection."""
        if self._producer:
            try:
                self._producer.close(timeout=5)
                logger.info("Kafka Producer closed")
            except Exception as e:
                logger.warning(f"Error closing Kafka Producer: {e}")

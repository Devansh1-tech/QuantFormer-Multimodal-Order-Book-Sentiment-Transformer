"""
===========================================================
QuantFormer Backend — Kafka Consumer
===========================================================

Background Kafka consumer for streaming topics.
Runs in a separate thread and processes messages via
registered callbacks.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

import json
import logging
import threading
from typing import Callable, Dict, Optional

logger = logging.getLogger(__name__)


class KafkaConsumer:
    """
    Background Kafka consumer wrapper.

    If Kafka is disabled or unreachable, the consumer
    gracefully does nothing.
    """

    def __init__(
        self,
        bootstrap_servers: str = "localhost:9092",
        enabled: bool = False,
    ):
        self._enabled = enabled
        self._bootstrap_servers = bootstrap_servers
        self._consumers: Dict[str, threading.Thread] = {}
        self._running = False

    def subscribe(
        self,
        topic: str,
        callback: Callable[[dict], None],
        group_id: str = "quantformer-backend",
    ) -> bool:
        """
        Subscribe to a Kafka topic with a message callback.

        The consumer runs in a background daemon thread.

        Parameters
        ----------
        topic : str — Kafka topic name
        callback : callable — Function to process each message
        group_id : str — Consumer group ID

        Returns True if subscription started successfully.
        """
        if not self._enabled:
            logger.info(f"Kafka disabled — skipping subscription to {topic}")
            return False

        try:
            from kafka import KafkaConsumer as _KafkaConsumer

            def _consume():
                try:
                    consumer = _KafkaConsumer(
                        topic,
                        bootstrap_servers=self._bootstrap_servers,
                        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                        group_id=group_id,
                        auto_offset_reset="latest",
                        consumer_timeout_ms=1000,
                    )

                    logger.info(f"Kafka Consumer started for topic: {topic}")

                    while self._running:
                        messages = consumer.poll(timeout_ms=1000)
                        for tp, records in messages.items():
                            for record in records:
                                try:
                                    callback(record.value)
                                except Exception as e:
                                    logger.error(
                                        f"Error processing message from {topic}: {e}"
                                    )

                    consumer.close()
                    logger.info(f"Kafka Consumer stopped for topic: {topic}")

                except Exception as e:
                    logger.warning(
                        f"Kafka Consumer failed for topic {topic}: {e}"
                    )

            self._running = True
            thread = threading.Thread(
                target=_consume,
                name=f"kafka-consumer-{topic}",
                daemon=True,
            )
            thread.start()
            self._consumers[topic] = thread

            return True

        except Exception as e:
            logger.warning(f"Failed to subscribe to {topic}: {e}")
            return False

    def stop(self) -> None:
        """Stop all consumer threads."""
        self._running = False
        for topic, thread in self._consumers.items():
            thread.join(timeout=5)
            logger.info(f"Kafka Consumer thread stopped for: {topic}")
        self._consumers.clear()

    @property
    def is_running(self) -> bool:
        return self._running

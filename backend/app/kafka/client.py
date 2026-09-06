import logging
import json
from kafka import KafkaProducer, KafkaConsumer
import kafka.errors

from backend.app.core.config import settings

logger = logging.getLogger("backend")

class KafkaClientWrapper:
    """
    Wraps Kafka Python to provide resilient direct API fallback if broker is offline.
    """
    def __init__(self):
        self.is_connected = False
        self.producer = None
        
        if settings.KAFKA_FALLBACK_MODE:
            try:
                import socket
                host, port_str = settings.KAFKA_BOOTSTRAP_SERVERS.split(":")
                with socket.create_connection((host, int(port_str)), timeout=0.5):
                    pass
                self.producer = KafkaProducer(
                    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                    value_serializer=lambda v: json.dumps(v).encode('utf-8')
                )
                self.is_connected = True
                logger.info("Connected to Kafka Broker successfully.")
            except Exception:
                logger.info("Kafka Broker not running locally. Running in Direct API Mode.")
                self.is_connected = False

                
    def send_message(self, topic: str, message: dict):
        if self.is_connected and self.producer:
            try:
                self.producer.send(topic, message)
                self.producer.flush()
            except Exception as e:
                logger.error(f"Failed to send Kafka message to topic {topic}: {e}")
        else:
            # Fallback direct mode -> No-op for producer as endpoints directly call services
            pass

kafka_client = KafkaClientWrapper()

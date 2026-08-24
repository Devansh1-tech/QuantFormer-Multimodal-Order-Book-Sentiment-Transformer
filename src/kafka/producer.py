from kafka import KafkaProducer

from src.kafka.config import (
    BOOTSTRAP_SERVERS,
    ACKS,
    RETRIES,
    REQUEST_TIMEOUT_MS
)

from src.kafka.serializer import serialize


class QuantFormerProducer:
    """
    Generic Kafka Producer.
    """

    def __init__(self):

        self.producer = KafkaProducer(

            bootstrap_servers=BOOTSTRAP_SERVERS,

            value_serializer=serialize,

            acks=ACKS,

            retries=RETRIES,

            request_timeout_ms=REQUEST_TIMEOUT_MS
        )

    def send(
        self,
        topic,
        message
    ):
        """
        Publish message.
        """

        future = self.producer.send(
            topic,
            value=message
        )

        future.get(timeout=10)

    def flush(self):

        self.producer.flush()

    def close(self):

        self.producer.close()
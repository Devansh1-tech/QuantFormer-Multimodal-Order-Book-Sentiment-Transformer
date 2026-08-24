from kafka import KafkaConsumer

from src.kafka.config import (
    BOOTSTRAP_SERVERS,
    CONSUMER_GROUP
)

from src.kafka.serializer import deserialize


class QuantFormerConsumer:
    """
    Generic Kafka Consumer.
    """

    def __init__(self, topic):

        self.consumer = KafkaConsumer(

            topic,

            bootstrap_servers=BOOTSTRAP_SERVERS,

            value_deserializer=deserialize,

            group_id="quantformer-preprocessing-v2",

            auto_offset_reset="latest",

            enable_auto_commit=True
        )

    def listen(self):
        """
        Generator for Kafka messages.
        """

        for message in self.consumer:

            yield message.value

    def close(self):

        self.consumer.close()
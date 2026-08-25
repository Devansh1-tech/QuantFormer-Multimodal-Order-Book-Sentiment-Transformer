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

    def __init__(
        self,
        topic: str,
        group_id: str = CONSUMER_GROUP,
        auto_offset_reset: str = "earliest"
    ):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=BOOTSTRAP_SERVERS,
            value_deserializer=deserialize,
            group_id=group_id,
            auto_offset_reset=auto_offset_reset,
            enable_auto_commit=True
        )

    def listen(self):
        """
        Generator for Kafka messages.
        """
        print(f"[Consumer.listen] Entered listen() method. Starting iteration over KafkaConsumer (bootstrap_servers={BOOTSTRAP_SERVERS})", flush=True)
        for message in self.consumer:
            print(f"[Consumer.listen] Loop entered! KafkaConsumer received message from topic '{message.topic}' | partition={message.partition} | offset={message.offset}", flush=True)
            print(f"[Consumer.listen] type(message.value): {type(message.value)}", flush=True)
            val_str = str(message.value)
            print(f"[Consumer.listen] first 200 characters of message.value: {val_str[:200]}", flush=True)
            print(f"[Consumer.listen] result after deserialization: {type(message.value)} | is_dict={isinstance(message.value, dict)}", flush=True)
            yield message.value

    def close(self):
        """
        Close consumer connection.
        """
        self.consumer.close()
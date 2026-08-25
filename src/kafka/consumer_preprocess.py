"""
===========================================================
Market Data Preprocessing Kafka Consumer
===========================================================

Consumes raw Limit Order Book market data from RAW_MARKET_TOPIC,
validates message structure and sequence shapes, and publishes
preprocessed market records to PROCESSED_MARKET_TOPIC.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from datetime import datetime

from src.kafka.consumer import QuantFormerConsumer
from src.kafka.producer import QuantFormerProducer
from src.kafka.config import (
    RAW_MARKET_TOPIC,
    PROCESSED_MARKET_TOPIC
)


import traceback


# ==========================================================
# Preprocessing Function
# ==========================================================

def preprocess_message(message: dict) -> dict:
    """
    Validate incoming market message structure and append metadata.
    """
    print(f"[preprocess_message] type(message): {type(message)}", flush=True)
    if isinstance(message, dict):
        print(f"[preprocess_message] available keys: {list(message.keys())}", flush=True)
    else:
        print(f"[preprocess_message] available keys: None (message is not a dict: {type(message)})", flush=True)

    required_keys = [
        "message_id",
        "timestamp",
        "sequence_length",
        "feature_count",
        "features"
    ]

    for key in required_keys:
        exists = isinstance(message, dict) and (key in message)
        print(f"[preprocess_message] required key '{key}' exists: {exists}", flush=True)
        if not exists:
            err = ValueError(
                f"Missing required key in market message: '{key}'"
            )
            print(f"[preprocess_message] Validation Error Traceback:\n{traceback.format_exc()}", flush=True)
            raise err

    processed_message = {
        "message_id": message["message_id"],
        "market_timestamp": message["timestamp"],
        "processing_timestamp": datetime.now().isoformat(),
        "sequence_length": message["sequence_length"],
        "feature_count": message["feature_count"],
        "features": message["features"],
        "status": "processed"
    }

    return processed_message


# ==========================================================
# Kafka Processing Loop
# ==========================================================

def start_preprocessing():
    """
    Consume raw market data, preprocess it, and publish to processed topic.
    """
    print("=" * 60, flush=True)
    print("Preprocessing Consumer Started", flush=True)
    print("=" * 60, flush=True)

    consumer = QuantFormerConsumer(RAW_MARKET_TOPIC)
    producer = QuantFormerProducer()

    for message in consumer.listen():
        try:
            processed = preprocess_message(message)

            print(f"[Preprocessing Consumer] Immediately before producer.send('{PROCESSED_MARKET_TOPIC}', message_id={processed['message_id']})", flush=True)
            producer.send(
                PROCESSED_MARKET_TOPIC,
                processed
            )
            print(f"[Preprocessing Consumer] Immediately after producer.send('{PROCESSED_MARKET_TOPIC}', message_id={processed['message_id']})", flush=True)

            print(
                f"Processed Message ID {processed['message_id']} | "
                f"Features: {processed['sequence_length']}x{processed['feature_count']}",
                flush=True
            )

        except Exception as error:
            print(f"Preprocessing Consumer Error: {error}\nFull Traceback:\n{traceback.format_exc()}", flush=True)


if __name__ == "__main__":
    start_preprocessing()
"""
===========================================================
Market Data Kafka Producer
===========================================================

Streams FI-2010 Limit Order Book test sequences to the raw
market topic (RAW_MARKET_TOPIC) simulating a live exchange feed.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

import time
from datetime import datetime
from pathlib import Path
import numpy as np

from src.kafka.producer import QuantFormerProducer
from src.kafka.config import RAW_MARKET_TOPIC


# ==========================================================
# Dataset Path & Loading
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "datasets" / "processed" / "FI2010" / "X_test.npy"

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Processed FI2010 test set not found at:\n{DATA_PATH}"
    )

X_test = np.load(DATA_PATH)

print("=" * 60)
print("FI-2010 Market Dataset Loaded Successfully")
print(f"Total Test Sequences : {len(X_test)}")
print("=" * 60)

# ==========================================================
# Initialize Kafka Producer
# ==========================================================

producer = QuantFormerProducer()


# ==========================================================
# Stream Market Data
# ==========================================================

def stream_market_data(
    delay: float = 0.1,
    max_messages: int = 10
):
    """
    Stream FI-2010 sequences to Kafka RAW_MARKET_TOPIC.
    """
    print("=" * 60)
    print("Starting Live Market Data Stream...")
    print("=" * 60)

    total = min(max_messages, len(X_test))

    for message_id in range(1, total + 1):
        sample = X_test[message_id - 1]

        message = {
            "message_id": message_id,
            "timestamp": datetime.now().isoformat(),
            "sequence_length": int(sample.shape[0]),
            "feature_count": int(sample.shape[1]),
            "features": sample.tolist()
        }

        producer.send(
            RAW_MARKET_TOPIC,
            message
        )

        print(
            f"Sent Market Message #{message_id:03d} | "
            f"Shape: {sample.shape}"
        )

        time.sleep(delay)

    producer.flush()
    print("\nMarket Data Streaming Completed Successfully.")


if __name__ == "__main__":
    stream_market_data()
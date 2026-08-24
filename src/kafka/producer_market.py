import os
import time
import numpy as np
from datetime import datetime

from src.kafka.producer import QuantFormerProducer
from src.kafka.config import RAW_MARKET_TOPIC


# ==========================================================
# Dataset Path
# ==========================================================

from pathlib import Path
import numpy as np

# ==========================================================
# Project Root
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "datasets" / "processed" / "FI2010" / "X_test.npy"

X_test = np.load(DATA_PATH)

print("=" * 60)
print("Dataset Loaded Successfully")
print(f"Samples : {len(X_test)}")
print("=" * 60)

# ==========================================================
# Load Dataset
# ==========================================================

X_test = np.load(DATA_PATH)

print("=" * 60)
print("Dataset Loaded Successfully")
print(f"Samples : {len(X_test)}")
print("=" * 60)

# ==========================================================
# Initialize Kafka Producer
# ==========================================================

producer = QuantFormerProducer()

print("Kafka Producer Initialized.")

# ==========================================================
# Stream Market Data
# ==========================================================

def stream_market_data(
    delay=0.1,
    max_messages=10
):
    """
    Stream FI-2010 sequences to Kafka.
    """

    print("=" * 60)
    print("Starting Market Data Stream...")
    print("=" * 60)

    for message_id, sample in enumerate(X_test[:max_messages], start=1):

        message = {
            "message_id": message_id,
            "timestamp": datetime.now().isoformat(),
            "sequence_length": sample.shape[0],
            "feature_count": sample.shape[1],
            "features": sample.tolist()
        }

        producer.send(
            RAW_MARKET_TOPIC,
            message
        )

        print(
            f"Sent Message {message_id} | "
            f"Shape: {sample.shape}"
        )

        time.sleep(delay)

    producer.flush()
    producer.close()

    print("\nStreaming Completed Successfully.")
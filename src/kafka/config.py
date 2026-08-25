"""
===========================================================
Kafka Pipeline Configuration
===========================================================

Centralized Kafka configuration parameters, topic names,
and consumer/producer settings.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

BOOTSTRAP_SERVERS = [
    "localhost:9092"
]

# Topic Definitions
RAW_MARKET_TOPIC = "raw-market-data"
PROCESSED_MARKET_TOPIC = "processed-market-data"
NEWS_TOPIC = "financial-news"
PREDICTIONS_TOPIC = "predictions"

# Consumer & Producer Settings
CONSUMER_GROUP = "quantformer-group"
ACKS = "all"
RETRIES = 5
REQUEST_TIMEOUT_MS = 30000
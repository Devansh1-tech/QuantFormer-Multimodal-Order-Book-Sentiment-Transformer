"""
===========================================================
Financial News Kafka Consumer (FinBERT Feature Extractor)
===========================================================

Consumes financial headlines from Kafka topic, generates 768-dim
embeddings using HuggingFace FinBERT in inference mode (eval),
and caches the latest news state in memory.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

import torch
from transformers import AutoTokenizer, AutoModel

from src.kafka.consumer import QuantFormerConsumer
from src.kafka.config import NEWS_TOPIC
from src.kafka.latest_news import update_news


# ==========================================================
# Device Configuration
# ==========================================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

# ==========================================================
# Load FinBERT (Loaded once and kept in memory)
# ==========================================================

MODEL_NAME = "ProsusAI/finbert"

print("=" * 60)
print(f"Loading FinBERT on {DEVICE}...")
print("=" * 60)

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

model = AutoModel.from_pretrained(
    MODEL_NAME
)

model = model.to(DEVICE)
model.eval()

print("FinBERT Loaded Successfully (Inference Mode)")

# ==========================================================
# Kafka Consumer
# ==========================================================

consumer = QuantFormerConsumer(
    NEWS_TOPIC
)


# ==========================================================
# Generate Embedding Function
# ==========================================================

def generate_embedding(text: str) -> torch.Tensor:
    """
    Generate 768-dimensional FinBERT sentence embedding.
    """
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    inputs = {
        key: value.to(DEVICE)
        for key, value in inputs.items()
    }

    with torch.no_grad():
        outputs = model(**inputs)

    # Mean-pooling across tokens to obtain sentence embedding (768,)
    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().cpu()

    return embedding


# ==========================================================
# Start News Consumer Loop
# ==========================================================

def start_news_consumer():
    """
    Continuous loop consuming news messages and updating in-memory store.
    """
    print("=" * 60)
    print("News Consumer Started - Listening for Headlines")
    print("=" * 60)

    for message in consumer.listen():
        headline = message.get("headline", "")
        sentiment = message.get("sentiment", "neutral")
        timestamp = message.get("timestamp")

        embedding = generate_embedding(headline)

        # Cache latest news event in memory
        update_news(
            headline=headline,
            sentiment=sentiment,
            embedding=embedding,
            timestamp=timestamp
        )

        print()
        print(f"News ID         : {message.get('news_id', 'N/A')}")
        print(f"Headline        : {headline}")
        print(f"Sentiment       : {sentiment}")
        print(f"Embedding Shape : {embedding.shape}")
        print("-" * 60)


if __name__ == "__main__":
    start_news_consumer()
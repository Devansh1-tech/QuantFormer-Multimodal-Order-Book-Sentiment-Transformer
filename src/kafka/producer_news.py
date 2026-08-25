"""
===========================================================
Financial News Kafka Producer

Streams FinancialPhraseBank headlines
like a live Reuters feed.

Project : QuantFormer
===========================================================
"""

import time
from pathlib import Path

from src.kafka.producer import QuantFormerProducer
from src.kafka.config import NEWS_TOPIC

# ==========================================================
# Dataset Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "datasets"
    / "FinancialPhraseBank-v1.0"
    / "Sentences_50Agree.txt"
)

# ==========================================================
# Load Headlines
# ==========================================================

news_data = []

with open(DATA_PATH, "r", encoding="latin-1") as file:

    for line in file:

        line = line.strip()

        if not line:
            continue

        if "@"in line:

            headline, sentiment = line.rsplit("@", 1)

            news_data.append(
                {
                    "headline": headline.strip(),
                    "sentiment": sentiment.strip()
                }
            )

print("=" * 60)
print("FinancialPhraseBank Loaded Successfully")
print(f"Total Headlines : {len(news_data)}")
print("=" * 60)

# ==========================================================
# Kafka Producer
# ==========================================================

producer = QuantFormerProducer()

# ==========================================================
# Stream News
# ==========================================================

def stream_news(delay=3, max_messages=10):

    print("=" * 60)
    print("Starting Live Financial News Stream")
    print("=" * 60)

    total = min(max_messages, len(news_data))

    for i in range(total):

        news = news_data[i]

        message = {

            "news_id": i + 1,

            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),

            "headline": news["headline"],

            "sentiment": news["sentiment"]

        }

        producer.send(
            NEWS_TOPIC,
            message
        )

        print(f"\nNews {i+1}")

        print(f"Headline : {news['headline']}")

        print(f"Sentiment : {news['sentiment']}")

        time.sleep(delay)

    producer.flush()

    producer.close()

    print()
    print("=" * 60)
    print("News Streaming Completed Successfully")
    print("=" * 60)


if __name__ == "__main__":
    stream_news()
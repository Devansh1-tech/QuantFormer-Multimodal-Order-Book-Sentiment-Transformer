import torch

from transformers import AutoTokenizer
from transformers import AutoModel

from src.kafka.consumer import QuantFormerConsumer
from src.kafka.config import NEWS_TOPIC
from src.kafka.latest_news import update_news


# ==========================================================
# Device
# ==========================================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

# ==========================================================
# Load FinBERT
# ==========================================================

MODEL_NAME = "ProsusAI/finbert"

print("=" * 60)
print("Loading FinBERT...")
print("=" * 60)

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

model = AutoModel.from_pretrained(
    MODEL_NAME
)

model = model.to(DEVICE)

model.eval()

print("FinBERT Loaded Successfully")

# ==========================================================
# Kafka Consumer
# ==========================================================

consumer = QuantFormerConsumer(
    NEWS_TOPIC
)


# ==========================================================
# Generate Embedding
# ==========================================================

def generate_embedding(text):

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

    embedding = outputs.last_hidden_state.mean(dim=1)

    embedding = embedding.squeeze().cpu()

    return embedding


# ==========================================================
# Start Consumer
# ==========================================================

def start_news_consumer():

    print("=" * 60)
    print("News Consumer Started")
    print("=" * 60)

    for message in consumer.listen():

        headline = message["headline"]

        embedding = generate_embedding(
            headline
        )

        update_news(
            headline,
            embedding
        )

        print()

        print(f"News ID : {message['news_id']}")

        print(f"Headline : {headline}")

        print(f"Embedding Shape : {embedding.shape}")

        print("-" * 60)
"""
===========================================================
Multimodal Inference Kafka Consumer
===========================================================

Consumes preprocessed market data sequences, combines them with
the latest cached FinBERT news embedding in memory, executes
inference through QuantFormerFusion, and publishes predictions.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from datetime import datetime
from pathlib import Path
import torch

from src.kafka.consumer import QuantFormerConsumer
from src.kafka.producer import QuantFormerProducer
from src.kafka.config import (
    PROCESSED_MARKET_TOPIC,
    PREDICTIONS_TOPIC
)
from src.kafka.latest_news import (
    get_latest_embedding,
    get_latest_headline,
    get_latest_sentiment
)
from src.models.tft_model import TemporalFusionTransformer
from src.fusion.fusion_model import QuantFormerFusion


# ==========================================================
# Device Configuration
# ==========================================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

# ==========================================================
# Model Loading & Fusion Initialization
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHECKPOINT_PATH = PROJECT_ROOT / "checkpoints" / "best_tft_model.pth"

if not CHECKPOINT_PATH.exists():
    raise FileNotFoundError(
        f"Pretrained TFT Checkpoint not found at:\n{CHECKPOINT_PATH}"
    )

print(f"Loading pretrained TFT checkpoint from:\n{CHECKPOINT_PATH}")

tft_base = TemporalFusionTransformer()
checkpoint = torch.load(
    CHECKPOINT_PATH,
    map_location=DEVICE
)

tft_base.load_state_dict(checkpoint["model_state_dict"])
tft_base = tft_base.to(DEVICE)
tft_base.eval()

# Initialize Multimodal Fusion Model (TFT parameters frozen)
fusion_model = QuantFormerFusion(tft_model=tft_base)
fusion_model = fusion_model.to(DEVICE)
fusion_model.eval()

print("=" * 60)
print("QuantFormer Multimodal Fusion Model Loaded Successfully")
print("=" * 60)


# ==========================================================
# Prediction Function
# ==========================================================

def predict_multimodal(market_sample):
    """
    Run multimodal QuantFormer fusion inference on a market sequence
    using the latest in-memory FinBERT news embedding.

    Parameters
    ----------
    market_sample : list or np.ndarray of shape (100, 143)

    Returns
    -------
    prediction : int (0: Down, 1: Stable, 2: Up)
    confidence : float
    attention  : torch.Tensor
    headline   : str or None
    sentiment  : str or None
    """
    market_tensor = torch.tensor(
        market_sample,
        dtype=torch.float32
    ).unsqueeze(0).to(DEVICE)

    # Fetch cached news context from memory
    latest_embedding = get_latest_embedding()
    headline = get_latest_headline()
    sentiment = get_latest_sentiment()

    if latest_embedding is not None:
        news_tensor = latest_embedding.to(DEVICE)
    else:
        news_tensor = None

    with torch.no_grad():
        (
            logits,
            prediction,
            confidence,
            attention,
            market_features,
            news_features
        ) = fusion_model(market_tensor, news_tensor)

    return (
        prediction.item(),
        confidence.item(),
        attention,
        headline,
        sentiment
    )


# ==========================================================
# Kafka Inference Loop
# ==========================================================

def start_inference():
    """
    Listen to processed market data, perform fusion inference,
    and publish output predictions.
    """
    print("=" * 60)
    print("Multimodal Inference Consumer Started")
    print("=" * 60)

    consumer = QuantFormerConsumer(PROCESSED_MARKET_TOPIC)
    producer = QuantFormerProducer()

    total_predictions = 0

    for message in consumer.listen():
        try:
            (
                prediction,
                confidence,
                attention,
                headline,
                sentiment
            ) = predict_multimodal(message["features"])

            total_predictions += 1

            prediction_message = {
                "message_id": message["message_id"],
                "prediction": int(prediction),
                "confidence": round(float(confidence), 4),
                "market_timestamp": message.get("market_timestamp"),
                "prediction_timestamp": datetime.now().isoformat(),
                "news_headline": headline,
                "news_sentiment": sentiment,
                "status": "predicted"
            }

            producer.send(
                PREDICTIONS_TOPIC,
                prediction_message
            )

            class_names = ["DOWN (0)", "STABLE (1)", "UP (2)"]
            pred_name = class_names[prediction] if 0 <= prediction < 3 else str(prediction)

            print(
                f"[{total_predictions}] Prediction: {pred_name} | "
                f"Confidence: {confidence:.4f} | "
                f"News: {headline[:40] if headline else 'None'}"
            )

        except Exception as error:
            print(f"Inference Consumer Error: {error}")


if __name__ == "__main__":
    start_inference()
import torch
import torch.nn.functional as F
from pathlib import Path
from datetime import datetime

from src.kafka.consumer import QuantFormerConsumer
from src.kafka.producer import QuantFormerProducer

from src.kafka.config import (
    PROCESSED_MARKET_TOPIC,
    PREDICTIONS_TOPIC
)

from src.models.tft_model import TemporalFusionTransformer


# ==========================================================
# Device
# ==========================================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print(f"Using Device : {DEVICE}")


# ==========================================================
# Kafka
# ==========================================================

consumer = QuantFormerConsumer(
    PROCESSED_MARKET_TOPIC
)

producer = QuantFormerProducer()


# ==========================================================
# Model Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CHECKPOINT_PATH = (
    PROJECT_ROOT
    / "checkpoints"
    / "best_tft_model.pth"
)

# ==========================================================
# Load QuantFormer
# ==========================================================

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Checkpoint Path
CHECKPOINT_PATH = (
    PROJECT_ROOT
    / "checkpoints"
    / "best_tft_model.pth"
)

print(f"Loading model from:\n{CHECKPOINT_PATH}")

model = TemporalFusionTransformer()

if not CHECKPOINT_PATH.exists():
    raise FileNotFoundError(
        f"Checkpoint not found:\n{CHECKPOINT_PATH}"
    )

checkpoint = torch.load(
    CHECKPOINT_PATH,
    map_location=DEVICE
)

model.load_state_dict(
    checkpoint["model_state_dict"]
)

model = model.to(DEVICE)
model.eval()

print("=" * 60)
print("QuantFormer Model Loaded Successfully")
print("=" * 60)


# ==========================================================
# Prediction Function
# ==========================================================

def predict_market(sample):
    """
    Run QuantFormer inference on one market sequence.
    """

    x = torch.tensor(
        sample,
        dtype=torch.float32
    ).unsqueeze(0).to(DEVICE)

    with torch.no_grad():

        logits, market_features, attention = model(x)

        probabilities = F.softmax(
            logits,
            dim=1
        )

        confidence, prediction = torch.max(
            probabilities,
            dim=1
        )

    return (
        prediction.item(),
        confidence.item(),
        attention_weights
    )

# ==========================================================
# Kafka Inference
# ==========================================================

def start_inference():

    print("=" * 60)
    print("Inference Consumer Started")
    print("=" * 60)

    for message in consumer.listen():

        try:

            prediction, confidence, attention_weights = predict_market(
                message["features"]
            )

            prediction_message = {

                "message_id":
                    message["message_id"],

                "prediction":
                    int(prediction),

                "confidence":
                    float(confidence),

                "market_timestamp":
                    message["market_timestamp"],

                "prediction_timestamp":
                    datetime.now().isoformat()

            }

            producer.send(
                PREDICTIONS_TOPIC,
                prediction_message
            )

            print(
                f"Prediction "
                f"{prediction} | "
                f"Confidence {confidence:.4f}"
            )

        except Exception as e:

            print(e)
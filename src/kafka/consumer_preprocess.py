from datetime import datetime

from src.kafka.consumer import QuantFormerConsumer
from src.kafka.producer import QuantFormerProducer

from src.kafka.config import (
    RAW_MARKET_TOPIC,
    PROCESSED_MARKET_TOPIC
)


# ==========================================================
# Initialize Kafka
# ==========================================================

consumer = QuantFormerConsumer(
    RAW_MARKET_TOPIC
)

producer = QuantFormerProducer()


# ==========================================================
# Preprocessing Function
# ==========================================================

def preprocess_message(message):
    

    required_keys = [
        "message_id",
        "timestamp",
        "sequence_length",
        "feature_count",
        "features"
    ]

    for key in required_keys:

        if key not in message:

            raise ValueError(
                f"Missing key: {key}"
            )

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
    Consume raw market data,
    preprocess it,
    and publish to processed topic.
    """

    print("=" * 60)
    print("Preprocessing Consumer Started")
    print("=" * 60)

    for message in consumer.listen():

        try:

            processed = preprocess_message(
                message
            )

            producer.send(
                PROCESSED_MARKET_TOPIC,
                processed
            )

            print(
                f"Processed Message "
                f"{processed['message_id']}"
            )

        except Exception as error:

            print(
                f"Error : {error}"
            )



def start_inference():

    print("=" * 60)
    print("Inference Consumer Started")
    print("=" * 60)

    total_predictions = 0

    for message in consumer.listen():

        try:

            prediction, confidence, _ = predict_market(
                message["features"]
            )

            prediction_message = {

                "message_id": message["message_id"],

                "market_timestamp": message["market_timestamp"],

                "prediction_timestamp": datetime.now().isoformat(),

                "prediction": int(prediction),

                "confidence": round(
                    float(confidence),
                    4
                ),

                "status": "predicted"

            }

            producer.send(
                PREDICTIONS_TOPIC,
                prediction_message
            )

            total_predictions += 1

            print(
                f"[{total_predictions}] "
                f"Prediction = {prediction} | "
                f"Confidence = {confidence:.4f}"
            )

        except Exception as error:

            print(f"Inference Error: {error}")


if __name__ == "__main__":

    start_inference()
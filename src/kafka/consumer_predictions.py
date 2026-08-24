from src.kafka.consumer import QuantFormerConsumer
from src.kafka.config import PREDICTIONS_TOPIC

consumer = QuantFormerConsumer(
    PREDICTIONS_TOPIC
)


def monitor_predictions():

    print("=" * 60)
    print("Prediction Monitor Started")
    print("=" * 60)

    total_predictions = 0

    for message in consumer.listen():

        total_predictions += 1

        print()

        print("=" * 60)

        print(f"Prediction #{total_predictions}")

        print(f"Message ID : {message['message_id']}")

        print(f"Prediction : {message['prediction']}")

        print(f"Confidence : {message['confidence']:.4f}")

        print(f"Market Time : {message['market_timestamp']}")

        print(f"Prediction Time : {message['prediction_timestamp']}")

        print("=" * 60)



if __name__ == "__main__":

    monitor_predictions()
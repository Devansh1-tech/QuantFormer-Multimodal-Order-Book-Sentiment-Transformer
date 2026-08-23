"""
===========================================================
Training Visualization

Project : QuantFormer
===========================================================
"""

import matplotlib.pyplot as plt


def plot_training_history(history):

    plt.figure(figsize=(10,5))

    plt.plot(
        history["train_loss"],
        label="Train Loss"
    )

    plt.plot(
        history["val_loss"],
        label="Validation Loss"
    )

    plt.xlabel("Epoch")

    plt.ylabel("Loss")

    plt.title("Training Loss")

    plt.legend()

    plt.grid(True)

    plt.show()

    plt.figure(figsize=(10,5))

    plt.plot(
        history["train_accuracy"],
        label="Train Accuracy"
    )

    plt.plot(
        history["val_accuracy"],
        label="Validation Accuracy"
    )

    plt.xlabel("Epoch")

    plt.ylabel("Accuracy")

    plt.title("Training Accuracy")

    plt.legend()

    plt.grid(True)

    plt.show()
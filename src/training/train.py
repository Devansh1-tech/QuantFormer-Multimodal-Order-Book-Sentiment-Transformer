"""
===========================================================
Training Pipeline

Project : QuantFormer

Contains the training and validation loops
for the Temporal Fusion Transformer.

Author : Team QuantFormer
===========================================================
"""

import torch
from tqdm.auto import tqdm

from sklearn.metrics import accuracy_score


# ==========================================================
# Device
# ==========================================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print(f"Using Device : {DEVICE}")

# ==========================================================
# Training Function
# ==========================================================

def train_one_epoch(
    model,
    dataloader,
    optimizer,
    criterion
):
    """
    Train model for one epoch.
    """

    model.train()

    running_loss = 0.0

    predictions = []

    labels = []

    progress_bar = tqdm(
        dataloader,
        desc="Training",
        leave=False
    )

    for features, targets in progress_bar:

        features = features.to(DEVICE)

        targets = targets.to(DEVICE)

        optimizer.zero_grad()

        logits, _ = model(features)

        loss = criterion(
            logits,
            targets
        )

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

        preds = torch.argmax(
            logits,
            dim=1
        )

        predictions.extend(
            preds.cpu().numpy()
        )

        labels.extend(
            targets.cpu().numpy()
        )

        progress_bar.set_postfix(
            loss=f"{loss.item():.4f}"
        )

    epoch_loss = running_loss / len(dataloader)

    epoch_accuracy = accuracy_score(
        labels,
        predictions
    )

    return epoch_loss, epoch_accuracy

# ==========================================================
# Validation Function
# ==========================================================

@torch.no_grad()

def validate_one_epoch(
    model,
    dataloader,
    criterion
):
    """
    Validation loop.
    """

    model.eval()

    running_loss = 0.0

    predictions = []

    labels = []

    progress_bar = tqdm(
        dataloader,
        desc="Validation",
        leave=False
    )

    for features, targets in progress_bar:

        features = features.to(DEVICE)

        targets = targets.to(DEVICE)

        logits, _ = model(features)

        loss = criterion(
            logits,
            targets
        )

        running_loss += loss.item()

        preds = torch.argmax(
            logits,
            dim=1
        )

        predictions.extend(
            preds.cpu().numpy()
        )

        labels.extend(
            targets.cpu().numpy()
        )

        progress_bar.set_postfix(
            loss=f"{loss.item():.4f}"
        )

    epoch_loss = running_loss / len(dataloader)

    epoch_accuracy = accuracy_score(
        labels,
        predictions
    )

    return (
        epoch_loss,
        epoch_accuracy,
        predictions,
        labels
    )

# ==========================================================
# Complete Training Pipeline
# ==========================================================

import copy


def train_model(
    model,
    train_loader,
    val_loader,
    optimizer,
    scheduler,
    criterion,
    epochs,
    save_path
):
    """
    Complete QuantFormer training pipeline.
    """

    model = model.to(DEVICE)

    history = {
        "train_loss": [],
        "train_accuracy": [],
        "val_loss": [],
        "val_accuracy": []
    }

    best_accuracy = 0.0
    best_model = None

    for epoch in range(epochs):

        print("=" * 70)
        print(f"Epoch {epoch + 1}/{epochs}")
        print("=" * 70)

        train_loss, train_acc = train_one_epoch(
            model,
            train_loader,
            optimizer,
            criterion
        )

        val_loss, val_acc, predictions, labels = validate_one_epoch(
            model,
            val_loader,
            criterion
        )

        scheduler.step()

        history["train_loss"].append(train_loss)
        history["train_accuracy"].append(train_acc)
        history["val_loss"].append(val_loss)
        history["val_accuracy"].append(val_acc)

        print(f"Train Loss     : {train_loss:.4f}")
        print(f"Train Accuracy : {train_acc:.4f}")
        print(f"Valid Loss     : {val_loss:.4f}")
        print(f"Valid Accuracy : {val_acc:.4f}")

        if val_acc > best_accuracy:

            best_accuracy = val_acc

            best_model = copy.deepcopy(
                model.state_dict()
            )

            torch.save(
                best_model,
                save_path
            )

            print("✅ Best model saved.")

        print()

    print("=" * 70)
    print("Training Finished")
    print(f"Best Validation Accuracy : {best_accuracy:.4f}")
    print("=" * 70)

    return history


import copy
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
# Train One Epoch
# ==========================================================

def train_one_epoch(
    model,
    dataloader,
    optimizer,
    criterion
):
    """
    Train QuantFormer for one epoch.
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
# Validation One Epoch
# ==========================================================

@torch.no_grad()

def validate_one_epoch(
    model,
    dataloader,
    criterion
):
    """
    Validate QuantFormer for one epoch.
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

        "val_accuracy": [],

        "learning_rate": []

    }

    best_accuracy = 0.0

    best_checkpoint = None

    for epoch in range(epochs):

        print("=" * 70)
        print(f"Epoch {epoch + 1}/{epochs}")
        print("=" * 70)

        # ------------------------------
        # Training
        # ------------------------------

        train_loss, train_acc = train_one_epoch(

            model,

            train_loader,

            optimizer,

            criterion

        )

        # ------------------------------
        # Validation
        # ------------------------------

        val_loss, val_acc, predictions, labels = validate_one_epoch(

            model,

            val_loader,

            criterion

        )

        # ------------------------------
        # Scheduler
        # ------------------------------

        scheduler.step(val_loss)

        current_lr = optimizer.param_groups[0]["lr"]

        # ------------------------------
        # History
        # ------------------------------

        history["train_loss"].append(train_loss)

        history["train_accuracy"].append(train_acc)

        history["val_loss"].append(val_loss)

        history["val_accuracy"].append(val_acc)

        history["learning_rate"].append(current_lr)

        # ------------------------------
        # Print Metrics
        # ------------------------------

        print(f"Train Loss       : {train_loss:.4f}")
        print(f"Train Accuracy   : {train_acc:.4f}")
        print(f"Validation Loss  : {val_loss:.4f}")
        print(f"Validation Acc   : {val_acc:.4f}")
        print(f"Learning Rate    : {current_lr:.6f}")

        # ------------------------------
        # Save Best Model
        # ------------------------------

        if val_acc > best_accuracy:

            best_accuracy = val_acc

            best_checkpoint = {

                "epoch": epoch + 1,

                "model_state_dict": copy.deepcopy(
                    model.state_dict()
                ),

                "optimizer_state_dict": optimizer.state_dict(),

                "best_validation_accuracy": best_accuracy

            }

            torch.save(

                best_checkpoint,

                save_path

            )

            print("Best model checkpoint saved.")

        print()

    print("=" * 70)
    print("Training Completed")
    print("=" * 70)

    print(f"Best Validation Accuracy : {best_accuracy:.4f}")

    print("=" * 70)

    return history, best_accuracy
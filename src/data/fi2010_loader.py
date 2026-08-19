"""
===========================================================
FI-2010 Dataset Loader

This module loads the preprocessed FI-2010 dataset,
creates custom PyTorch Dataset objects and DataLoaders.

Author : Team QuantFormer
Project: QuantFormer
===========================================================
"""

import numpy as np
import torch

from torch.utils.data import Dataset, DataLoader

from src.config import (
    X_TRAIN_PATH,
    Y_TRAIN_PATH,
    X_VAL_PATH,
    Y_VAL_PATH,
    X_TEST_PATH,
    Y_TEST_PATH,
    BATCH_SIZE,
    NUM_WORKERS,
    PIN_MEMORY,
    SHUFFLE
)


# ==========================================================
# Custom Dataset
# ==========================================================

class FI2010Dataset(Dataset):
    """
    Custom Dataset for the FI-2010 dataset.

    Each sample consists of:
        - Order book sequence
        - Target class
    """

    def __init__(self, X, y):

        self.X = X
        self.y = y

    def __len__(self):

        return len(self.X)

    def __getitem__(self, idx):

        features = torch.from_numpy(self.X[idx]).float()

        label = torch.tensor(
            self.y[idx],
            dtype=torch.long
        )

        return features, label


# ==========================================================
# Load NumPy Files
# ==========================================================

def load_numpy_data():
    """
    Load processed NumPy arrays.
    """

    X_train = np.load(X_TRAIN_PATH)
    y_train = np.load(Y_TRAIN_PATH)

    X_val = np.load(X_VAL_PATH)
    y_val = np.load(Y_VAL_PATH)

    X_test = np.load(X_TEST_PATH)
    y_test = np.load(Y_TEST_PATH)

    return (
        X_train,
        y_train,
        X_val,
        y_val,
        X_test,
        y_test
    )


# ==========================================================
# Create Dataset Objects
# ==========================================================

def create_datasets():
    """
    Create Dataset objects.
    """

    (
        X_train,
        y_train,
        X_val,
        y_val,
        X_test,
        y_test
    ) = load_numpy_data()

    train_dataset = FI2010Dataset(
        X_train,
        y_train
    )

    val_dataset = FI2010Dataset(
        X_val,
        y_val
    )

    test_dataset = FI2010Dataset(
        X_test,
        y_test
    )

    return (
        train_dataset,
        val_dataset,
        test_dataset
    )


# ==========================================================
# Create DataLoaders
# ==========================================================

def create_dataloaders(
    batch_size=BATCH_SIZE
):
    """
    Create DataLoaders.
    """

    (
        train_dataset,
        val_dataset,
        test_dataset
    ) = create_datasets()

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=SHUFFLE,
        num_workers=NUM_WORKERS,
        pin_memory=PIN_MEMORY
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=PIN_MEMORY
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=PIN_MEMORY
    )

    return (
        train_loader,
        val_loader,
        test_loader
    )


# ==========================================================
# Dataset Information
# ==========================================================

def dataset_summary():
    """
    Print dataset statistics.
    """

    (
        X_train,
        y_train,
        X_val,
        y_val,
        X_test,
        y_test
    ) = load_numpy_data()

    print("=" * 60)

    print("FI-2010 Dataset Summary")

    print("-" * 60)

    print(f"Train Samples      : {len(X_train):,}")
    print(f"Validation Samples : {len(X_val):,}")
    print(f"Test Samples       : {len(X_test):,}")

    print()

    print(f"Sequence Length    : {X_train.shape[1]}")
    print(f"Features           : {X_train.shape[2]}")

    print()

    print(f"Classes            : {np.unique(y_train)}")

    print("=" * 60)
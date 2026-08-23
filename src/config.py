"""
===========================================================
QuantFormer Configuration File
===========================================================

This file contains all configurable parameters used across
the QuantFormer project.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

import os
import torch

# ==========================================================
# Project Directories
# ==========================================================

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DATASET_DIR = os.path.join(PROJECT_ROOT, "datasets")
PROCESSED_DATA_DIR = os.path.join(DATASET_DIR, "processed")

FI2010_DIR = os.path.join(PROCESSED_DATA_DIR, "FI2010")
PHRASEBANK_DIR = os.path.join(PROCESSED_DATA_DIR, "PhraseBank")

SAVED_MODEL_DIR = os.path.join(PROJECT_ROOT, "saved_models")
ARTIFACT_DIR = os.path.join(PROJECT_ROOT, "artifacts")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "outputs")

# ==========================================================
# Dataset Files
# ==========================================================

X_TRAIN_PATH = os.path.join(FI2010_DIR, "X_train.npy")
Y_TRAIN_PATH = os.path.join(FI2010_DIR, "y_train.npy")

X_VAL_PATH = os.path.join(FI2010_DIR, "X_val.npy")
Y_VAL_PATH = os.path.join(FI2010_DIR, "y_val.npy")

X_TEST_PATH = os.path.join(FI2010_DIR, "X_test.npy")
Y_TEST_PATH = os.path.join(FI2010_DIR, "y_test.npy")

# ==========================================================
# General Configuration
# ==========================================================

SEED = 42

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

# ==========================================================
# Data Configuration
# ==========================================================

SEQUENCE_LENGTH = 100

NUM_FEATURES = 143

NUM_CLASSES = 3

# ==========================================================
# DataLoader Configuration
# ==========================================================

BATCH_SIZE = 128

NUM_WORKERS = 0

PIN_MEMORY = torch.cuda.is_available()

SHUFFLE = True

# ==========================================================
# Training Configuration
# ==========================================================

EPOCHS = 20

LEARNING_RATE = 1e-4

WEIGHT_DECAY = 1e-5

GRADIENT_CLIP = 1.0

# ==========================================================
# TFT Architecture
# ==========================================================

INPUT_SIZE = NUM_FEATURES

HIDDEN_SIZE = 128

LSTM_LAYERS = 2

ATTENTION_HEADS = 4

DROPOUT = 0.2

EMBEDDING_SIZE = 128

OUTPUT_SIZE = NUM_CLASSES

# ==========================================================
# Scheduler
# ==========================================================

SCHEDULER_PATIENCE = 3

SCHEDULER_FACTOR = 0.5

MIN_LEARNING_RATE = 1e-6

# ==========================================================
# Early Stopping
# ==========================================================

EARLY_STOPPING_PATIENCE = 5

# ==========================================================
# Saving Paths
# ==========================================================

BEST_TFT_MODEL = os.path.join(
    SAVED_MODEL_DIR,
    "best_tft_model.pth"
)

BEST_FINBERT_MODEL = os.path.join(
    SAVED_MODEL_DIR,
    "best_finbert_model.pth"
)

TFT_EMBEDDINGS = os.path.join(
    ARTIFACT_DIR,
    "tft_embeddings.npy"
)

FINBERT_EMBEDDINGS = os.path.join(
    ARTIFACT_DIR,
    "finbert_embeddings.npy"
)

# ==========================================================
# Logging
# ==========================================================

PRINT_EVERY = 10

SAVE_BEST_ONLY = True
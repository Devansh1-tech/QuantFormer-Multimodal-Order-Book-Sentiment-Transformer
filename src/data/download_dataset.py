"""
Download QuantFormer Resources from Google Drive

Author: QuantFormer Team
"""

import os
import gdown


# ==========================================================
# Create Required Directories
# ==========================================================

DATASET_DIR = "datasets/FI2010"
MODEL_DIR = "saved_models"

os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)


# ==========================================================
# Google Drive File IDs
# ==========================================================

TRAIN_FILE_ID = "10XnGpLq4OyAvYdg9HAU7VX4wo4FbEgxC"
TEST_FILE_ID = "1wWLVBNMk7Elxu_a9REsrhqppowseBT1-"

FINBERT_MODEL_ID = "1Ooy54QRylGhukZRDe97F8XSx6uo_ExxL"


# ==========================================================
# Output Paths
# ==========================================================

TRAIN_OUTPUT = os.path.join(
    DATASET_DIR,
    "train_clean.csv"
)

TEST_OUTPUT = os.path.join(
    DATASET_DIR,
    "test_clean.csv"
)

FINBERT_OUTPUT = os.path.join(
    MODEL_DIR,
    "best_finbert_model.pth"
)


# ==========================================================
# Download Train Dataset
# ==========================================================

print("=" * 60)
print("Downloading train_clean.csv...")
print("=" * 60)

gdown.download(
    f"https://drive.google.com/uc?id={TRAIN_FILE_ID}",
    TRAIN_OUTPUT,
    quiet=False
)


# ==========================================================
# Download Test Dataset
# ==========================================================

print("=" * 60)
print("Downloading test_clean.csv...")
print("=" * 60)

gdown.download(
    f"https://drive.google.com/uc?id={TEST_FILE_ID}",
    TEST_OUTPUT,
    quiet=False
)


# ==========================================================
# Download FinBERT Model
# ==========================================================

print("=" * 60)
print("Downloading best_finbert_model.pth...")
print("=" * 60)

gdown.download(
    f"https://drive.google.com/uc?id={FINBERT_MODEL_ID}",
    FINBERT_OUTPUT,
    quiet=False
)


# ==========================================================
# Done
# ==========================================================

print("\n" + "=" * 60)
print("All files downloaded successfully!")
print("=" * 60)

print(f"Train Dataset : {TRAIN_OUTPUT}")
print(f"Test Dataset  : {TEST_OUTPUT}")
print(f"FinBERT Model : {FINBERT_OUTPUT}")
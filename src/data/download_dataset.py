"""
Download FI-2010 Clean Dataset from Google Drive

Author: QuantFormer Team
"""

import os
import gdown


# ===========================
# Create Dataset Directory
# ===========================

DATASET_DIR = "datasets/FI2010"

os.makedirs(DATASET_DIR, exist_ok=True)


# ===========================
# Google Drive File IDs
# ===========================

TRAIN_FILE_ID = "10XnGpLq4OyAvYdg9HAU7VX4wo4FbEgxC"
TEST_FILE_ID = "1wWLVBNMk7Elxu_a9REsrhqppowseBT1-"


# ===========================
# Output Paths
# ===========================

TRAIN_OUTPUT = os.path.join(DATASET_DIR, "train_clean.csv")
TEST_OUTPUT = os.path.join(DATASET_DIR, "test_clean.csv")


# ===========================
# Download Files
# ===========================

print("Downloading train_clean.csv...")
gdown.download(
    f"https://drive.google.com/uc?id={TRAIN_FILE_ID}",
    TRAIN_OUTPUT,
    quiet=False
)

print("Downloading test_clean.csv...")
gdown.download(
    f"https://drive.google.com/uc?id={TEST_FILE_ID}",
    TEST_OUTPUT,
    quiet=False
)

print("\nDataset downloaded successfully!")
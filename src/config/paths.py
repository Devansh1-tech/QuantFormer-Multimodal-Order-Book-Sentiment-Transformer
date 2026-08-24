from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Main folders
DATASETS = PROJECT_ROOT / "datasets"
CHECKPOINTS = PROJECT_ROOT / "checkpoints"

# Dataset folderss
PROCESSED = DATASETS / "processed"
RAW = DATASETS / "FinancialPhraseBank-v1.0"
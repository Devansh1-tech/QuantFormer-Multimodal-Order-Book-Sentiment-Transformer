"""
===========================================================
QuantFormer Backend — Constants
===========================================================

Centralized domain-specific constants used across the entire
backend. Keeps magic strings and semantic labels in one place.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

# ===========================================================
# TFT Market Prediction Classes
# ===========================================================
# These correspond to the 3 output classes of the
# Temporal Fusion Transformer trained on FI-2010.
# ===========================================================

TFT_CLASS_NAMES = ["Down", "Stable", "Up"]

TFT_NUM_CLASSES = 3

# ===========================================================
# TFT → Market Trend Mapping
# ===========================================================
# Maps TFT class predictions to human-readable market trends.
# ===========================================================

TFT_TREND_MAP = {
    "Down": "Bearish",
    "Stable": "Neutral",
    "Up": "Bullish",
}

# ===========================================================
# FinBERT Sentiment Labels
# ===========================================================
# ProsusAI/finbert outputs 3 classes in this order.
# ===========================================================

FINBERT_LABELS = ["positive", "negative", "neutral"]

FINBERT_NUM_CLASSES = 3

# ===========================================================
# Multimodal Insight Matrix
# ===========================================================
# Maps (market_trend, news_sentiment) → overall_insight.
# Used by the Insight and Explain services.
# ===========================================================

INSIGHT_MATRIX = {
    ("Bullish", "positive"):  "Strong Bullish",
    ("Bullish", "neutral"):   "Bullish",
    ("Bullish", "negative"):  "Weak Bullish",
    ("Neutral", "positive"):  "Slightly Bullish",
    ("Neutral", "neutral"):   "Neutral",
    ("Neutral", "negative"):  "Slightly Bearish",
    ("Bearish", "positive"):  "Weak Bearish",
    ("Bearish", "neutral"):   "Bearish",
    ("Bearish", "negative"):  "Strong Bearish",
}

# ===========================================================
# Default Stock Symbols
# ===========================================================

POPULAR_SYMBOLS = [
    "AAPL", "MSFT", "GOOGL", "NVDA", "TSLA",
    "AMZN", "META", "JPM", "V", "WMT",
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "SBIN.NS",
]

# ===========================================================
# Model Metadata
# ===========================================================

MODEL_INFO = {
    "tft": {
        "name": "Temporal Fusion Transformer",
        "version": "1.0.0",
        "architecture": "LSTM + Multi-Head Attention + GRN",
        "input_shape": "(B, 100, 143)",
        "output_classes": TFT_NUM_CLASSES,
        "accuracy": 84.51,
        "role": "Primary Production Prediction Model",
    },
    "finbert": {
        "name": "FinBERT",
        "version": "1.0.0",
        "architecture": "ProsusAI/finbert (BERT-base fine-tuned)",
        "embedding_dim": 768,
        "output_classes": FINBERT_NUM_CLASSES,
        "role": "Financial News Sentiment Analysis",
    },
    "fusion": {
        "name": "QuantFormer Fusion",
        "version": "1.0.0",
        "architecture": "TFT Features (128D) + FinBERT Embeddings (768D) → Fusion Classifier",
        "output_classes": TFT_NUM_CLASSES,
        "role": "Internal Multimodal Insight Enrichment (Research)",
    },
}

# ===========================================================
# Disclaimers
# ===========================================================

INSIGHT_DISCLAIMER = (
    "This insight is generated using multimodal analysis and "
    "should not be considered financial advice."
)

PREDICTION_DISCLAIMER = (
    "AI-generated analysis. Do not rely solely on this "
    "prediction for investment decisions."
)

# ===========================================================
# Model Architecture Constants (mirrored from project_config)
# ===========================================================
# These are fixed values matching the trained checkpoints.
# They are NOT configurable — changing them would break
# checkpoint loading.
# ===========================================================

TFT_NUM_FEATURES = 143
TFT_HIDDEN_SIZE = 128
TFT_SEQUENCE_LENGTH = 100
FINBERT_EMBEDDING_DIM = 768

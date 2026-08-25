"""
===========================================================
In-Memory Latest News Store
===========================================================

Thread-safe / in-memory cache holding the most recent financial
news headline, sentiment label, FinBERT embedding, and timestamp.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from datetime import datetime
import torch

_latest_headline: str = None
_latest_sentiment: str = None
_latest_embedding: torch.Tensor = None
_latest_timestamp: str = None


def update_news(
    headline: str,
    sentiment: str,
    embedding: torch.Tensor,
    timestamp: str = None
):
    """
    Update the in-memory cache with the latest news event.

    Parameters
    ----------
    headline  : str, news headline text
    sentiment : str, sentiment label (e.g. positive, negative, neutral)
    embedding : torch.Tensor, 768-dim FinBERT embedding tensor
    timestamp : str, timestamp string (optional, defaults to now)
    """
    global _latest_headline
    global _latest_sentiment
    global _latest_embedding
    global _latest_timestamp

    _latest_headline = headline
    _latest_sentiment = sentiment
    _latest_embedding = embedding
    _latest_timestamp = timestamp or datetime.now().isoformat()


def get_latest_news() -> dict:
    """
    Get the complete latest news state dictionary.

    Returns
    -------
    dict with keys: headline, sentiment, embedding, timestamp
    """
    return {
        "headline": _latest_headline,
        "sentiment": _latest_sentiment,
        "embedding": _latest_embedding,
        "timestamp": _latest_timestamp
    }


def get_latest_embedding() -> torch.Tensor:
    """
    Get the most recent FinBERT embedding tensor.
    """
    return _latest_embedding


def get_latest_headline() -> str:
    """
    Get the most recent news headline string.
    """
    return _latest_headline


def get_latest_sentiment() -> str:
    """
    Get the most recent news sentiment string.
    """
    return _latest_sentiment


def get_latest_timestamp() -> str:
    """
    Get the most recent news timestamp string.
    """
    return _latest_timestamp
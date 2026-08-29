"""
===========================================================
QuantFormer Backend — Sentiment Service
===========================================================

FinBERT sentiment analysis with human-readable explanations.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

import logging
from typing import Dict, Any

from backend.app.models.model_manager import ModelManager
from backend.app.utils.helpers import LatencyTimer, utc_now_iso

logger = logging.getLogger(__name__)
prediction_logger = logging.getLogger("quantformer.prediction")


# ===========================================================
# Sentiment Explanation Templates
# ===========================================================

_EXPLANATIONS = {
    "positive": (
        "The financial text expresses a positive outlook. "
        "Keywords and context suggest optimistic market sentiment, "
        "indicating potential growth or favorable conditions."
    ),
    "negative": (
        "The financial text expresses a negative outlook. "
        "Keywords and context suggest pessimistic market sentiment, "
        "indicating potential decline or unfavorable conditions."
    ),
    "neutral": (
        "The financial text expresses a neutral outlook. "
        "The content is factual or balanced without strong "
        "directional sentiment indicators."
    ),
}


class SentimentService:
    """
    FinBERT sentiment analysis service.

    Runs FinBERT inference via ModelManager and generates
    human-readable explanations of the sentiment result.
    """

    def __init__(self, model_manager: ModelManager):
        self._manager = model_manager

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of financial text using FinBERT.

        Parameters
        ----------
        text : str — Financial news text

        Returns
        -------
        dict ready for SentimentResponse schema

        Raises
        ------
        RuntimeError — if FinBERT model is not loaded
        """
        with LatencyTimer() as timer:
            result = self._manager.analyze_sentiment(text)

        sentiment = result["sentiment"]
        explanation = _EXPLANATIONS.get(sentiment, "Sentiment analysis completed.")

        # Add confidence context to explanation
        confidence = result["confidence"]
        if confidence >= 90:
            explanation += f" The model is highly confident ({confidence}%) in this assessment."
        elif confidence >= 70:
            explanation += f" The model is moderately confident ({confidence}%) in this assessment."
        else:
            explanation += f" The model has lower confidence ({confidence}%) — the text may contain mixed signals."

        # Log sentiment analysis
        prediction_logger.info(
            f"FinBERT Sentiment | "
            f"Result: {sentiment} | "
            f"Confidence: {confidence}% | "
            f"Latency: {timer.elapsed_ms}ms | "
            f"Text: {text[:80]}..."
        )

        return {
            "success": True,
            "text": text,
            "sentiment": sentiment,
            "confidence": confidence,
            "scores": result["scores"],
            "explanation": explanation,
            "model_name": "FinBERT",
            "latency_ms": timer.elapsed_ms,
            "timestamp": utc_now_iso(),
            # Internal: pass embedding for downstream services
            "_embedding": result["embedding"],
        }

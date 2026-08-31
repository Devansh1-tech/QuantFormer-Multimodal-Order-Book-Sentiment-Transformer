"""
===========================================================
QuantFormer Backend — Prediction Service
===========================================================

TFT inference pipeline for market direction prediction.
This is the ONLY production prediction service.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

import logging
from typing import Dict, List, Any, Optional

import numpy as np
import torch

from app.models.model_manager import ModelManager
from app.utils.constants import TFT_SEQUENCE_LENGTH, TFT_NUM_FEATURES
from app.utils.helpers import LatencyTimer, utc_now_iso

logger = logging.getLogger(__name__)
prediction_logger = logging.getLogger("quantformer.prediction")


class PredictionService:
    """
    TFT market prediction service.

    Validates input, runs inference via ModelManager,
    and formats the response.
    """

    def __init__(self, model_manager: ModelManager):
        self._manager = model_manager

    def predict(
        self,
        features: List[List[float]],
        symbol: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Run TFT inference on market features.

        Parameters
        ----------
        features : list of lists, shape (100, 143)
        symbol : optional stock symbol for labeling

        Returns
        -------
        dict ready for PredictResponse schema

        Raises
        ------
        ValueError — if feature dimensions are invalid
        RuntimeError — if TFT model is not loaded
        """
        # Validate input dimensions
        features_array = np.array(features, dtype=np.float32)

        if features_array.ndim != 2:
            raise ValueError(
                f"Expected 2D features array, got {features_array.ndim}D"
            )

        if features_array.shape[0] != TFT_SEQUENCE_LENGTH:
            raise ValueError(
                f"Expected sequence length {TFT_SEQUENCE_LENGTH}, "
                f"got {features_array.shape[0]}"
            )

        if features_array.shape[1] != TFT_NUM_FEATURES:
            raise ValueError(
                f"Expected {TFT_NUM_FEATURES} features, "
                f"got {features_array.shape[1]}"
            )

        # Convert to tensor
        features_tensor = torch.from_numpy(features_array).float()

        # Run inference with latency measurement
        with LatencyTimer() as timer:
            result = self._manager.predict_tft(features_tensor)

        # Log prediction
        prediction_logger.info(
            f"TFT Prediction | "
            f"Symbol: {symbol or 'N/A'} | "
            f"Result: {result['prediction']} ({result['trend']}) | "
            f"Confidence: {result['confidence']}% | "
            f"Latency: {timer.elapsed_ms}ms"
        )

        return {
            "success": True,
            "prediction": result["prediction"],
            "market_trend": result["trend"],
            "confidence": result["confidence"],
            "probabilities": result["probabilities"],
            "latency_ms": timer.elapsed_ms,
            "model_name": "Temporal Fusion Transformer",
            "model_version": "1.0.0",
            "symbol": symbol,
            "timestamp": utc_now_iso(),
        }

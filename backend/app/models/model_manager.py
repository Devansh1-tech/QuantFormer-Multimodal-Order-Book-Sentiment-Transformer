"""
===========================================================
QuantFormer Backend — Model Manager (Singleton)
===========================================================

Thread-safe singleton that loads and manages all three
QuantFormer AI models:

  1. Temporal Fusion Transformer (TFT) — Primary Prediction
  2. FinBERT — News Sentiment Analysis
  3. QuantFormer Fusion — Internal Multimodal Insight

Models are loaded once during application startup (lifespan).
Supports CUDA and CPU. Exposes health status for monitoring.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

import logging
import threading
from pathlib import Path
from typing import Dict, Optional, Any

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

logger = logging.getLogger(__name__)


class ModelManager:
    """
    Singleton manager for all QuantFormer AI models.

    Usage:
        manager = ModelManager()
        await manager.load_all_models(settings)
        logits = manager.predict_tft(features_tensor)
    """

    _instance: Optional["ModelManager"] = None
    _lock = threading.Lock()

    def __new__(cls) -> "ModelManager":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        # Device
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        # Model references
        self._tft_model = None
        self._finbert_model = None
        self._finbert_tokenizer = None
        self._fusion_model = None

        # Status tracking
        self._tft_loaded = False
        self._finbert_loaded = False
        self._fusion_loaded = False

        self._tft_checkpoint_exists = False
        self._finbert_checkpoint_exists = False
        self._fusion_checkpoint_exists = False

        self._checkpoint_paths: Dict[str, str] = {}

    # ==========================================================
    # Model Loading
    # ==========================================================

    async def load_all_models(self, settings) -> None:
        """
        Load all three models from checkpoints.
        Called once during FastAPI lifespan startup.
        """
        logger.info("=" * 60)
        logger.info("QuantFormer Model Manager — Loading Models")
        logger.info(f"Device: {self.device}")
        logger.info("=" * 60)

        self._load_tft(settings)
        self._load_finbert(settings)
        self._load_fusion(settings)

        loaded_count = sum([
            self._tft_loaded,
            self._finbert_loaded,
            self._fusion_loaded,
        ])

        logger.info("=" * 60)
        logger.info(f"Model Loading Complete: {loaded_count}/3 models loaded")
        logger.info("=" * 60)

    def _load_tft(self, settings) -> None:
        """Load the Temporal Fusion Transformer checkpoint."""
        checkpoint_path = Path(settings.tft_checkpoint_abs)
        self._checkpoint_paths["tft"] = str(checkpoint_path)
        self._tft_checkpoint_exists = checkpoint_path.exists()

        if not self._tft_checkpoint_exists:
            logger.error(f"TFT checkpoint not found: {checkpoint_path}")
            return

        try:
            # Import the model class from the existing project
            from src.models.tft_model import TemporalFusionTransformer

            self._tft_model = TemporalFusionTransformer()
            checkpoint = torch.load(
                str(checkpoint_path),
                map_location=self.device,
                weights_only=False,
            )
            self._tft_model.load_state_dict(checkpoint["model_state_dict"])
            self._tft_model.to(self.device)
            self._tft_model.eval()
            self._tft_loaded = True

            accuracy = checkpoint.get("best_validation_accuracy", "N/A")
            logger.info(
                f"[OK] TFT loaded successfully | "
                f"Accuracy: {accuracy} | Device: {self.device}"
            )

        except Exception as e:
            logger.error(f"[FAIL] Failed to load TFT: {e}", exc_info=True)

    def _load_finbert(self, settings) -> None:
        """Load the FinBERT model for sentiment analysis."""
        checkpoint_path = Path(settings.finbert_checkpoint_abs)
        self._checkpoint_paths["finbert"] = str(checkpoint_path)
        self._finbert_checkpoint_exists = checkpoint_path.exists()

        try:
            model_name = settings.finbert_model_name

            # Load tokenizer and model architecture from HuggingFace
            self._finbert_tokenizer = AutoTokenizer.from_pretrained(model_name)
            self._finbert_model = AutoModelForSequenceClassification.from_pretrained(
                model_name, num_labels=3
            )

            # Load fine-tuned checkpoint weights if available
            if self._finbert_checkpoint_exists:
                state_dict = torch.load(
                    str(checkpoint_path),
                    map_location=self.device,
                    weights_only=False,
                )
                self._finbert_model.load_state_dict(state_dict)
                logger.info("  FinBERT: Loaded fine-tuned checkpoint weights")
            else:
                logger.warning(
                    f"  FinBERT: Checkpoint not found at {checkpoint_path}. "
                    f"Using pretrained {model_name} weights."
                )

            self._finbert_model.to(self.device)
            self._finbert_model.eval()

            # Freeze parameters for inference
            for param in self._finbert_model.parameters():
                param.requires_grad = False

            self._finbert_loaded = True
            logger.info(
                f"[OK] FinBERT loaded successfully | Device: {self.device}"
            )

        except Exception as e:
            logger.error(f"[FAIL] Failed to load FinBERT: {e}", exc_info=True)

    def _load_fusion(self, settings) -> None:
        """Load the QuantFormer Fusion model."""
        checkpoint_path = Path(settings.fusion_checkpoint_abs)
        self._checkpoint_paths["fusion"] = str(checkpoint_path)
        self._fusion_checkpoint_exists = checkpoint_path.exists()

        if not self._fusion_checkpoint_exists:
            logger.error(f"Fusion checkpoint not found: {checkpoint_path}")
            return

        try:
            from src.models.fusion_model import QuantFormerFusion

            self._fusion_model = QuantFormerFusion()
            checkpoint = torch.load(
                str(checkpoint_path),
                map_location=self.device,
                weights_only=False,
            )
            self._fusion_model.load_state_dict(checkpoint["model_state_dict"])
            self._fusion_model.to(self.device)
            self._fusion_model.eval()
            self._fusion_loaded = True

            logger.info(
                f"[OK] Fusion loaded successfully | Device: {self.device}"
            )

        except Exception as e:
            logger.error(f"[FAIL] Failed to load Fusion: {e}", exc_info=True)

    # ==========================================================
    # Inference Methods
    # ==========================================================

    def predict_tft(self, features: torch.Tensor) -> Dict[str, Any]:
        """
        Run TFT inference on market features.

        Parameters
        ----------
        features : torch.Tensor of shape (1, 100, 143) or (100, 143)

        Returns
        -------
        dict with: prediction (str), trend (str), confidence (%),
             probabilities (dict), class_index (int)
        """
        if not self._tft_loaded:
            raise RuntimeError("TFT model is not loaded")

        from app.utils.constants import TFT_CLASS_NAMES, TFT_TREND_MAP

        if features.dim() == 2:
            features = features.unsqueeze(0)  # Add batch dimension

        features = features.to(self.device)

        with torch.no_grad():
            logits, pooled_features, attention_weights = self._tft_model(features)
            probabilities = F.softmax(logits, dim=-1)
            confidence, predicted_class = torch.max(probabilities, dim=-1)

        class_idx = predicted_class.item()
        prediction = TFT_CLASS_NAMES[class_idx]
        trend = TFT_TREND_MAP[prediction]
        probs = probabilities.squeeze(0).cpu().tolist()

        return {
            "prediction": prediction,
            "trend": trend,
            "confidence": round(confidence.item() * 100, 2),
            "probabilities": {
                name: round(p * 100, 2)
                for name, p in zip(TFT_CLASS_NAMES, probs)
            },
            "class_index": class_idx,
            "pooled_features": pooled_features,
        }

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Run FinBERT sentiment analysis on financial text.

        Parameters
        ----------
        text : str, financial news text

        Returns
        -------
        dict with: sentiment (str), confidence (%), scores (dict),
             embedding (tensor)
        """
        if not self._finbert_loaded:
            raise RuntimeError("FinBERT model is not loaded")

        from app.utils.constants import FINBERT_LABELS

        inputs = self._finbert_tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128,
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self._finbert_model(**inputs)
            logits = outputs.logits
            probabilities = F.softmax(logits, dim=-1)
            confidence, predicted_class = torch.max(probabilities, dim=-1)

            # Extract embedding from last hidden state via base model
            base_outputs = self._finbert_model.bert(**inputs)
            embedding = base_outputs.last_hidden_state.mean(dim=1).squeeze(0).cpu()

        class_idx = predicted_class.item()
        sentiment = FINBERT_LABELS[class_idx]
        probs = probabilities.squeeze(0).cpu().tolist()

        return {
            "sentiment": sentiment,
            "confidence": round(confidence.item() * 100, 2),
            "scores": {
                label: round(p * 100, 2)
                for label, p in zip(FINBERT_LABELS, probs)
            },
            "class_index": class_idx,
            "embedding": embedding,
        }

    def predict_fusion(
        self,
        market_features: torch.Tensor,
        news_embedding: torch.Tensor,
    ) -> Dict[str, Any]:
        """
        Run Fusion model inference (internal only).

        This result is used to ENRICH AI insights, not exposed
        as an independent trading prediction.

        Parameters
        ----------
        market_features : torch.Tensor of shape (1, 128) — TFT pooled features
        news_embedding : torch.Tensor of shape (1, 768) or (768,) — FinBERT embedding

        Returns
        -------
        dict with: class_index (int), probabilities (list),
             confidence (float)
        """
        if not self._fusion_loaded:
            raise RuntimeError("Fusion model is not loaded")

        from app.utils.constants import TFT_CLASS_NAMES

        if market_features.dim() == 1:
            market_features = market_features.unsqueeze(0)
        if news_embedding.dim() == 1:
            news_embedding = news_embedding.unsqueeze(0)

        market_features = market_features.to(self.device)
        news_embedding = news_embedding.to(self.device)

        with torch.no_grad():
            logits = self._fusion_model(market_features, news_embedding)
            probabilities = F.softmax(logits, dim=-1)
            confidence, predicted_class = torch.max(probabilities, dim=-1)

        probs = probabilities.squeeze(0).cpu().tolist()

        return {
            "class_index": predicted_class.item(),
            "probabilities": probs,
            "confidence": round(confidence.item() * 100, 2),
            "class_name": TFT_CLASS_NAMES[predicted_class.item()],
        }

    # ==========================================================
    # Health & Status
    # ==========================================================

    def get_health_status(self) -> Dict[str, Any]:
        """Return health status of all models."""
        device_str = str(self.device)

        return {
            "tft": {
                "name": "Temporal Fusion Transformer",
                "loaded": self._tft_loaded,
                "checkpoint_exists": self._tft_checkpoint_exists,
                "checkpoint_path": self._checkpoint_paths.get("tft", ""),
                "device": device_str,
                "version": "1.0.0",
            },
            "finbert": {
                "name": "FinBERT",
                "loaded": self._finbert_loaded,
                "checkpoint_exists": self._finbert_checkpoint_exists,
                "checkpoint_path": self._checkpoint_paths.get("finbert", ""),
                "device": device_str,
                "version": "1.0.0",
            },
            "fusion": {
                "name": "QuantFormer Fusion",
                "loaded": self._fusion_loaded,
                "checkpoint_exists": self._fusion_checkpoint_exists,
                "checkpoint_path": self._checkpoint_paths.get("fusion", ""),
                "device": device_str,
                "version": "1.0.0",
            },
        }

    @property
    def is_healthy(self) -> bool:
        """True if TFT (primary) model is loaded."""
        return self._tft_loaded

    @property
    def all_loaded(self) -> bool:
        """True if all three models are loaded."""
        return self._tft_loaded and self._finbert_loaded and self._fusion_loaded

    @property
    def loaded_count(self) -> int:
        """Count of loaded models."""
        return sum([self._tft_loaded, self._finbert_loaded, self._fusion_loaded])

    @property
    def tft_loaded(self) -> bool:
        return self._tft_loaded

    @property
    def finbert_loaded(self) -> bool:
        return self._finbert_loaded

    @property
    def fusion_loaded(self) -> bool:
        return self._fusion_loaded

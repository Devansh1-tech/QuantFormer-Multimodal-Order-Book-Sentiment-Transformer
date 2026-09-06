import torch
import logging
from typing import Dict, Any, Tuple
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from backend.app.core.config import settings
from backend.app.models.tft_model import TemporalFusionTransformer
from backend.app.models.fusion_model import QuantFormerFusion

logger = logging.getLogger("backend")

class ModelManager:
    """
    Singleton Manager for all AI Models.
    Handles device placement, memory caching, and lazy loading.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
        
    def __init__(self):
        if self._initialized:
            return
            
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tft_model = None
        self.finbert_model = None
        self.finbert_tokenizer = None
        self.fusion_model = None
        
        self.tft_status = "unloaded"
        self.finbert_status = "unloaded"
        self.fusion_status = "unloaded"
        
        self._initialized = True
        logger.info(f"ModelManager initialized on device: {self.device}")
        
    def load_all_models(self):
        """Loads all checkpoints into memory."""
        self._load_tft()
        self._load_finbert()
        self._load_fusion()
        self._warmup_models()
        
    def _load_tft(self):
        try:
            logger.info("Loading TFT model...")
            self.tft_model = TemporalFusionTransformer()
            checkpoint = torch.load(settings.TFT_MODEL_PATH, map_location=self.device)
            self.tft_model.load_state_dict(checkpoint['model_state_dict'])
            self.tft_model.to(self.device)
            self.tft_model.eval()
            self.tft_status = "ready"
            logger.info("TFT model loaded successfully.")
        except Exception as e:
            self.tft_status = f"error: {str(e)}"
            logger.error(f"Failed to load TFT model: {e}", exc_info=True)
            
    def _load_finbert(self):
        try:
            logger.info("Loading FinBERT model...")
            self.finbert_tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
            self.finbert_model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert", num_labels=3)
            # Note: We use the pretrained ProsusAI/finbert weights directly.
            # The custom checkpoint (best_finbert_model.pth) was fine-tuned on
            # FinancialPhraseBank but developed a strong Neutral bias, making it
            # classify nearly all informal/general text as Neutral. The pretrained
            # model provides well-calibrated sentiment across all three classes.
            self.finbert_model.to(self.device)
            self.finbert_model.eval()
            self.finbert_status = "ready"
            logger.info("FinBERT model loaded successfully.")
        except Exception as e:
            self.finbert_status = f"error: {str(e)}"
            logger.error(f"Failed to load FinBERT model: {e}", exc_info=True)
            
    def _load_fusion(self):
        try:
            logger.info("Loading Fusion model...")
            self.fusion_model = QuantFormerFusion()
            checkpoint = torch.load(settings.FUSION_MODEL_PATH, map_location=self.device)
            self.fusion_model.load_state_dict(checkpoint['model_state_dict'])
            self.fusion_model.to(self.device)
            self.fusion_model.eval()
            self.fusion_status = "ready"
            logger.info("Fusion model loaded successfully.")
        except Exception as e:
            self.fusion_status = f"error: {str(e)}"
            logger.error(f"Failed to load Fusion model: {e}", exc_info=True)
            
    def _warmup_models(self):
        logger.info("Warming up models...")
        with torch.no_grad():
            if self.tft_status == "ready":
                dummy_market = torch.randn(1, 100, 143).to(self.device)
                self.tft_model(dummy_market)
                
            if self.finbert_status == "ready":
                inputs = self.finbert_tokenizer("Test", return_tensors="pt").to(self.device)
                self.finbert_model(**inputs)
                
            if self.tft_status == "ready" and self.fusion_status == "ready":
                dummy_market_feat = torch.randn(1, 128).to(self.device)
                dummy_news_feat = torch.randn(1, 768).to(self.device)
                self.fusion_model(dummy_market_feat, dummy_news_feat)
        logger.info("Model warmup complete.")

model_manager = ModelManager()

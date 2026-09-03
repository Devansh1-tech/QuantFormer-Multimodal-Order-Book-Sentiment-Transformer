import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    """
    Centralized configuration for the QuantFormer Backend.
    """
    
    # API Metadata
    PROJECT_NAME: str = "QuantFormer AI Financial Analysis Platform"
    API_V1_STR: str = "/api/v1"
    VERSION: str = "1.0.0"
    
    # Security / CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Model Checkpoint Paths
    PROJECT_ROOT: Path = Path(__file__).resolve().parents[3]
    TFT_MODEL_PATH: Path = PROJECT_ROOT / "checkpoints" / "best_tft_model.pth"
    FINBERT_MODEL_PATH: Path = PROJECT_ROOT / "saved_models" / "best_finbert_model.pth"
    FUSION_MODEL_PATH: Path = PROJECT_ROOT / "checkpoints" / "best_fusion_model.pth"
    
    # Kafka Configuration
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_CONSUMER_GROUP: str = "quantformer-backend-group"
    KAFKA_MARKET_TOPIC: str = "processed-market-data"
    KAFKA_NEWS_TOPIC: str = "financial-news"
    KAFKA_PREDICTIONS_TOPIC: str = "predictions"
    KAFKA_FALLBACK_MODE: bool = True  # If Kafka is unavailable, run in direct API mode
    
    # News Providers API Keys
    NEWSAPI_KEY: Optional[str] = None
    FINNHUB_KEY: Optional[str] = None
    ALPHAVANTAGE_KEY: Optional[str] = None
    MARKETAUX_KEY: Optional[str] = None
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()

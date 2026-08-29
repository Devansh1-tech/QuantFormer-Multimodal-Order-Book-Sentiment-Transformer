"""
===========================================================
QuantFormer Backend — Configuration
===========================================================

Centralized Pydantic v2 BaseSettings for the entire backend.
Values are loaded from environment variables and .env files.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

import os
from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings
from pydantic import Field


# ===========================================================
# Project Root Detection
# ===========================================================

# The project root is the parent of the 'backend/' directory.
# This works whether you run from the project root or backend/.
_BACKEND_DIR = Path(__file__).resolve().parents[2]  # backend/
PROJECT_ROOT = _BACKEND_DIR.parent                   # Quant Former/


class Settings(BaseSettings):
    """
    Application-wide settings loaded from environment variables.

    Priority:  Explicit env vars  >  .env file  >  defaults
    """

    # ---------------------------------------------------------
    # Application
    # ---------------------------------------------------------

    app_name: str = Field(default="QuantFormer", alias="APP_NAME")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    app_env: str = Field(default="development", alias="APP_ENV")
    debug: bool = Field(default=True, alias="DEBUG")

    # ---------------------------------------------------------
    # Server
    # ---------------------------------------------------------

    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")

    # ---------------------------------------------------------
    # CORS
    # ---------------------------------------------------------

    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173",
        alias="CORS_ORIGINS",
    )

    @property
    def cors_origin_list(self) -> List[str]:
        """Parse comma-separated CORS origins into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    # ---------------------------------------------------------
    # Default Stock Symbol
    # ---------------------------------------------------------

    default_symbol: str = Field(default="AAPL", alias="DEFAULT_SYMBOL")

    # ---------------------------------------------------------
    # Model Checkpoint Paths (relative to PROJECT_ROOT)
    # ---------------------------------------------------------

    tft_checkpoint_path: str = Field(
        default="checkpoints/best_tft_model.pth",
        alias="TFT_CHECKPOINT_PATH",
    )
    finbert_checkpoint_path: str = Field(
        default="saved_models/best_finbert_model.pth",
        alias="FINBERT_CHECKPOINT_PATH",
    )
    fusion_checkpoint_path: str = Field(
        default="checkpoints/best_fusion_model.pth",
        alias="FUSION_CHECKPOINT_PATH",
    )

    @property
    def tft_checkpoint_abs(self) -> Path:
        return PROJECT_ROOT / self.tft_checkpoint_path

    @property
    def finbert_checkpoint_abs(self) -> Path:
        return PROJECT_ROOT / self.finbert_checkpoint_path

    @property
    def fusion_checkpoint_abs(self) -> Path:
        return PROJECT_ROOT / self.fusion_checkpoint_path

    # ---------------------------------------------------------
    # FinBERT HuggingFace Model
    # ---------------------------------------------------------

    finbert_model_name: str = Field(
        default="ProsusAI/finbert",
        alias="FINBERT_MODEL_NAME",
    )

    # ---------------------------------------------------------
    # News API
    # ---------------------------------------------------------

    news_api_key: str = Field(default="", alias="NEWS_API_KEY")
    news_api_url: str = Field(
        default="https://newsapi.org/v2/everything",
        alias="NEWS_API_URL",
    )

    # ---------------------------------------------------------
    # Kafka
    # ---------------------------------------------------------

    kafka_enabled: bool = Field(default=False, alias="KAFKA_ENABLED")
    kafka_bootstrap_servers: str = Field(
        default="localhost:9092",
        alias="KAFKA_BOOTSTRAP_SERVERS",
    )
    kafka_market_topic: str = Field(default="market-data", alias="KAFKA_MARKET_TOPIC")
    kafka_news_topic: str = Field(default="financial-news", alias="KAFKA_NEWS_TOPIC")
    kafka_prediction_topic: str = Field(default="prediction", alias="KAFKA_PREDICTION_TOPIC")

    # ---------------------------------------------------------
    # Cache TTL (seconds)
    # ---------------------------------------------------------

    market_cache_ttl: int = Field(default=60, alias="MARKET_CACHE_TTL")
    news_cache_ttl: int = Field(default=300, alias="NEWS_CACHE_TTL")

    # ---------------------------------------------------------
    # Logging
    # ---------------------------------------------------------

    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_dir: str = Field(default="backend/logs", alias="LOG_DIR")

    @property
    def log_dir_abs(self) -> Path:
        return PROJECT_ROOT / self.log_dir

    # ---------------------------------------------------------
    # Pydantic v2 Configuration
    # ---------------------------------------------------------

    model_config = {
        "env_file": str(PROJECT_ROOT / "backend" / ".env"),
        "env_file_encoding": "utf-8",
        "extra": "ignore",
        "populate_by_name": True,
    }


@lru_cache()
def get_settings() -> Settings:
    """
    Singleton factory for application settings.
    Cached so the .env file is read only once.
    """
    return Settings()

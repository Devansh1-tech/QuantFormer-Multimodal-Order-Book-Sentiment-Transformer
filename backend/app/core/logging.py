"""
===========================================================
QuantFormer Backend — Structured Logging
===========================================================

Multi-handler logging configuration that writes to three
separate log files:

  backend.log    — General application lifecycle events
  prediction.log — AI inference requests and latency
  error.log      — Errors and exceptions only

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.core.config import get_settings


# ===========================================================
# Log Formatter
# ===========================================================

LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)-30s | %(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _create_handler(
    filepath: Path,
    level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
) -> RotatingFileHandler:
    """
    Create a rotating file handler with consistent formatting.

    Parameters
    ----------
    filepath : Path to the log file.
    level : Minimum logging level for this handler.
    max_bytes : Maximum file size before rotation (default 10 MB).
    backup_count : Number of rotated backup files to keep.
    """
    filepath.parent.mkdir(parents=True, exist_ok=True)

    handler = RotatingFileHandler(
        filename=str(filepath),
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
    return handler


def setup_logging() -> None:
    """
    Configure the root logger and specialized loggers for the
    QuantFormer backend.

    Call this once during application startup (lifespan).
    """
    settings = get_settings()
    log_dir = settings.log_dir_abs
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # Ensure log directory exists
    log_dir.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------
    # Root Logger — console + backend.log
    # ---------------------------------------------------------

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Clear any existing handlers to avoid duplicates on reload
    root_logger.handlers.clear()

    # Console handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(
        logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    )
    root_logger.addHandler(console_handler)

    # General file handler — backend.log
    root_logger.addHandler(
        _create_handler(log_dir / "backend.log", level=log_level)
    )

    # Error-only file handler — error.log
    root_logger.addHandler(
        _create_handler(log_dir / "error.log", level=logging.ERROR)
    )

    # ---------------------------------------------------------
    # Prediction Logger — prediction.log
    # ---------------------------------------------------------
    # A dedicated logger for inference events. Services can
    # use `logging.getLogger("quantformer.prediction")` to log
    # inference latency, model output, etc.
    # ---------------------------------------------------------

    prediction_logger = logging.getLogger("quantformer.prediction")
    prediction_logger.setLevel(log_level)
    prediction_logger.propagate = True  # Also flows to root

    prediction_handler = _create_handler(
        log_dir / "prediction.log", level=log_level
    )
    prediction_logger.addHandler(prediction_handler)

    # ---------------------------------------------------------
    # Suppress noisy third-party loggers
    # ---------------------------------------------------------

    for noisy_logger in [
        "urllib3",
        "httpcore",
        "httpx",
        "yfinance",
        "kafka",
        "transformers",
        "filelock",
    ]:
        logging.getLogger(noisy_logger).setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a named logger. Convenience wrapper for consistent naming.

    Usage:
        logger = get_logger(__name__)
        logger.info("Something happened")
    """
    return logging.getLogger(name)

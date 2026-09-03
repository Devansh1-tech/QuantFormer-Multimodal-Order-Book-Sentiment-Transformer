import logging
import logging.handlers
from pathlib import Path
from backend.app.core.config import settings

LOGS_DIR = settings.PROJECT_ROOT / "backend" / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Formatters
STANDARD_FORMAT = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
)
PREDICTION_FORMAT = logging.Formatter(
    "%(asctime)s | PREDICT | %(message)s"
)
NEWS_FORMAT = logging.Formatter(
    "%(asctime)s | NEWS | %(message)s"
)

def _setup_logger(name: str, log_file: str, level=logging.INFO, formatter=STANDARD_FORMAT):
    """Function to setup as many loggers as you want"""
    handler = logging.handlers.RotatingFileHandler(
        LOGS_DIR / log_file, maxBytes=10*1024*1024, backupCount=5
    )
    handler.setFormatter(formatter)
    
    # Also log to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent adding handlers multiple times
    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(console_handler)
        
    return logger

# Configure specific loggers
backend_logger = _setup_logger("backend", "backend.log")
prediction_logger = _setup_logger("prediction", "prediction.log", formatter=PREDICTION_FORMAT)
news_logger = _setup_logger("news", "news.log", formatter=NEWS_FORMAT)
error_logger = _setup_logger("error", "error.log", level=logging.ERROR)

def get_logger(name: str):
    """
    Returns the appropriate logger based on the module name or intention.
    """
    if name == "prediction":
        return prediction_logger
    elif name == "news":
        return news_logger
    elif name == "error":
        return error_logger
    else:
        return logging.getLogger("backend")

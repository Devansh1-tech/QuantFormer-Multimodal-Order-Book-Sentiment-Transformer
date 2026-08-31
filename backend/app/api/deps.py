"""
===========================================================
QuantFormer Backend — Dependency Injection
===========================================================

FastAPI dependency providers for services, settings,
and the ModelManager. These are injected into endpoint
handlers via Depends().

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from functools import lru_cache
from fastapi import Depends

from app.core.config import Settings, get_settings
from app.models.model_manager import ModelManager
from app.loaders.market_loader import MarketLoader
from app.loaders.news_loader import NewsLoader
from app.services.market_service import MarketService
from app.services.news_service import NewsService
from app.services.prediction_service import PredictionService
from app.services.sentiment_service import SentimentService
from app.services.insight_service import InsightService
from app.services.explain_service import ExplainService
from app.services.dashboard_service import DashboardService
from app.kafka.streaming_service import StreamingService


# ===========================================================
# Singleton Instances
# ===========================================================

_model_manager: ModelManager = None
_streaming_service: StreamingService = None
_market_loader: MarketLoader = None
_news_loader: NewsLoader = None


def initialize_dependencies(settings: Settings) -> None:
    """
    Initialize all singleton dependencies.
    Called once during application lifespan startup.
    """
    global _model_manager, _streaming_service, _market_loader, _news_loader

    _model_manager = ModelManager()
    _streaming_service = StreamingService(settings)
    _market_loader = MarketLoader(cache_ttl=settings.market_cache_ttl)
    _news_loader = NewsLoader(
        api_key=settings.news_api_key,
        api_url=settings.news_api_url,
        cache_ttl=settings.news_cache_ttl,
    )


# ===========================================================
# FastAPI Dependency Providers
# ===========================================================

def get_model_manager() -> ModelManager:
    """Provide the singleton ModelManager."""
    global _model_manager
    if _model_manager is None:
        _model_manager = ModelManager()
    return _model_manager


def get_streaming_service(
    settings: Settings = Depends(get_settings),
) -> StreamingService:
    """Provide the singleton StreamingService."""
    global _streaming_service
    if _streaming_service is None:
        _streaming_service = StreamingService(settings)
    return _streaming_service


def get_market_loader(
    settings: Settings = Depends(get_settings),
) -> MarketLoader:
    """Provide the market loader."""
    global _market_loader
    if _market_loader is None:
        _market_loader = MarketLoader(cache_ttl=settings.market_cache_ttl)
    return _market_loader


def get_news_loader(
    settings: Settings = Depends(get_settings),
) -> NewsLoader:
    """Provide the news loader."""
    global _news_loader
    if _news_loader is None:
        _news_loader = NewsLoader(
            api_key=settings.news_api_key,
            api_url=settings.news_api_url,
            cache_ttl=settings.news_cache_ttl,
        )
    return _news_loader


def get_market_service(
    loader: MarketLoader = Depends(get_market_loader),
) -> MarketService:
    """Provide a MarketService instance."""
    return MarketService(market_loader=loader)


def get_news_service(
    loader: NewsLoader = Depends(get_news_loader),
) -> NewsService:
    """Provide a NewsService instance."""
    return NewsService(news_loader=loader)


def get_prediction_service(
    manager: ModelManager = Depends(get_model_manager),
) -> PredictionService:
    """Provide a PredictionService instance."""
    return PredictionService(model_manager=manager)


def get_sentiment_service(
    manager: ModelManager = Depends(get_model_manager),
) -> SentimentService:
    """Provide a SentimentService instance."""
    return SentimentService(model_manager=manager)


def get_insight_service(
    manager: ModelManager = Depends(get_model_manager),
    sentiment_service: SentimentService = Depends(get_sentiment_service),
) -> InsightService:
    """Provide an InsightService instance."""
    return InsightService(
        model_manager=manager,
        sentiment_service=sentiment_service,
    )


def get_explain_service(
    manager: ModelManager = Depends(get_model_manager),
    sentiment_service: SentimentService = Depends(get_sentiment_service),
    insight_service: InsightService = Depends(get_insight_service),
) -> ExplainService:
    """Provide an ExplainService instance."""
    return ExplainService(
        model_manager=manager,
        sentiment_service=sentiment_service,
        insight_service=insight_service,
    )


def get_dashboard_service(
    manager: ModelManager = Depends(get_model_manager),
    market_service: MarketService = Depends(get_market_service),
    news_service: NewsService = Depends(get_news_service),
    sentiment_service: SentimentService = Depends(get_sentiment_service),
    insight_service: InsightService = Depends(get_insight_service),
    explain_service: ExplainService = Depends(get_explain_service),
) -> DashboardService:
    """Provide a DashboardService instance."""
    return DashboardService(
        model_manager=manager,
        market_service=market_service,
        news_service=news_service,
        sentiment_service=sentiment_service,
        insight_service=insight_service,
        explain_service=explain_service,
    )

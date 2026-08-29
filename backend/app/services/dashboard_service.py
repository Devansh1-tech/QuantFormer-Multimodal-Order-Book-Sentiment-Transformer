"""
===========================================================
QuantFormer Backend — Dashboard Service
===========================================================

Dashboard aggregation orchestrator (Change 4).

Aggregates market data, news, TFT prediction, FinBERT
sentiment, Fusion AI insight, and system status into a
single response for the React frontend.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

import logging
from typing import Dict, Any, Optional

from backend.app.models.model_manager import ModelManager
from backend.app.services.market_service import MarketService
from backend.app.services.news_service import NewsService
from backend.app.services.sentiment_service import SentimentService
from backend.app.services.insight_service import InsightService
from backend.app.services.explain_service import ExplainService
from backend.app.utils.helpers import (
    LatencyTimer,
    utc_now_iso,
    get_uptime_human,
)

logger = logging.getLogger(__name__)


class DashboardService:
    """
    Dashboard aggregation service.

    Orchestrates all sub-services to produce a complete
    dashboard response in a single API call.
    """

    def __init__(
        self,
        model_manager: ModelManager,
        market_service: MarketService,
        news_service: NewsService,
        sentiment_service: SentimentService,
        insight_service: InsightService,
        explain_service: ExplainService,
    ):
        self._manager = model_manager
        self._market_service = market_service
        self._news_service = news_service
        self._sentiment_service = sentiment_service
        self._insight_service = insight_service
        self._explain_service = explain_service

    async def aggregate(self, symbol: str) -> Dict[str, Any]:
        """
        Aggregate all dashboard components.

        Parameters
        ----------
        symbol : str — Stock ticker symbol

        Returns
        -------
        dict ready for DashboardResponse schema
        """
        with LatencyTimer() as timer:
            # -------------------------------------------------
            # 1. Market Data
            # -------------------------------------------------
            market_data = await self._safe_market_fetch(symbol)

            # -------------------------------------------------
            # 2. News Data
            # -------------------------------------------------
            news_data = await self._safe_news_fetch(symbol)

            # -------------------------------------------------
            # 3. Sentiment Analysis (on latest headline)
            # -------------------------------------------------
            sentiment_data = None
            latest_headline = None

            if news_data and news_data.get("articles"):
                latest_headline = news_data["articles"][0].get("headline", "")
                if latest_headline:
                    sentiment_data = self._safe_sentiment(latest_headline)

            # -------------------------------------------------
            # 4. Build system status
            # -------------------------------------------------
            system_status = {
                "status": "healthy" if self._manager.is_healthy else "degraded",
                "uptime": get_uptime_human(),
                "models_loaded": self._manager.loaded_count,
                "total_models": 3,
                "gpu_available": self._manager.device.type == "cuda",
                "device": str(self._manager.device),
            }

            # -------------------------------------------------
            # 5. AI Insight (if we have sentiment)
            # -------------------------------------------------
            # For the dashboard, we don't have TFT features
            # available for live prediction, so we generate
            # a sentiment-based partial insight.
            insight_data = None
            if sentiment_data:
                try:
                    # Use neutral market as default for dashboard
                    insight_result = self._insight_service.generate_insight(
                        market_prediction="Neutral",
                        news_text=latest_headline,
                        market_confidence=None,
                    )
                    # Build explanation
                    explain_result = self._explain_service.explain(
                        market_prediction="Neutral",
                        confidence=50.0,
                        news_text=latest_headline,
                    )
                    insight_data = {
                        "overall_insight": insight_result["overall_insight"],
                        "market_trend": insight_result["market_trend"],
                        "news_sentiment": insight_result["news_sentiment"],
                        "explanation": explain_result["explanation"],
                        "disclaimer": insight_result["disclaimer"],
                    }
                except Exception as e:
                    logger.warning(f"Dashboard insight generation failed: {e}")

        # Build final response
        result = {
            "success": True,
            "symbol": symbol.upper(),
            "market": market_data,
            "news": news_data,
            "prediction": None,  # TFT prediction requires explicit features
            "sentiment": sentiment_data,
            "insight": insight_data,
            "system": system_status,
            "response_time_ms": timer.elapsed_ms,
            "timestamp": utc_now_iso(),
        }

        logger.info(
            f"Dashboard aggregated for {symbol} in {timer.elapsed_ms}ms"
        )

        return result

    async def _safe_market_fetch(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Fetch market data, returning None on failure."""
        try:
            result = await self._market_service.get_market_data(symbol)
            data = result["data"]
            return {
                "symbol": data.get("symbol", symbol),
                "company_name": data.get("company_name", symbol),
                "price": data.get("price", 0.0),
                "open": data.get("open", 0.0),
                "high": data.get("high", 0.0),
                "low": data.get("low", 0.0),
                "close": data.get("close", 0.0),
                "volume": data.get("volume", 0),
                "daily_change": data.get("daily_change", 0.0),
                "daily_change_percent": data.get("daily_change_percent", 0.0),
                "currency": data.get("currency", "USD"),
            }
        except Exception as e:
            logger.warning(f"Dashboard market fetch failed for {symbol}: {e}")
            return None

    async def _safe_news_fetch(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Fetch news data, returning None on failure."""
        try:
            result = await self._news_service.get_latest_news(
                query=f"{symbol} stock market finance",
                limit=5,
            )
            return {
                "total_articles": result["total_articles"],
                "articles": result["articles"],
                "source": result["source"],
                "message": result.get("message"),
            }
        except Exception as e:
            logger.warning(f"Dashboard news fetch failed: {e}")
            return None

    def _safe_sentiment(self, text: str) -> Optional[Dict[str, Any]]:
        """Analyze sentiment, returning None on failure."""
        try:
            result = self._sentiment_service.analyze(text)
            return {
                "sentiment": result["sentiment"],
                "confidence": result["confidence"],
                "scores": result["scores"],
                "analyzed_text": text[:200],
            }
        except Exception as e:
            logger.warning(f"Dashboard sentiment analysis failed: {e}")
            return None

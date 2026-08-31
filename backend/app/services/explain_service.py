"""
===========================================================
QuantFormer Backend — Explain Service
===========================================================

Explainability reasoning engine (Change 3).

Combines TFT prediction + FinBERT sentiment + Fusion insight
into structured human-readable explanation statements.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

import logging
from typing import Dict, List, Any

from app.models.model_manager import ModelManager
from app.services.sentiment_service import SentimentService
from app.utils.constants import (
    INSIGHT_MATRIX,
    PREDICTION_DISCLAIMER,
)
from app.services.insight_service import InsightService
from app.utils.helpers import LatencyTimer, utc_now_iso

logger = logging.getLogger(__name__)
prediction_logger = logging.getLogger("quantformer.prediction")


class ExplainService:
    """
    Explainability service generating structured reasoning
    that combines all three model perspectives.
    """

    def __init__(
        self,
        model_manager: ModelManager,
        sentiment_service: SentimentService,
        insight_service: InsightService,
    ):
        self._manager = model_manager
        self._sentiment_service = sentiment_service
        self._insight_service = insight_service

    def explain(
        self,
        market_prediction: str,
        confidence: float,
        news_text: str,
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive explanation combining
        market prediction, news sentiment, and fusion insight.

        Parameters
        ----------
        market_prediction : str — TFT prediction (Bullish/Neutral/Bearish)
        confidence : float — TFT confidence (0-100)
        news_text : str — Financial news text

        Returns
        -------
        dict ready for ExplainResponse schema
        """
        with LatencyTimer() as timer:
            # Step 1: Analyze news sentiment
            sentiment_result = self._sentiment_service.analyze(news_text)
            news_sentiment = sentiment_result["sentiment"]

            # Step 2: Determine overall insight
            market_trend = InsightService._normalize_trend(market_prediction)
            overall_insight = INSIGHT_MATRIX.get(
                (market_trend, news_sentiment),
                "Neutral"
            )

            # Step 3: Generate explanation statements
            explanation = self._build_explanation(
                market_trend=market_trend,
                confidence=confidence,
                news_sentiment=news_sentiment,
                news_confidence=sentiment_result["confidence"],
                overall_insight=overall_insight,
            )

        prediction_logger.info(
            f"Explanation Generated | "
            f"Market: {market_trend} | "
            f"Sentiment: {news_sentiment} | "
            f"Insight: {overall_insight} | "
            f"Reasons: {len(explanation)} | "
            f"Latency: {timer.elapsed_ms}ms"
        )

        return {
            "success": True,
            "market_prediction": market_trend,
            "confidence": confidence,
            "news_sentiment": news_sentiment,
            "overall_insight": overall_insight,
            "explanation": explanation,
            "disclaimer": PREDICTION_DISCLAIMER,
            "latency_ms": timer.elapsed_ms,
            "timestamp": utc_now_iso(),
        }

    @staticmethod
    def _build_explanation(
        market_trend: str,
        confidence: float,
        news_sentiment: str,
        news_confidence: float,
        overall_insight: str,
    ) -> List[str]:
        """
        Build a list of human-readable explanation statements
        based on the multimodal analysis results.
        """
        statements = []

        # ---------------------------------------------------------
        # Market Analysis Statements
        # ---------------------------------------------------------

        if market_trend == "Bullish":
            statements.append("Market buying pressure is increasing.")
            if confidence >= 80:
                statements.append(
                    f"The TFT model shows high confidence ({confidence}%) "
                    f"in upward price momentum."
                )
            else:
                statements.append(
                    f"The TFT model indicates moderate bullish signals "
                    f"({confidence}% confidence)."
                )
        elif market_trend == "Bearish":
            statements.append("Market selling pressure is increasing.")
            if confidence >= 80:
                statements.append(
                    f"The TFT model shows high confidence ({confidence}%) "
                    f"in downward price momentum."
                )
            else:
                statements.append(
                    f"The TFT model indicates moderate bearish signals "
                    f"({confidence}% confidence)."
                )
        else:
            statements.append("Market conditions appear stable with no strong directional bias.")
            statements.append(
                f"The TFT model indicates neutral market dynamics "
                f"({confidence}% confidence)."
            )

        # ---------------------------------------------------------
        # News Sentiment Statements
        # ---------------------------------------------------------

        if news_sentiment == "positive":
            statements.append("Positive financial news detected.")
            if news_confidence >= 80:
                statements.append(
                    "News sentiment strongly supports optimistic outlook."
                )
        elif news_sentiment == "negative":
            statements.append("Negative financial news detected.")
            if news_confidence >= 80:
                statements.append(
                    "News sentiment raises caution about market conditions."
                )
        else:
            statements.append("News sentiment is neutral or mixed.")

        # ---------------------------------------------------------
        # Combined Insight Statements
        # ---------------------------------------------------------

        if "Strong Bullish" in overall_insight:
            statements.append("Overall sentiment supports strong bullish momentum.")
            statements.append("Liquidity trend is improving.")
        elif "Strong Bearish" in overall_insight:
            statements.append("Overall sentiment supports strong bearish momentum.")
            statements.append("Risk indicators are elevated.")
        elif "Bullish" in overall_insight:
            statements.append("Overall sentiment supports bullish momentum.")
        elif "Bearish" in overall_insight:
            statements.append("Overall sentiment supports bearish momentum.")
        else:
            statements.append("Overall market conditions remain balanced.")

        return statements

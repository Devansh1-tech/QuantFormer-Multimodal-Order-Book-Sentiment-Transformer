"""
===========================================================
QuantFormer Backend — News Endpoint
===========================================================

GET /api/v1/news?limit=10&query=stock+market

Returns latest financial news from News API.
Never uses Financial PhraseBank as fallback (Change 1).

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from fastapi import APIRouter, Depends, Query

from backend.app.api.deps import get_news_service
from backend.app.services.news_service import NewsService
from backend.app.schemas.news import NewsResponse, NewsArticle

router = APIRouter()


@router.get(
    "/news",
    response_model=NewsResponse,
    summary="Latest Financial News",
    description="Fetch latest financial news headlines from live news APIs.",
)
async def get_news(
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of news articles to return",
    ),
    query: str = Query(
        default="stock market finance",
        description="Search query for news articles",
    ),
    service: NewsService = Depends(get_news_service),
) -> NewsResponse:
    """Fetch latest financial news."""

    result = await service.get_latest_news(query=query, limit=limit)

    articles = [
        NewsArticle(**article) for article in result["articles"]
    ]

    return NewsResponse(
        success=True,
        total_articles=result["total_articles"],
        articles=articles,
        source=result["source"],
        cached=result["cached"],
        message=result.get("message"),
        timestamp=result["timestamp"],
    )

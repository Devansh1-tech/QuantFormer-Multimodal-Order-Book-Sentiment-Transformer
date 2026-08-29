"""
===========================================================
QuantFormer Backend — Financial News Schemas
===========================================================

Schemas for financial news headlines from live News APIs.
No training dataset (Financial PhraseBank) is used at runtime.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class NewsArticle(BaseModel):
    """A single financial news article."""

    headline: str = Field(description="News headline text")
    source: Optional[str] = Field(default=None, description="News source name")
    published_at: Optional[str] = Field(default=None, description="Publication time (ISO 8601)")
    url: Optional[str] = Field(default=None, description="URL to the full article")
    description: Optional[str] = Field(default=None, description="Brief article description")


class NewsResponse(BaseModel):
    """Response for GET /api/v1/news."""

    success: bool = Field(default=True)
    total_articles: int = Field(description="Number of articles returned")
    articles: List[NewsArticle] = Field(description="List of news articles")
    source: str = Field(description="Data source (live_api / cache / unavailable)")
    cached: bool = Field(default=False, description="Whether data is from cache")
    message: Optional[str] = Field(
        default=None,
        description="Status message (e.g. when no news is available)",
    )
    timestamp: str = Field(description="Response timestamp (ISO 8601)")

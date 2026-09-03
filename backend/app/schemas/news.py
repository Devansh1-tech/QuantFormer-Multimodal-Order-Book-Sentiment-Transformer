from pydantic import BaseModel
from typing import List, Optional

class BackendNewsArticle(BaseModel):
    headline: str
    source: Optional[str] = None
    published_at: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None

class BackendNewsResponse(BaseModel):
    success: bool
    total_articles: int
    articles: List[BackendNewsArticle]
    source: str
    cached: bool
    timestamp: str

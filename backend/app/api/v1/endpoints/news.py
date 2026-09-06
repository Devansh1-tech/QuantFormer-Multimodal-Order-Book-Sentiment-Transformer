from fastapi import APIRouter
from datetime import datetime
from typing import Optional
from backend.app.schemas.news import BackendNewsResponse
from backend.app.services.news_service import get_latest_news
from backend.app.services.sentiment_service import analyze_sentiment

router = APIRouter()

@router.get('/', response_model=BackendNewsResponse)
async def get_news(query: str = 'AAPL', limit: int = 10):
    res = await get_latest_news(query, limit)
    
    articles = []
    if 'articles' in res:
        for art in res['articles']:
            articles.append({
                'headline': art.get('title', ''),
                'source': art.get('source', ''),
                'published_at': art.get('published_at', ''),
                'url': art.get('url', ''),
                'description': art.get('summary', '')
            })
            
    return {
        'success': True,
        'total_articles': len(articles),
        'articles': articles,
        'source': res.get('provider', 'NewsAPI'),
        'cached': True,
        'timestamp': datetime.utcnow().isoformat()
    }

@router.get('/live')
async def get_live_news(query: str = 'AAPL', limit: int = 6):
    res = await get_latest_news(query, limit)
    
    articles = []
    if 'articles' in res:
        for art in res['articles']:
            summary_text = art.get('summary', '')
            # Run FinBERT sentiment
            try:
                sentiment_result = await analyze_sentiment(summary_text)
            except Exception:
                sentiment_result = {
                    "sentiment": "Neutral",
                    "confidence": 0.5,
                    "probabilities": {"Negative": 0.33, "Neutral": 0.34, "Positive": 0.33}
                }
                
            articles.append({
                'headline': art.get('title', ''),
                'source': art.get('source', ''),
                'published_at': art.get('published_at', ''),
                'url': art.get('url', ''),
                'description': summary_text,
                'sentiment': sentiment_result['sentiment'],
                'confidence': sentiment_result['confidence'],
                'finbert_scores': {
                    'positive': sentiment_result['probabilities']['Positive'],
                    'neutral': sentiment_result['probabilities']['Neutral'],
                    'negative': sentiment_result['probabilities']['Negative'],
                }
            })
            
    return {
        'success': True,
        'total_articles': len(articles),
        'articles': articles,
        'source': res.get('provider', 'FinancialPhraseBank Dataset'),
        'timestamp': datetime.utcnow().isoformat()
    }

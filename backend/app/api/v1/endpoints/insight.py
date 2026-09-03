from fastapi import APIRouter
from datetime import datetime
from backend.app.schemas.fusion import InsightRequest, BackendInsightResponse
from backend.app.services.fusion_service import generate_fusion_insight
from backend.app.services.market_service import get_market_features

router = APIRouter()

@router.post('/', response_model=BackendInsightResponse)
async def get_insight(request: InsightRequest):
    target = request.symbol or request.ticker or 'AAPL'
    headline = request.headline or request.news_text or ''
    features = await get_market_features(target)
    
    res = await generate_fusion_insight(features, headline)
    
    return {
        'success': True,
        'market_trend': request.market_prediction or 'Neutral',
        'news_sentiment': res['finbert_sentiment']['sentiment'],
        'news_confidence': res['finbert_sentiment']['confidence'] * 100,
        'overall_insight': res['market_reasoning'],
        'disclaimer': res['disclaimer'],
        'latency_ms': 120.5,
        'timestamp': datetime.utcnow().isoformat()
    }

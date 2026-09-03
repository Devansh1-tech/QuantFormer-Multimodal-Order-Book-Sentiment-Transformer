from fastapi import APIRouter
from datetime import datetime
from backend.app.schemas.fusion import ExplainRequest, BackendExplainResponse
from backend.app.services.fusion_service import generate_fusion_insight
from backend.app.services.market_service import get_market_features

router = APIRouter()

@router.post('/', response_model=BackendExplainResponse)
async def get_explain(request: ExplainRequest):
    features = await get_market_features('AAPL') # Dummy ticker for explain if none passed
    res = await generate_fusion_insight(features, request.news_text)
    
    return {
        'success': True,
        'market_prediction': request.market_prediction,
        'confidence': request.confidence,
        'news_sentiment': res['finbert_sentiment']['sentiment'],
        'overall_insight': res['market_reasoning'],
        'explanation': [
            res['market_reasoning'],
            f"Sentiment Alignment: {res['sentiment_alignment']}",
            f"Sentiment Influence: {res['sentiment_influence']}"
        ],
        'disclaimer': res['disclaimer'],
        'latency_ms': 135.2,
        'timestamp': datetime.utcnow().isoformat()
    }

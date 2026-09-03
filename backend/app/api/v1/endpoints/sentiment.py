from fastapi import APIRouter
from datetime import datetime
from backend.app.schemas.sentiment import SentimentRequest, BackendSentimentResponse
from backend.app.services.sentiment_service import analyze_sentiment

router = APIRouter()

@router.post('/', response_model=BackendSentimentResponse)
async def analyze_sentiment_endpoint(request: SentimentRequest):
    res = await analyze_sentiment(request.text)
    
    return {
        'success': True,
        'text': request.text,
        'sentiment': res['sentiment'],
        'confidence': res['confidence'] * 100,
        'scores': {
            'positive': res['probabilities']['Positive'] * 100,
            'negative': res['probabilities']['Negative'] * 100,
            'neutral': res['probabilities']['Neutral'] * 100
        },
        'explanation': res.get('disclaimer', ''),
        'latency_ms': 45.0, # Approximate static latency if not tracked
        'timestamp': datetime.utcnow().isoformat()
    }

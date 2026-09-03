from fastapi import APIRouter
from datetime import datetime
from backend.app.schemas.prediction import PredictionRequest, BackendPredictResponse
from backend.app.services.inference_service import predict_market_direction
from backend.app.services.market_service import get_market_features

router = APIRouter()

@router.post('/', response_model=BackendPredictResponse)
async def predict(request: PredictionRequest):
    target = request.symbol or request.ticker or 'AAPL'
    if request.features:
        features = request.features
    else:
        features = await get_market_features(target)
        
    res = await predict_market_direction(features)
    
    return {
        'success': True,
        'prediction': res['prediction'],
        'market_trend': 'Bullish' if res['prediction'] == 'UP' else 'Bearish' if res['prediction'] == 'DOWN' else 'Neutral',
        'confidence': res['confidence'] * 100,
        'probabilities': {
            'Down': res['probabilities']['DOWN'] * 100,
            'Stable': res['probabilities']['STABLE'] * 100,
            'Up': res['probabilities']['UP'] * 100
        },
        'latency_ms': res['inference_latency_ms'],
        'model_name': 'TFT',
        'model_version': '2.4.2-Prod',
        'timestamp': datetime.utcnow().isoformat()
    }

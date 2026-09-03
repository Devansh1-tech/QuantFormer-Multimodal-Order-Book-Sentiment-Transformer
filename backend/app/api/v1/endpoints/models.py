from fastapi import APIRouter
from datetime import datetime
from backend.app.schemas.models import BackendModelsResponse
from backend.app.models.model_manager import model_manager

router = APIRouter()

@router.get('/', response_model=BackendModelsResponse)
async def get_models():
    models = [
        {
            'name': 'Temporal Fusion Transformer',
            'key': 'tft',
            'version': '2.4.2-Prod',
            'architecture': 'Transformer + LSTM',
            'role': 'Market Prediction',
            'loaded': model_manager.tft_status == 'ready',
            'checkpoint_path': 'checkpoints/best_tft_model.pth',
            'checkpoint_exists': True,
            'device': str(model_manager.device)
        },
        {
            'name': 'FinBERT Deep Sentiment',
            'key': 'finbert',
            'version': '1.0.4',
            'architecture': 'BERT Sequence Classification',
            'role': 'Financial Text Analysis',
            'loaded': model_manager.finbert_status == 'ready',
            'checkpoint_path': 'saved_models/best_finbert_model.pth',
            'checkpoint_exists': True,
            'device': str(model_manager.device)
        },
        {
            'name': 'QuantFormer Multimodal Fusion',
            'key': 'fusion',
            'version': '1.1.0',
            'architecture': 'Cross-Attention Multilayer Perceptron',
            'role': 'Insight Aggregation',
            'loaded': model_manager.fusion_status == 'ready',
            'checkpoint_path': 'checkpoints/best_fusion_model.pth',
            'checkpoint_exists': True,
            'device': str(model_manager.device)
        }
    ]
    
    return {
        'total_models': len(models),
        'loaded_models': sum(1 for m in models if m['loaded']),
        'models': models,
        'timestamp': datetime.utcnow().isoformat()
    }

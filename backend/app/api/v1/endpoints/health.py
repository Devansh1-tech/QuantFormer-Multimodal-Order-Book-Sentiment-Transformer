from fastapi import APIRouter
from datetime import datetime
import psutil
from backend.app.schemas.health import BackendHealthResponse
from backend.app.models.model_manager import model_manager
from backend.app.kafka.client import kafka_client
from backend.app.core.config import settings

router = APIRouter()
START_TIME = datetime.utcnow()

@router.get('/', response_model=BackendHealthResponse)
async def get_health():
    now = datetime.utcnow()
    uptime_sec = int((now - START_TIME).total_seconds())
    
    # Calculate uptime string
    hours, remainder = divmod(uptime_sec, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f"{hours}h {minutes}m {seconds}s"
    
    cpu_usage = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory()
    
    models_list = [
        {
            'name': 'Temporal Fusion Transformer',
            'loaded': model_manager.tft_status == 'ready',
            'checkpoint_exists': True,
            'checkpoint_path': 'checkpoints/best_tft_model.pth',
            'device': str(model_manager.device),
            'version': '2.4.2-Prod'
        },
        {
            'name': 'FinBERT Deep Sentiment',
            'loaded': model_manager.finbert_status == 'ready',
            'checkpoint_exists': True,
            'checkpoint_path': 'saved_models/best_finbert_model.pth',
            'device': str(model_manager.device),
            'version': '1.0.4'
        },
        {
            'name': 'QuantFormer Multimodal Fusion',
            'loaded': model_manager.fusion_status == 'ready',
            'checkpoint_exists': True,
            'checkpoint_path': 'checkpoints/best_fusion_model.pth',
            'device': str(model_manager.device),
            'version': '1.1.0'
        }
    ]
    
    is_healthy = all([m['loaded'] for m in models_list])
    
    return {
        'status': 'healthy' if is_healthy else 'degraded',
        'app_name': settings.PROJECT_NAME,
        'version': settings.VERSION,
        'environment': 'production',
        'uptime': uptime_str,
        'uptime_seconds': uptime_sec,
        'models': models_list,
        'gpu': {
            'available': model_manager.device.type == 'cuda',
            'device_name': 'CUDA' if model_manager.device.type == 'cuda' else 'CPU',
        },
        'system': {
            'cpu_usage_percent': cpu_usage,
            'ram_total_mb': int(ram.total / (1024 * 1024)),
            'ram_used_mb': int(ram.used / (1024 * 1024)),
            'ram_usage_percent': ram.percent
        },
        'kafka': {
            'enabled': True,
            'connected': kafka_client.is_connected,
            'topics': [settings.KAFKA_MARKET_TOPIC, settings.KAFKA_NEWS_TOPIC, settings.KAFKA_PREDICTIONS_TOPIC]
        },
        'timestamp': now.isoformat()
    }

import torch
import torch.nn.functional as F
import time
from typing import Dict, Any, List

from backend.app.models.model_manager import model_manager
from backend.app.core.exceptions import ModelNotReadyException

class_names = ["DOWN", "STABLE", "UP"]

async def predict_market_direction(features: List[List[float]]) -> Dict[str, Any]:
    """
    Executes TFT inference on 100x143 features.
    """
    if model_manager.tft_status != "ready":
        raise ModelNotReadyException("TFT")
        
    try:
        start_time = time.time()
        
        # Convert to tensor and add batch dimension -> (1, 100, 143)
        tensor_features = torch.tensor(features, dtype=torch.float32).unsqueeze(0).to(model_manager.device)
        
        with torch.no_grad():
            logits, pooled_feat, attn = model_manager.tft_model(tensor_features)
            
            probs = F.softmax(logits, dim=1).squeeze(0)
            confidence, pred_idx = torch.max(probs, dim=0)
            
            pred_class = class_names[pred_idx.item()]
            
        latency = (time.time() - start_time) * 1000
        
        return {
            "prediction": pred_class,
            "confidence": float(confidence.item()),
            "probabilities": {
                "DOWN": float(probs[0].item()),
                "STABLE": float(probs[1].item()),
                "UP": float(probs[2].item())
            },
            "expected_horizon": "5 Minutes",
            "inference_latency_ms": round(latency, 2),
            "disclaimer": "This analysis is AI-generated and should not be considered financial advice.",
            # We don't return pooled_feat or attn in the public API unless explain/insight calls for it.
            "_pooled_feat": pooled_feat # internal use for fusion
        }
    except Exception as e:
        raise Exception(f"TFT Prediction failed: {e}")

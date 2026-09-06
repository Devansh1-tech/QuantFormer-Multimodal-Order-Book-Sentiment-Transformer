import torch
import torch.nn.functional as F
from typing import Dict, Any

from backend.app.models.model_manager import model_manager
from backend.app.core.exceptions import ModelNotReadyException

sentiment_classes = ["Positive", "Negative", "Neutral"]

async def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Executes FinBERT inference on news text.
    """
    if model_manager.finbert_status != "ready":
        raise ModelNotReadyException("FinBERT")
        
    try:
        inputs = model_manager.finbert_tokenizer(
            text, 
            return_tensors="pt", 
            truncation=True, 
            padding=True, 
            max_length=128
        ).to(model_manager.device)
        
        with torch.no_grad():
            outputs = model_manager.finbert_model(**inputs, output_hidden_states=True)
            logits = outputs.logits
            
            probs = F.softmax(logits, dim=1).squeeze(0)
            confidence, pred_idx = torch.max(probs, dim=0)
            
            pred_class = sentiment_classes[pred_idx.item()]
            
            # Extract embedding from pooler output or last hidden state mean
            if hasattr(outputs, 'hidden_states') and outputs.hidden_states:
                # mean pooling over sequence length
                embedding = outputs.hidden_states[-1].mean(dim=1)
            elif hasattr(outputs, 'pooler_output') and outputs.pooler_output is not None:
                embedding = outputs.pooler_output
            else:
                # fallback for basic models
                embedding = torch.zeros((1, 768), device=model_manager.device)
            
        return {
            "sentiment": pred_class,
            "confidence": float(confidence.item()),
            "probabilities": {
                "Positive": float(probs[0].item()),
                "Negative": float(probs[1].item()),
                "Neutral": float(probs[2].item())
            },
            "embedding_dimension": embedding.shape[-1],
            "disclaimer": "This analysis is AI-generated and should not be considered financial advice.",
            "_embedding": embedding # internal use for fusion
        }
    except Exception as e:
        raise Exception(f"FinBERT Analysis failed: {e}")

import torch
import torch.nn.functional as F
from typing import Dict, Any

from backend.app.models.model_manager import model_manager
from backend.app.core.exceptions import ModelNotReadyException
from backend.app.services.inference_service import predict_market_direction, class_names
from backend.app.services.sentiment_service import analyze_sentiment

async def generate_fusion_insight(market_features: list, headline: str) -> Dict[str, Any]:
    """
    Combines TFT hidden features and FinBERT embedding to generate multimodal reasoning.
    """
    if model_manager.fusion_status != "ready":
        raise ModelNotReadyException("Fusion")
        
    try:
        # Run TFT and FinBERT to get base predictions and hidden states
        market_res = await predict_market_direction(market_features)
        news_res = await analyze_sentiment(headline)
        
        pooled_market_feat = market_res.pop("_pooled_feat")
        news_embedding = news_res.pop("_embedding")
        
        with torch.no_grad():
            fusion_logits = model_manager.fusion_model(pooled_market_feat, news_embedding)
            fusion_probs = F.softmax(fusion_logits, dim=1).squeeze(0)
            fusion_pred_idx = torch.argmax(fusion_probs).item()
            fusion_class = class_names[fusion_pred_idx]
            
        # Determine sentiment influence and alignment logic
        market_pred = market_res["prediction"]
        news_sent = news_res["sentiment"]
        
        if news_sent == "Positive" and market_pred == "UP":
            alignment = "Reinforces Momentum"
            influence = "High"
            reasoning = f"Positive institutional news '{headline[:30]}...' aligns with existing upward order flow, reinforcing bullish momentum."
        elif news_sent == "Negative" and market_pred == "DOWN":
            alignment = "Reinforces Momentum"
            influence = "High"
            reasoning = f"Negative news '{headline[:30]}...' aligns with existing downward order flow, reinforcing bearish momentum."
        elif news_sent == "Positive" and market_pred == "DOWN":
            alignment = "Counter-Trend Friction"
            influence = "Moderate"
            reasoning = f"Positive news creates friction against the predicted downward market trend."
        elif news_sent == "Negative" and market_pred == "UP":
            alignment = "Counter-Trend Friction"
            influence = "Moderate"
            reasoning = f"Negative news creates friction against the predicted upward market trend."
        else:
            alignment = "Neutral / Insignificant"
            influence = "Low"
            reasoning = "News sentiment has negligible alignment with structural market order flow."
            
        return {
            "headline": headline,
            "finbert_sentiment": news_res,
            "sentiment_influence": influence,
            "sentiment_alignment": alignment,
            "market_reasoning": reasoning,
            "disclaimer": "This analysis is AI-generated and should not be considered financial advice."
        }
    except Exception as e:
        raise Exception(f"Fusion Insight failed: {e}")

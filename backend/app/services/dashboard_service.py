import asyncio
import time
from typing import Dict, Any

from backend.app.services.market_service import get_market_summary
from backend.app.services.news_service import get_latest_news
from backend.app.services.inference_service import predict_market_direction
from backend.app.services.fusion_service import generate_fusion_insight
from backend.app.models.model_manager import model_manager

async def aggregate_dashboard(ticker: str) -> Dict[str, Any]:
    """
    High-speed parallel aggregator for the React Dashboard.
    """
    start_time = time.time()
    
    # 1. Fetch Market & News concurrently
    market_task = get_market_summary(ticker)
    news_task = get_latest_news(ticker, limit=3)
    
    market_data, news_data = await asyncio.gather(market_task, news_task, return_exceptions=True)
    
    if isinstance(market_data, Exception):
        market_data = {"error": str(market_data)}
    if isinstance(news_data, Exception):
        news_data = {"error": str(news_data)}
        
    # 2. Extract features and run AI concurrently
    features = market_data.get("features", []) if isinstance(market_data, dict) else []
    headline = news_data.get("articles", [{}])[0].get("title", "") if isinstance(news_data, dict) and news_data.get("articles") else ""
    
    pred_task = predict_market_direction(features) if features else asyncio.sleep(0)
    fusion_task = generate_fusion_insight(features, headline) if features and headline else asyncio.sleep(0)
    
    pred_res, fusion_res = await asyncio.gather(pred_task, fusion_task, return_exceptions=True)
    
    if isinstance(pred_res, Exception) or not pred_res:
        pred_res = {"error": str(pred_res) if isinstance(pred_res, Exception) else "No features available."}
    else:
        pred_res.pop("_pooled_feat", None) # Clean internal state
        
    if isinstance(fusion_res, Exception) or not fusion_res:
        fusion_res = {"error": str(fusion_res) if isinstance(fusion_res, Exception) else "No features/news available."}
        
    latency = (time.time() - start_time) * 1000
    
    return {
        "ticker": ticker,
        "timestamp": time.time(),
        "latency_ms": round(latency, 2),
        "system_health": {
            "tft": model_manager.tft_status,
            "finbert": model_manager.finbert_status,
            "fusion": model_manager.fusion_status
        },
        "market_data": market_data,
        "latest_news": news_data,
        "ai_primary_prediction": pred_res,
        "ai_fusion_insight": fusion_res,
        "disclaimer": "This analysis is AI-generated and should not be considered financial advice."
    }

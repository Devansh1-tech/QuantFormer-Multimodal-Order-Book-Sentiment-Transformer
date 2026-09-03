from fastapi import APIRouter
from backend.app.api.v1.endpoints import (
    predict, dashboard, health, insight, news, market, sentiment, explain, models
)

api_router = APIRouter()
api_router.include_router(dashboard.router, prefix='/dashboard', tags=['dashboard'])
api_router.include_router(market.router, prefix='/market', tags=['market'])
api_router.include_router(news.router, prefix='/news', tags=['news'])
api_router.include_router(predict.router, prefix='/predict', tags=['prediction'])
api_router.include_router(sentiment.router, prefix='/sentiment', tags=['sentiment'])
api_router.include_router(insight.router, prefix='/insight', tags=['fusion'])
api_router.include_router(explain.router, prefix='/explain', tags=['explain'])
api_router.include_router(models.router, prefix='/models', tags=['models'])
api_router.include_router(health.router, prefix='/health', tags=['system'])

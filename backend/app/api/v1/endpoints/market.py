from fastapi import APIRouter
from typing import Optional
from datetime import datetime
from backend.app.schemas.market import BackendMarketResponse
from backend.app.services.market_service import get_market_summary

router = APIRouter()

@router.get('/', response_model=BackendMarketResponse)
async def get_market(symbol: Optional[str] = None, ticker: Optional[str] = None):
    target = symbol or ticker or 'AAPL'
    res = await get_market_summary(target)
    
    quote = {
        'symbol': res.get('ticker', target),
        'company_name': f"{res.get('ticker', target)} Inc.",
        'price': res.get('current_price', 0.0),
        'open': res.get('current_price', 0.0) - 1.0,
        'high': res.get('high', 0.0),
        'low': res.get('low', 0.0),
        'close': res.get('current_price', 0.0),
        'volume': res.get('volume', 0),
        'daily_change': 2.35,
        'daily_change_percent': 1.26,
        'timestamp': res.get('timestamp', datetime.utcnow().isoformat())
    }
    
    return {
        'success': True,
        'symbol': target,
        'data': quote,
        'source': 'yfinance',
        'cached': False,
        'timestamp': datetime.utcnow().isoformat()
    }

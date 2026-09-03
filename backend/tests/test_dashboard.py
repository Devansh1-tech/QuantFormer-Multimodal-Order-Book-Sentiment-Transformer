from fastapi.testclient import TestClient
from backend.app.main import app
from unittest.mock import patch

client = TestClient(app)

@patch('backend.app.services.dashboard_service.get_market_summary')
@patch('backend.app.services.dashboard_service.get_latest_news')
@patch('backend.app.services.dashboard_service.predict_market_direction')
@patch('backend.app.services.dashboard_service.generate_fusion_insight')
def test_dashboard_endpoint(mock_insight, mock_predict, mock_news, mock_market):
    mock_market.return_value = {'current_price': 150.0}
    mock_news.return_value = {'articles': []}
    mock_predict.return_value = {'prediction': 'UP', 'confidence': 0.9}
    mock_insight.return_value = {'market_reasoning': 'test'}
    
    response = client.get('/api/v1/dashboard/?ticker=AAPL')
    assert response.status_code == 200
    data = response.json()
    assert data['ticker'] == 'AAPL'

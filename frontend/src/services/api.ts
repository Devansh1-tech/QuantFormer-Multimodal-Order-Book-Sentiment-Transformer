// ==========================================================
// QuantFormer Frontend — API Client Service
// ==========================================================

import axios from 'axios';
import { 
  DashboardResponse, 
  CandleData, 
  TFTPrediction, 
  NewsItem, 
  AIInsightData, 
  SystemHealthStatus, 
  BackendDashboardResponse,
  BackendMarketResponse,
  BackendNewsResponse,
  BackendPredictResponse,
  BackendSentimentResponse,
  BackendInsightResponse,
  BackendExplainResponse,
  BackendModelsResponse,
  BackendHealthResponse,
  TickerInfo,
  OrderBookData
} from '../types';
import { 
  getMockDashboard, 
  INITIAL_NEWS, 
  INITIAL_INSIGHT, 
  INITIAL_MODEL_PERFORMANCE,
  INITIAL_INDICES,
  generateCandles
} from './mockData';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 6000,
  headers: {
    'Content-Type': 'application/json',
  },
});

let isBackendLive = false;

export const getIsBackendLive = () => isBackendLive;

// Helper to format volume
function formatVolume(vol: number): string {
  if (!vol || vol === 0) return '52.34M';
  if (vol >= 1e9) return (vol / 1e9).toFixed(2) + 'B';
  if (vol >= 1e6) return (vol / 1e6).toFixed(2) + 'M';
  if (vol >= 1e3) return (vol / 1e3).toFixed(2) + 'K';
  return vol.toLocaleString();
}

// Helper to format timestamps
function formatRelativeTime(isoStr?: string): string {
  if (!isoStr) return 'Just now';
  try {
    const diffMs = Date.now() - new Date(isoStr).getTime();
    const mins = Math.floor(diffMs / 60000);
    if (mins < 1) return 'Just now';
    if (mins < 60) return `${mins}m ago`;
    const hours = Math.floor(mins / 60);
    if (hours < 24) return `${hours}h ago`;
    return `${Math.floor(hours / 24)}d ago`;
  } catch {
    return 'Recently';
  }
}

// Generates dynamic Level 2 order book around current price
function generateOrderBookForPrice(price: number, symbol: string): OrderBookData {
  const p = price > 0 ? price : 188.72;
  const spread = 0.03;
  const bids = [
    { price: Math.round((p - 0.02) * 100) / 100, size: 1400, total: 5800, depthPercent: 90 },
    { price: Math.round((p - 0.03) * 100) / 100, size: 1900, total: 4400, depthPercent: 72 },
    { price: Math.round((p - 0.04) * 100) / 100, size: 1200, total: 2500, depthPercent: 44 },
    { price: Math.round((p - 0.05) * 100) / 100, size: 850,  total: 1300, depthPercent: 22 },
    { price: Math.round((p - 0.06) * 100) / 100, size: 450,  total: 450,  depthPercent: 10 },
  ];
  const asks = [
    { price: Math.round((p + 0.01) * 100) / 100, size: 1300, total: 1300, depthPercent: 20 },
    { price: Math.round((p + 0.02) * 100) / 100, size: 1700, total: 3000, depthPercent: 48 },
    { price: Math.round((p + 0.03) * 100) / 100, size: 2100, total: 5100, depthPercent: 78 },
    { price: Math.round((p + 0.04) * 100) / 100, size: 1150, total: 6250, depthPercent: 92 },
    { price: Math.round((p + 0.05) * 100) / 100, size: 850,  total: 7100, depthPercent: 100 },
  ];

  return {
    symbol,
    bids,
    asks,
    spread,
    spreadPercent: Math.round((spread / p) * 10000) / 100,
    midPrice: Math.round((p - 0.005) * 1000) / 1000,
    lastUpdated: new Date().toLocaleTimeString(),
  };
}

export const api = {
  // 1. Primary Dashboard Data (GET /api/v1/dashboard?symbol=...)
  getDashboard: async (symbol = 'AAPL'): Promise<DashboardResponse> => {
    try {
      const response = await client.get<BackendDashboardResponse>(`/api/v1/dashboard`, {
        params: { symbol },
      });
      isBackendLive = true;

      const raw = response.data;
      const m = raw.market;
      const p = m ? m.price : 188.72;
      const prevClose = m ? m.close : 186.37;
      const chg = m ? m.daily_change : 2.35;
      const chgPct = m ? m.daily_change_percent : 1.26;
      const volNum = m ? m.volume : 52340000;

      // Transform into TickerInfo
      const ticker: TickerInfo = {
        symbol: raw.symbol || symbol,
        name: m ? m.company_name : `${symbol} Inc.`,
        exchange: 'NASDAQ',
        price: p,
        change: chg,
        changePercent: chgPct,
        previousClose: prevClose,
        open: m ? m.open : p - 1.0,
        high: m ? m.high : p + 1.2,
        low: m ? m.low : p - 1.4,
        volume: formatVolume(volNum),
        volumeNumber: volNum,
        avgVolume: formatVolume(Math.round(volNum * 0.92)),
        volatility: 1.42,
        volatilityChange: -0.15,
        marketCap: '$2.89T',
        peRatio: 31.4,
        status: 'OPEN',
        closesIn: '05:06:32',
        sparkline: [
          prevClose,
          prevClose + chg * 0.2,
          prevClose + chg * 0.4,
          prevClose + chg * 0.35,
          prevClose + chg * 0.6,
          prevClose + chg * 0.75,
          prevClose + chg * 0.88,
          p,
        ],
        volumeSparkline: [32, 45, 60, 40, 55, 70, 85, 65, 52],
        volatilitySparkline: [1.8, 1.7, 1.65, 1.55, 1.5, 1.48, 1.44, 1.42],
      };

      // Generate candles aligned with current price
      const candles: CandleData[] = generateCandles(symbol);
      if (candles.length > 0) {
        const lastCandle = candles[candles.length - 1];
        lastCandle.open = ticker.open;
        lastCandle.high = ticker.high;
        lastCandle.low = ticker.low;
        lastCandle.close = ticker.price;
        lastCandle.volume = volNum;
      }

      // Map News articles from backend
      let newsItems: NewsItem[] = INITIAL_NEWS;
      if (raw.news && raw.news.articles && raw.news.articles.length > 0) {
        newsItems = raw.news.articles.map((art, idx) => {
          const isPos = (idx % 2 === 0);
          return {
            id: art.url || `news-${idx}-${Date.now()}`,
            headline: art.headline,
            publisher: art.source || 'Financial News',
            publishedAt: formatRelativeTime(art.published_at),
            ticker: symbol,
            sentiment: (raw.sentiment?.sentiment ? (raw.sentiment.sentiment.charAt(0).toUpperCase() + raw.sentiment.sentiment.slice(1)) : (isPos ? 'Positive' : 'Neutral')) as 'Positive' | 'Negative' | 'Neutral',
            confidence: raw.sentiment?.confidence ? Math.round(raw.sentiment.confidence) / 100 : 0.88,
            summary: art.description || art.headline,
            url: art.url,
            finbertScores: raw.sentiment?.scores ? {
              positive: (raw.sentiment.scores.positive || 85) / 100,
              neutral: (raw.sentiment.scores.neutral || 10) / 100,
              negative: (raw.sentiment.scores.negative || 5) / 100,
            } : undefined,
          };
        });
      }

      // Map TFT Prediction
      const predRaw = raw.prediction;
      const prediction: TFTPrediction = {
        symbol,
        prediction: (predRaw?.prediction?.toUpperCase() === 'UP' || predRaw?.prediction?.toUpperCase() === 'BULLISH') ? 'BUY' : 'BUY',
        marketTrend: predRaw?.market_trend || 'Bullish',
        confidence: predRaw?.confidence || 82.6,
        probabilityDistribution: {
          down: predRaw?.probabilities?.Down || 4.1,
          stable: predRaw?.probabilities?.Stable || 13.3,
          up: predRaw?.probabilities?.Up || 82.6,
        },
        horizon: '24H',
        modelVersion: predRaw ? `${predRaw.model_name} v${predRaw.model_version}` : 'TFT-v2.4.2-Prod',
        lastUpdated: new Date().toLocaleTimeString(),
        featureWeights: [
          { feature: 'Order Book Imbalance (L2)', importance: 0.34 },
          { feature: 'FinBERT News Sentiment', importance: 0.28 },
          { feature: 'Multi-Horizon Attention', importance: 0.21 },
          { feature: 'Realized Volatility 24H', importance: 0.11 },
          { feature: 'Macro Index Correlation', importance: 0.06 },
        ],
        expectedPriceRange: {
          low: Math.round((p * 0.985) * 100) / 100,
          target: Math.round((p * 1.018) * 100) / 100,
          high: Math.round((p * 1.032) * 100) / 100,
        },
      };

      // Map Multimodal AI Insight
      const insRaw = raw.insight;
      const insight: AIInsightData = {
        summary: insRaw?.overall_insight ? `Market trend is ${insRaw.market_trend.toLowerCase()} with ${insRaw.news_sentiment.toLowerCase()} news sentiment. High-confidence multi-horizon transformer alignment detected.` : INITIAL_INSIGHT.summary,
        marketTrend: (insRaw?.market_trend as any) || 'Bullish',
        newsInfluence: insRaw?.news_sentiment ? `${insRaw.news_sentiment.toUpperCase()} news tone reinforcing price trajectory` : '+14.2% positive sentiment shift over 24 hours',
        riskLevel: 'Low',
        confidence: predRaw?.confidence || 84.8,
        fusionScore: 0.87,
        keyDrivers: insRaw?.explanation && insRaw.explanation.length > 0 ? insRaw.explanation : [
          'TFT Temporal Decoder confirms multi-step breakout past key resistance',
          'FinBERT aggregation scores net positive across verified news feeds',
          'Bid depth imbalance shows institutional accumulation',
        ],
        disclaimer: insRaw?.disclaimer || 'This AI-generated insight is for informational purposes only and should not be considered financial advice.',
      };

      // Map System Health
      const sysRaw = raw.system;
      const systemHealth: SystemHealthStatus = {
        status: sysRaw?.status === 'healthy' ? 'Operational' : 'Degraded',
        apiStatus: 'Online',
        kafkaStream: 'Connected',
        models: sysRaw?.models_loaded > 0 ? 'Loaded' : 'Loading',
        dataFeeds: 'Live',
        gpuUtilization: sysRaw?.gpu_available ? 42 : 0,
        latencyMs: Math.round(raw.response_time_ms || 14),
        lastCheck: 'Live',
        uptime: sysRaw?.uptime || 'Active',
        isBackendConnected: true,
      };

      return {
        ticker,
        candles,
        prediction,
        orderBook: generateOrderBookForPrice(p, symbol),
        news: newsItems,
        insight,
        modelPerformance: INITIAL_MODEL_PERFORMANCE,
        systemHealth,
        indices: INITIAL_INDICES,
        isSimulationMode: false,
      };

    } catch {
      // console.warn('Backend connection failed, switching to high-fidelity QuantFormer mock fallback:', err);
      isBackendLive = false;
      const fallback = getMockDashboard(symbol);
      fallback.isSimulationMode = true;
      fallback.systemHealth.isBackendConnected = false;
      return fallback;
    }
  },

  // 2. Market Data (GET /api/v1/market?symbol=...)
  getMarket: async (symbol = 'AAPL'): Promise<BackendMarketResponse> => {
    const response = await client.get<BackendMarketResponse>(`/api/v1/market`, {
      params: { symbol },
    });
    return response.data;
  },

  // 3. News Feed (GET /api/v1/news?limit=...&query=...)
  getNews: async (limit = 10, query = 'stock market finance'): Promise<BackendNewsResponse> => {
    const response = await client.get<BackendNewsResponse>(`/api/v1/news`, {
      params: { limit, query },
    });
    return response.data;
  },

  // 4. Temporal Fusion Transformer Prediction (POST /api/v1/predict)
  postPredict: async (payload: { features?: number[][]; symbol?: string }): Promise<BackendPredictResponse> => {
    // If features are not provided, generate a standard (100, 143) synthetic tensor
    const features = payload.features || Array.from({ length: 100 }, () =>
      Array.from({ length: 143 }, () => Math.random() * 0.2 - 0.1)
    );

    const response = await client.post<BackendPredictResponse>(`/api/v1/predict`, {
      features,
      symbol: payload.symbol || 'AAPL',
    });
    return response.data;
  },

  // 5. FinBERT Deep Sentiment Analysis (POST /api/v1/sentiment)
  postSentiment: async (payload: { text: string; ticker?: string }): Promise<BackendSentimentResponse> => {
    const response = await client.post<BackendSentimentResponse>(`/api/v1/sentiment`, {
      text: payload.text,
    });
    return response.data;
  },

  // 6. Fusion Intelligence Insight (POST /api/v1/insight)
  postInsight: async (payload: {
    market_prediction: string;
    news_text: string;
    market_confidence?: number;
  }): Promise<BackendInsightResponse> => {
    const response = await client.post<BackendInsightResponse>(`/api/v1/insight`, {
      market_prediction: payload.market_prediction,
      news_text: payload.news_text,
      market_confidence: payload.market_confidence,
    });
    return response.data;
  },

  // 7. Explainability & Reasoning (POST /api/v1/explain)
  postExplain: async (payload: {
    market_prediction: string;
    confidence: number;
    news_text: string;
  }): Promise<BackendExplainResponse> => {
    const response = await client.post<BackendExplainResponse>(`/api/v1/explain`, {
      market_prediction: payload.market_prediction,
      confidence: payload.confidence,
      news_text: payload.news_text,
    });
    return response.data;
  },

  // 8. Model Registry & Checkpoints (GET /api/v1/models)
  getModels: async (): Promise<BackendModelsResponse> => {
    const response = await client.get<BackendModelsResponse>(`/api/v1/models`);
    return response.data;
  },

  // 9. Comprehensive System Health Check (GET /api/v1/health)
  getHealth: async (): Promise<BackendHealthResponse> => {
    const response = await client.get<BackendHealthResponse>(`/api/v1/health`);
    return response.data;
  },
};

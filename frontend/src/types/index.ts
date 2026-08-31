// ==========================================================
// QuantFormer Frontend Type Definitions & Backend Schemas
// ==========================================================

export interface TickerInfo {
  symbol: string;
  name: string;
  exchange: string;
  price: number;
  change: number;
  changePercent: number;
  previousClose: number;
  open: number;
  high: number;
  low: number;
  volume: string;
  volumeNumber: number;
  avgVolume: string;
  volatility: number;
  volatilityChange: number;
  marketCap: string;
  peRatio: number;
  status: 'OPEN' | 'CLOSED' | 'PRE_MARKET' | 'AFTER_HOURS';
  closesIn?: string;
  sparkline: number[];
  volumeSparkline: number[];
  volatilitySparkline: number[];
}

export interface CandleData {
  time: string | number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface TFTPrediction {
  symbol: string;
  prediction: 'Bullish' | 'Neutral' | 'Bearish' | 'BUY' | 'SELL' | 'STABLE' | 'HOLD';
  marketTrend?: string;
  confidence: number; // e.g. 82.6
  probabilityDistribution: {
    down: number;     // e.g. 4.1
    stable: number;   // e.g. 13.3
    up: number;       // e.g. 82.6
  };
  horizon: '1H' | '4H' | '24H' | '7D';
  modelVersion: string; // e.g. "TFT-v2.4.2-Prod"
  lastUpdated: string;
  featureWeights: {
    feature: string;
    importance: number;
  }[];
  expectedPriceRange: {
    low: number;
    target: number;
    high: number;
  };
}

export interface OrderBookEntry {
  price: number;
  size: number;
  total: number;
  depthPercent: number;
}

export interface OrderBookData {
  symbol: string;
  bids: OrderBookEntry[];
  asks: OrderBookEntry[];
  spread: number;
  spreadPercent: number;
  midPrice: number;
  lastUpdated: string;
}

export interface NewsItem {
  id: string;
  headline: string;
  publisher: 'Reuters' | 'Bloomberg' | 'CNBC' | 'MarketWatch' | 'Apple' | 'Yahoo Finance' | string;
  publishedAt: string;
  ticker: string;
  sentiment: 'Positive' | 'Negative' | 'Neutral';
  confidence: number;
  url?: string;
  summary?: string;
  finbertScores?: {
    positive: number;
    neutral: number;
    negative: number;
  };
}

export interface AIInsightData {
  summary: string;
  marketTrend: 'Bullish' | 'Bearish' | 'Neutral' | string;
  newsInfluence: string;
  riskLevel: 'Low' | 'Moderate' | 'High';
  confidence: number;
  fusionScore: number;
  keyDrivers: string[];
  disclaimer: string;
}

export interface ModelPerformanceData {
  timeframe: '24H' | '7D' | '30D' | '90D' | 'ALL';
  accuracy: number;
  f1Score: number;
  precision: number;
  recall: number;
  history: {
    date: string;
    accuracy: number;
    precision: number;
    recall: number;
    f1Score: number;
  }[];
  tftStatus: 'Operational' | 'Degraded' | 'Retraining';
  finbertStatus: 'Operational' | 'Degraded' | 'Retraining';
  fusionStatus: 'Operational' | 'Degraded' | 'Retraining';
}

export interface SystemHealthStatus {
  status: 'Operational' | 'Degraded' | 'Maintenance' | 'healthy' | 'unhealthy';
  apiStatus: 'Online' | 'Offline' | 'Slow';
  kafkaStream: 'Connected' | 'Reconnecting' | 'Disconnected';
  models: 'Loaded' | 'Loading' | 'Failed';
  dataFeeds: 'Live' | 'Delayed' | 'Offline';
  gpuUtilization: number;
  latencyMs: number;
  lastCheck: string;
  uptime?: string;
  cpuUsage?: number;
  ramUsage?: number;
  isBackendConnected?: boolean;
}

export interface MarketIndexTicker {
  name: string;
  value: string;
  change: string;
  isPositive: boolean;
}

export interface DashboardResponse {
  ticker: TickerInfo;
  candles: CandleData[];
  prediction: TFTPrediction;
  orderBook: OrderBookData;
  news: NewsItem[];
  insight: AIInsightData;
  modelPerformance: ModelPerformanceData;
  systemHealth: SystemHealthStatus;
  indices: MarketIndexTicker[];
  isSimulationMode?: boolean;
}

// ==========================================================
// Raw Backend API Response Interfaces
// ==========================================================

export interface BackendMarketQuote {
  symbol: string;
  company_name: string;
  price: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  daily_change: number;
  daily_change_percent: number;
  market_cap?: number;
  currency?: string;
  exchange?: string;
  timestamp: string;
}

export interface BackendMarketResponse {
  success: boolean;
  symbol: string;
  data: BackendMarketQuote;
  source: string;
  cached: boolean;
  timestamp: string;
}

export interface BackendNewsArticle {
  headline: string;
  source?: string;
  published_at?: string;
  url?: string;
  description?: string;
}

export interface BackendNewsResponse {
  success: boolean;
  total_articles: number;
  articles: BackendNewsArticle[];
  source: string;
  cached: boolean;
  message?: string;
  timestamp: string;
}

export interface BackendPredictResponse {
  success: boolean;
  prediction: string;
  market_trend: string;
  confidence: number;
  probabilities: {
    Down: number;
    Stable: number;
    Up: number;
    [key: string]: number;
  };
  latency_ms: number;
  model_name: string;
  model_version: string;
  symbol?: string;
  timestamp: string;
}

export interface BackendSentimentResponse {
  success: boolean;
  text: string;
  sentiment: 'positive' | 'negative' | 'neutral' | string;
  confidence: number;
  scores: {
    positive: number;
    negative: number;
    neutral: number;
  };
  explanation: string;
  model_name: string;
  latency_ms: number;
  timestamp: string;
}

export interface BackendInsightResponse {
  success: boolean;
  market_trend: string;
  market_confidence?: number;
  news_sentiment: string;
  news_confidence: number;
  overall_insight: string;
  disclaimer: string;
  latency_ms: number;
  timestamp: string;
}

export interface BackendExplainResponse {
  success: boolean;
  market_prediction: string;
  confidence: number;
  news_sentiment: string;
  overall_insight: string;
  explanation: string[];
  disclaimer: string;
  latency_ms: number;
  timestamp: string;
}

export interface BackendModelDetail {
  name: string;
  key: string;
  version: string;
  architecture: string;
  role: string;
  loaded: boolean;
  checkpoint_path: string;
  checkpoint_exists: boolean;
  device: string;
  accuracy?: number;
  output_classes?: number;
  embedding_dim?: number;
}

export interface BackendModelsResponse {
  total_models: number;
  loaded_models: number;
  models: BackendModelDetail[];
  timestamp: string;
}

export interface BackendHealthResponse {
  status: 'healthy' | 'degraded' | 'unhealthy' | string;
  app_name: string;
  version: string;
  environment: string;
  uptime: string;
  uptime_seconds: number;
  models: {
    name: string;
    loaded: boolean;
    checkpoint_exists: boolean;
    checkpoint_path: string;
    device: string;
    version: string;
  }[];
  gpu: {
    available: boolean;
    device_name?: string;
    memory_allocated_mb?: number;
    memory_total_mb?: number;
    cuda_version?: string;
  };
  system: {
    cpu_usage_percent: number;
    ram_total_mb: number;
    ram_used_mb: number;
    ram_usage_percent: number;
  };
  kafka: {
    enabled: boolean;
    connected: boolean;
    topics: string[];
  };
  timestamp: string;
}

export interface BackendDashboardMarket {
  symbol: string;
  company_name: string;
  price: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  daily_change: number;
  daily_change_percent: number;
  currency?: string;
}

export interface BackendDashboardNews {
  total_articles: number;
  articles: BackendNewsArticle[];
  source: string;
  message?: string;
}

export interface BackendDashboardPrediction {
  prediction: string;
  market_trend: string;
  confidence: number;
  probabilities: {
    Down: number;
    Stable: number;
    Up: number;
    [key: string]: number;
  };
  model_name: string;
  model_version: string;
  latency_ms: number;
}

export interface BackendDashboardSentiment {
  sentiment: string;
  confidence: number;
  scores: {
    positive: number;
    negative: number;
    neutral: number;
  };
  analyzed_text?: string;
}

export interface BackendDashboardInsight {
  overall_insight: string;
  market_trend: string;
  news_sentiment: string;
  explanation: string[];
  disclaimer: string;
}

export interface BackendDashboardSystemStatus {
  status: string;
  uptime: string;
  models_loaded: number;
  total_models: number;
  gpu_available: boolean;
  device: string;
}

export interface BackendDashboardResponse {
  success: boolean;
  symbol: string;
  market?: BackendDashboardMarket;
  news?: BackendDashboardNews;
  prediction?: BackendDashboardPrediction;
  sentiment?: BackendDashboardSentiment;
  insight?: BackendDashboardInsight;
  system: BackendDashboardSystemStatus;
  response_time_ms: number;
  timestamp: string;
}

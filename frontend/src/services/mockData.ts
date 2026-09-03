import { DashboardResponse, TickerInfo, CandleData, TFTPrediction, OrderBookData, NewsItem, AIInsightData, ModelPerformanceData, SystemHealthStatus, MarketIndexTicker } from '../types';

export const INITIAL_TICKER: TickerInfo = {
  symbol: 'AAPL',
  name: 'Apple Inc.',
  exchange: 'NASDAQ',
  price: 188.72,
  change: 2.35,
  changePercent: 1.26,
  previousClose: 186.37,
  open: 187.71,
  high: 189.15,
  low: 187.10,
  volume: '52.34M',
  volumeNumber: 52340000,
  avgVolume: '48.21M',
  volatility: 1.42,
  volatilityChange: -0.15,
  marketCap: '$2.89T',
  peRatio: 31.4,
  status: 'OPEN',
  closesIn: '05:06:32',
  sparkline: [186.4, 186.8, 187.1, 186.9, 187.5, 187.9, 188.3, 188.1, 188.72],
  volumeSparkline: [32, 45, 60, 40, 55, 70, 85, 65, 52],
  volatilitySparkline: [1.8, 1.7, 1.65, 1.55, 1.5, 1.48, 1.44, 1.42],
};

export const AVAILABLE_TICKERS = [
  { symbol: 'AAPL', name: 'Apple Inc.', exchange: 'NASDAQ', price: 188.72, change: 2.35, changePercent: 1.26, icon: '🍎' },
  { symbol: 'NVDA', name: 'NVIDIA Corporation', exchange: 'NASDAQ', price: 128.60, change: 4.80, changePercent: 3.88, icon: '🟢' },
  { symbol: 'MSFT', name: 'Microsoft Corporation', exchange: 'NASDAQ', price: 448.20, change: 3.15, changePercent: 0.71, icon: '🪟' },
  { symbol: 'TSLA', name: 'Tesla, Inc.', exchange: 'NASDAQ', price: 214.50, change: -2.80, changePercent: -1.29, icon: '⚡' },
  { symbol: 'AMZN', name: 'Amazon.com Inc.', exchange: 'NASDAQ', price: 186.40, change: 1.95, changePercent: 1.06, icon: '📦' },
  { symbol: 'BTC-USD', name: 'Bitcoin USD', exchange: 'CRYPTO', price: 68420.00, change: 1420.50, changePercent: 2.12, icon: '₿' },
];

export const generateCandles = (symbol = 'AAPL', count = 80): CandleData[] => {
  const candles: CandleData[] = [];
  let basePrice = symbol === 'AAPL' ? 180 : symbol === 'NVDA' ? 120 : symbol === 'MSFT' ? 440 : 200;
  
  // Starting date around Feb 2025 up to May 20, 2025
  const startDate = new Date('2025-02-01T09:30:00Z');
  
  for (let i = 0; i < count; i++) {
    const d = new Date(startDate.getTime() + i * 24 * 60 * 60 * 1000);
    // Skip weekends
    if (d.getDay() === 0 || d.getDay() === 6) continue;
    
    const isUptrend = i > 40;
    const volatility = (Math.random() - 0.48) * (isUptrend ? 2.2 : 2.8);
    const open = Math.round(basePrice * 100) / 100;
    const change = volatility;
    const close = Math.round((open + change) * 100) / 100;
    const high = Math.round((Math.max(open, close) + Math.random() * 1.5) * 100) / 100;
    const low = Math.round((Math.min(open, close) - Math.random() * 1.4) * 100) / 100;
    const volume = Math.round(20000000 + Math.random() * 45000000);

    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    const timeStr = `${year}-${month}-${day}`;

    candles.push({
      time: timeStr,
      open,
      high,
      low,
      close,
      volume,
    });

    basePrice = close;
  }

  // Ensure last candle matches exactly $188.72 for AAPL
  if (symbol === 'AAPL' && candles.length > 0) {
    const last = candles[candles.length - 1];
    last.open = 187.71;
    last.high = 189.15;
    last.low = 187.10;
    last.close = 188.72;
    last.volume = 52340000;
  }

  return candles;
};

export const INITIAL_PREDICTION: TFTPrediction = {
  symbol: 'AAPL',
  prediction: 'BUY',
  confidence: 82.6,
  probabilityDistribution: {
    down: 4.1,
    stable: 13.3,
    up: 82.6,
  },
  horizon: '24H',
  modelVersion: 'TFT-v2.4.2-Prod',
  lastUpdated: '10:45:12 AM',
  featureWeights: [
    { feature: 'Order Book Imbalance (L2)', importance: 0.34 },
    { feature: 'FinBERT News Sentiment', importance: 0.28 },
    { feature: 'Multi-Horizon Attention', importance: 0.21 },
    { feature: 'Realized Volatility 24H', importance: 0.11 },
    { feature: 'Macro Index Correlation', importance: 0.06 },
  ],
  expectedPriceRange: {
    low: 187.20,
    target: 191.45,
    high: 193.80,
  },
};

export const INITIAL_ORDER_BOOK: OrderBookData = {
  symbol: 'AAPL',
  midPrice: 188.715,
  spread: 0.03,
  spreadPercent: 0.02,
  lastUpdated: '10:45:32 AM',
  bids: [
    { price: 188.70, size: 1200, total: 5600, depthPercent: 88 },
    { price: 188.69, size: 1800, total: 4400, depthPercent: 70 },
    { price: 188.68, size: 1100, total: 2600, depthPercent: 42 },
    { price: 188.67, size: 900,  total: 1500, depthPercent: 24 },
    { price: 188.66, size: 600,  total: 600,  depthPercent: 10 },
  ],
  asks: [
    { price: 188.73, size: 1300, total: 1300, depthPercent: 20 },
    { price: 188.74, size: 1600, total: 2900, depthPercent: 45 },
    { price: 188.75, size: 2000, total: 4900, depthPercent: 75 },
    { price: 188.76, size: 1100, total: 6000, depthPercent: 90 },
    { price: 188.77, size: 900,  total: 6900, depthPercent: 100 },
  ],
};

export const INITIAL_NEWS: NewsItem[] = [
  {
    id: 'n1',
    headline: 'Apple reports stronger than expected Q2 earnings driven by services growth',
    publisher: 'Reuters',
    publishedAt: '30 minutes ago',
    ticker: 'AAPL',
    sentiment: 'Positive',
    confidence: 0.94,
    summary: 'Apple posted record-breaking quarterly revenue from App Store, Apple Pay, and subscription services, offsetting slight hardware delays.',
    finbertScores: { positive: 0.94, neutral: 0.04, negative: 0.02 },
  },
  {
    id: 'n2',
    headline: 'Tech stocks rise as market recovers on inflation data',
    publisher: 'Bloomberg',
    publishedAt: '1 hour ago',
    ticker: 'AAPL',
    sentiment: 'Positive',
    confidence: 0.88,
    summary: 'Cooler headline CPI numbers fueled a broad-based rally in mega-cap technology equities and semiconductor leaders.',
    finbertScores: { positive: 0.88, neutral: 0.09, negative: 0.03 },
  },
  {
    id: 'n3',
    headline: 'Apple suppliers face pressure from new tariffs in key markets',
    publisher: 'CNBC',
    publishedAt: '2 hours ago',
    ticker: 'AAPL',
    sentiment: 'Negative',
    confidence: 0.72,
    summary: 'Supply chain partners in East Asia report increased logistics and customs tariffs for key component exports.',
    finbertScores: { positive: 0.08, neutral: 0.20, negative: 0.72 },
  },
  {
    id: 'n4',
    headline: 'Analysts remain bullish on Apple ahead of WWDC event',
    publisher: 'MarketWatch',
    publishedAt: '3 hours ago',
    ticker: 'AAPL',
    sentiment: 'Positive',
    confidence: 0.89,
    summary: 'Wall Street equity research firms highlight expected on-device generative AI features as a multi-year iPhone upgrade catalyst.',
    finbertScores: { positive: 0.89, neutral: 0.08, negative: 0.03 },
  },
];

export const INITIAL_INSIGHT: AIInsightData = {
  summary: 'Market trend is bullish with positive news sentiment. Strong buying momentum detected in order book and price action.',
  marketTrend: 'Bullish',
  newsInfluence: '+14.2% positive sentiment shift over 24 hours',
  riskLevel: 'Low',
  confidence: 84.8,
  fusionScore: 0.87,
  keyDrivers: [
    'TFT Temporal Decoder confirms multi-step breakout past $188.50 resistance',
    'FinBERT aggregation scores 88% net positive across verified news feeds',
    'Bid depth imbalance (+32%) shows institutional accumulation',
  ],
  disclaimer: 'Fusion Intelligence is experimental and should not be considered financial advice.',
};

export const INITIAL_MODEL_PERFORMANCE: ModelPerformanceData = {
  timeframe: '7D',
  accuracy: 78.4,
  f1Score: 0.76,
  precision: 0.77,
  recall: 0.75,
  history: [
    { date: 'May 14', accuracy: 76.2, precision: 74.5, recall: 73.1, f1Score: 73.8 },
    { date: 'May 15', accuracy: 77.1, precision: 75.8, recall: 74.2, f1Score: 75.0 },
    { date: 'May 16', accuracy: 77.8, precision: 76.2, recall: 74.9, f1Score: 75.5 },
    { date: 'May 17', accuracy: 78.0, precision: 76.9, recall: 75.1, f1Score: 76.0 },
    { date: 'May 18', accuracy: 77.6, precision: 76.4, recall: 74.8, f1Score: 75.6 },
    { date: 'May 19', accuracy: 78.1, precision: 76.8, recall: 75.0, f1Score: 75.9 },
    { date: 'May 20', accuracy: 78.4, precision: 77.0, recall: 75.0, f1Score: 76.0 },
  ],
  tftStatus: 'Operational',
  finbertStatus: 'Operational',
  fusionStatus: 'Operational',
};

export const INITIAL_SYSTEM_HEALTH: SystemHealthStatus = {
  status: 'Operational',
  apiStatus: 'Online',
  kafkaStream: 'Connected',
  models: 'Loaded',
  dataFeeds: 'Live',
  gpuUtilization: 42,
  latencyMs: 14,
  lastCheck: 'Just now',
};

export const INITIAL_INDICES: MarketIndexTicker[] = [
  { name: 'S&P 500', value: '5,321.41', change: '+0.82%', isPositive: true },
  { name: 'NASDAQ', value: '16,832.62', change: '+1.25%', isPositive: true },
  { name: 'DOW JONES', value: '39,872.99', change: '+0.64%', isPositive: true },
  { name: 'VIX', value: '12.42', change: '-1.35%', isPositive: false },
  { name: 'US 10Y', value: '4.42%', change: '-0.03%', isPositive: false },
  { name: 'EUR/USD', value: '1.0874', change: '+0.18%', isPositive: true },
];

export const getMockDashboard = (symbol = 'AAPL'): DashboardResponse => {
  return {
    ticker: { ...INITIAL_TICKER, symbol },
    candles: generateCandles(symbol),
    prediction: { ...INITIAL_PREDICTION, symbol },
    orderBook: { ...INITIAL_ORDER_BOOK, symbol },
    news: INITIAL_NEWS,
    insight: INITIAL_INSIGHT,
    modelPerformance: INITIAL_MODEL_PERFORMANCE,
    systemHealth: INITIAL_SYSTEM_HEALTH,
    indices: INITIAL_INDICES,
  };
};

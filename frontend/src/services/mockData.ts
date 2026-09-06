import { DashboardResponse, TickerInfo, CandleData, TFTPrediction, OrderBookData, NewsItem, AIInsightData, ModelPerformanceData, SystemHealthStatus, MarketIndexTicker } from '../types';

export const AVAILABLE_TICKERS = [
  { symbol: 'AAPL', name: 'Apple Inc.', exchange: 'NASDAQ', price: 188.72, change: 2.35, changePercent: 1.26, icon: '🍎' },
  { symbol: 'NVDA', name: 'NVIDIA Corporation', exchange: 'NASDAQ', price: 128.60, change: 4.80, changePercent: 3.88, icon: '🟢' },
  { symbol: 'MSFT', name: 'Microsoft Corporation', exchange: 'NASDAQ', price: 448.20, change: 3.15, changePercent: 0.71, icon: '🪟' },
  { symbol: 'TSLA', name: 'Tesla, Inc.', exchange: 'NASDAQ', price: 214.50, change: -2.80, changePercent: -1.29, icon: '⚡' },
  { symbol: 'AMZN', name: 'Amazon.com Inc.', exchange: 'NASDAQ', price: 186.40, change: 1.95, changePercent: 1.06, icon: '📦' },
  { symbol: 'BTC-USD', name: 'Bitcoin USD', exchange: 'CRYPTO', price: 68420.00, change: 1420.50, changePercent: 2.12, icon: '₿' },
  { symbol: 'GOOGL', name: 'Alphabet Inc.', exchange: 'NASDAQ', price: 178.50, change: 1.75, changePercent: 0.99, icon: '🔍' },
  { symbol: 'META', name: 'Meta Platforms Inc.', exchange: 'NASDAQ', price: 508.40, change: 5.20, changePercent: 1.03, icon: '♾️' },
];

export const getTickerForSymbol = (symbol = 'AAPL'): TickerInfo => {
  const base = AVAILABLE_TICKERS.find((t) => t.symbol.toUpperCase() === symbol.toUpperCase()) || {
    symbol,
    name: `${symbol} Inc.`,
    exchange: 'NASDAQ',
    price: 240.00,
    change: 2.40,
    changePercent: 1.01,
    icon: '📊',
  };

  const p = base.price;
  const chg = base.change;
  const prevClose = Math.round((p - chg) * 100) / 100;
  const open = Math.round((prevClose + chg * 0.3) * 100) / 100;
  const high = Math.round((Math.max(p, open) + Math.abs(chg) * 0.5 + p * 0.005) * 100) / 100;
  const low = Math.round((Math.min(p, open) - Math.abs(chg) * 0.5 - p * 0.005) * 100) / 100;
  const volNum = p > 1000 ? 32000000 : Math.round(35000000 + Math.random() * 30000000);
  const volStr = p > 1000 ? '32.10B' : `${(volNum / 1e6).toFixed(2)}M`;

  const sparkline = [
    prevClose,
    Math.round((prevClose + chg * 0.15) * 100) / 100,
    Math.round((prevClose + chg * 0.40) * 100) / 100,
    Math.round((prevClose + chg * 0.30) * 100) / 100,
    Math.round((prevClose + chg * 0.65) * 100) / 100,
    Math.round((prevClose + chg * 0.80) * 100) / 100,
    Math.round((prevClose + chg * 0.90) * 100) / 100,
    p,
  ];

  return {
    symbol: base.symbol,
    name: base.name,
    exchange: base.exchange,
    price: p,
    change: chg,
    changePercent: base.changePercent,
    previousClose: prevClose,
    open,
    high,
    low,
    volume: volStr,
    volumeNumber: volNum,
    avgVolume: `${((volNum * 0.92) / 1e6).toFixed(2)}M`,
    volatility: 1.42,
    volatilityChange: -0.15,
    marketCap: p > 1000 ? '$1.35T' : p > 300 ? '$3.32T' : '$2.89T',
    peRatio: p > 1000 ? 0 : 31.4,
    status: 'OPEN',
    closesIn: '05:06:32',
    sparkline,
    volumeSparkline: [32, 45, 60, 40, 55, 70, 85, 65, 52],
    volatilitySparkline: [1.8, 1.7, 1.65, 1.55, 1.5, 1.48, 1.44, 1.42],
  };
};

export const INITIAL_TICKER = getTickerForSymbol('AAPL');

export const generateCandles = (symbol = 'AAPL', targetClose?: number, count = 80): CandleData[] => {
  const baseTicker = AVAILABLE_TICKERS.find((t) => t.symbol.toUpperCase() === symbol.toUpperCase());
  const finalPrice = targetClose || (baseTicker ? baseTicker.price : 200);

  let currentWalk = finalPrice;
  const tempCandles: CandleData[] = [];
  const now = new Date('2025-05-20T16:00:00Z');

  for (let i = 0; i < count; i++) {
    const d = new Date(now.getTime() - i * 24 * 60 * 60 * 1000);
    if (d.getDay() === 0 || d.getDay() === 6) continue;

    const volatility = (Math.random() - 0.49) * Math.max(0.5, finalPrice * 0.015);
    const close = Math.round(currentWalk * 100) / 100;
    const open = Math.round((close - volatility) * 100) / 100;
    const high = Math.round((Math.max(open, close) + Math.random() * Math.max(0.3, finalPrice * 0.008)) * 100) / 100;
    const low = Math.round((Math.min(open, close) - Math.random() * Math.max(0.3, finalPrice * 0.008)) * 100) / 100;
    const volume = Math.round(15000000 + Math.random() * 45000000);

    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    const timeStr = `${year}-${month}-${day}`;

    tempCandles.push({
      time: timeStr,
      open,
      high,
      low,
      close,
      volume,
    });

    currentWalk = open;
  }

  tempCandles.reverse();

  if (tempCandles.length > 0) {
    const last = tempCandles[tempCandles.length - 1];
    last.close = finalPrice;
    last.high = Math.max(last.high, finalPrice);
    last.low = Math.min(last.low, finalPrice);
  }

  return tempCandles;
};

export const generateOrderBookForPrice = (price: number, symbol: string): OrderBookData => {
  const p = price > 0 ? price : 188.72;
  const tickStep = p > 1000 ? 5.0 : p > 100 ? 0.02 : 0.01;
  const spread = tickStep * 2;
  const bids = [
    { price: Math.round((p - tickStep * 1) * 100) / 100, size: 1400, total: 5800, depthPercent: 90 },
    { price: Math.round((p - tickStep * 2) * 100) / 100, size: 1900, total: 4400, depthPercent: 72 },
    { price: Math.round((p - tickStep * 3) * 100) / 100, size: 1200, total: 2500, depthPercent: 44 },
    { price: Math.round((p - tickStep * 4) * 100) / 100, size: 850,  total: 1300, depthPercent: 22 },
    { price: Math.round((p - tickStep * 5) * 100) / 100, size: 450,  total: 450,  depthPercent: 10 },
  ];
  const asks = [
    { price: Math.round((p + tickStep * 1) * 100) / 100, size: 1300, total: 1300, depthPercent: 20 },
    { price: Math.round((p + tickStep * 2) * 100) / 100, size: 1700, total: 3000, depthPercent: 48 },
    { price: Math.round((p + tickStep * 3) * 100) / 100, size: 2100, total: 5100, depthPercent: 78 },
    { price: Math.round((p + tickStep * 4) * 100) / 100, size: 1150, total: 6250, depthPercent: 92 },
    { price: Math.round((p + tickStep * 5) * 100) / 100, size: 850,  total: 7100, depthPercent: 100 },
  ];

  return {
    symbol,
    bids,
    asks,
    spread,
    spreadPercent: Math.round((spread / p) * 10000) / 100,
    midPrice: p,
    lastUpdated: new Date().toLocaleTimeString(),
  };
};

export const getPredictionForSymbol = (symbol: string, price: number): TFTPrediction => {
  const isBull = symbol !== 'TSLA';
  return {
    symbol,
    prediction: isBull ? 'BUY' : 'SELL',
    marketTrend: isBull ? 'Bullish' : 'Bearish',
    confidence: isBull ? 82.6 : 74.2,
    probabilityDistribution: {
      down: isBull ? 4.1 : 74.2,
      stable: isBull ? 13.3 : 18.5,
      up: isBull ? 82.6 : 7.3,
    },
    horizon: '24H',
    modelVersion: 'TFT-v2.4.2-Prod',
    lastUpdated: new Date().toLocaleTimeString(),
    featureWeights: [
      { feature: 'Order Book Imbalance (L2)', importance: 0.34 },
      { feature: 'FinBERT News Sentiment', importance: 0.28 },
      { feature: 'Multi-Horizon Attention', importance: 0.21 },
      { feature: 'Realized Volatility 24H', importance: 0.11 },
      { feature: 'Macro Index Correlation', importance: 0.06 },
    ],
    expectedPriceRange: {
      low: Math.round((price * 0.985) * 100) / 100,
      target: Math.round((price * 1.018) * 100) / 100,
      high: Math.round((price * 1.032) * 100) / 100,
    },
  };
};

export const INITIAL_PREDICTION: TFTPrediction = getPredictionForSymbol('AAPL', 188.72);
export const INITIAL_ORDER_BOOK: OrderBookData = generateOrderBookForPrice(188.72, 'AAPL');

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
  const ticker = getTickerForSymbol(symbol);
  const candles = generateCandles(symbol, ticker.price);
  const orderBook = generateOrderBookForPrice(ticker.price, symbol);
  const prediction = getPredictionForSymbol(symbol, ticker.price);
  const news = INITIAL_NEWS.map((n, i) => ({
    ...n,
    id: `mock-news-${symbol}-${i}`,
    ticker: symbol,
  }));

  return {
    ticker,
    candles,
    prediction,
    orderBook,
    news,
    insight: {
      ...INITIAL_INSIGHT,
      summary: `Market trend for ${symbol} is ${(prediction.marketTrend || 'Bullish').toLowerCase()} with positive sentiment. Multi-horizon attention validates strong volume support.`,
    },
    modelPerformance: INITIAL_MODEL_PERFORMANCE,
    systemHealth: INITIAL_SYSTEM_HEALTH,
    indices: INITIAL_INDICES,
    isSimulationMode: false,
  };
};

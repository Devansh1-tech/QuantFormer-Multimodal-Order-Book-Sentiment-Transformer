import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';
import { DashboardResponse, CandleData } from '../types';
import { getMockDashboard } from '../services/mockData';

export function useDashboardData(symbol = 'AAPL') {
  const [liveData, setLiveData] = useState<DashboardResponse | null>(() => getMockDashboard(symbol));

  // Instantly switch dashboard metrics when selected symbol changes
  useEffect(() => {
    setLiveData(getMockDashboard(symbol));
  }, [symbol]);

  const query = useQuery({
    queryKey: ['dashboard', symbol],
    queryFn: () => api.getDashboard(symbol),
    refetchInterval: 10000,
    staleTime: 4000,
    retry: 2,
  });

  // Sync query data when live backend returns fresh data for the active symbol
  const queryData = query.data;
  useEffect(() => {
    if (queryData && queryData.ticker.symbol.toUpperCase() === symbol.toUpperCase()) {
      setLiveData(queryData);
    }
  }, [queryData, symbol]);

  // Real-time market tick jitter & dynamic candlestick formation
  useEffect(() => {
    let tickCounter = 0;
    const interval = setInterval(() => {
      setLiveData((prev) => {
        if (!prev) return prev;
        
        // Micro tick scaled to price of asset
        const priceScale = Math.max(0.02, prev.ticker.price * 0.00035);
        const delta = (Math.random() - 0.48) * priceScale * 2;
        const newPrice = Math.round((prev.ticker.price + delta) * 100) / 100;
        const prevClose = prev.ticker.previousClose || (newPrice - prev.ticker.change);
        const newChange = Math.round((newPrice - prevClose) * 100) / 100;
        const newChangePct = prevClose > 0 ? Math.round((newChange / prevClose) * 10000) / 100 : 0;

        // Dynamic candle update & live formation
        const updatedCandles = [...prev.candles];
        tickCounter++;

        if (updatedCandles.length > 0) {
          // Every ~15 ticks (~18 seconds), close previous candle and dynamically form a NEW candle!
          if (tickCounter >= 15) {
            tickCounter = 0;
            const now = new Date();
            const timeStr = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
            
            const newCandle: CandleData = {
              time: timeStr,
              open: newPrice,
              high: newPrice,
              low: newPrice,
              close: newPrice,
              volume: Math.round(15000 + Math.random() * 25000),
            };
            if (updatedCandles.length >= 80) {
              updatedCandles.shift();
            }
            updatedCandles.push(newCandle);
          } else {
            // Actively update current candle's high, low, close, and volume
            const lastIdx = updatedCandles.length - 1;
            const last = { ...updatedCandles[lastIdx] };
            last.close = newPrice;
            last.high = Math.max(last.high, newPrice);
            last.low = Math.min(last.low, newPrice);
            last.volume = (last.volume || 10000) + Math.round(Math.random() * 300 + 40);
            updatedCandles[lastIdx] = last;
          }
        }

        // Jitter top-of-book depth slightly
        const updatedBids = [...prev.orderBook.bids];
        if (updatedBids[0]) {
          updatedBids[0] = {
            ...updatedBids[0],
            price: Math.round((newPrice - 0.02) * 100) / 100,
            size: Math.max(800, Math.min(2500, updatedBids[0].size + Math.floor((Math.random() - 0.5) * 60))),
          };
        }

        const updatedAsks = [...prev.orderBook.asks];
        if (updatedAsks[0]) {
          updatedAsks[0] = {
            ...updatedAsks[0],
            price: Math.round((newPrice + 0.02) * 100) / 100,
            size: Math.max(900, Math.min(2400, updatedAsks[0].size + Math.floor((Math.random() - 0.5) * 60))),
          };
        }

        return {
          ...prev,
          ticker: {
            ...prev.ticker,
            price: newPrice,
            change: newChange,
            changePercent: newChangePct,
            high: Math.max(prev.ticker.high, newPrice),
            low: Math.min(prev.ticker.low, newPrice),
          },
          candles: updatedCandles,
          orderBook: {
            ...prev.orderBook,
            midPrice: newPrice,
            bids: updatedBids,
            asks: updatedAsks,
          },
        };
      });
    }, 1200);

    return () => clearInterval(interval);
  }, [symbol]);

  // Fetch live news stream every 3.5s
  useEffect(() => {
    const fetchNews = async () => {
      try {
        const liveNews = await api.getLiveNews(3, symbol);
        if (liveNews?.success && liveNews.articles) {
          const newNewsItems = liveNews.articles.map((art: any, idx: number) => ({
            id: art.url || `live-news-${Date.now()}-${idx}`,
            headline: art.headline,
            publisher: art.source || 'FinancialPhraseBank',
            publishedAt: art.published_at ? 'Just now' : 'Just now',
            ticker: symbol,
            sentiment: art.sentiment,
            confidence: art.confidence,
            summary: art.description,
            url: art.url,
            finbertScores: art.finbert_scores,
          }));
          
          setLiveData((prev) => {
             if (!prev) return prev;
             // Prepend new news and keep top 10
             const mergedNews = [...newNewsItems, ...prev.news].slice(0, 10);
             return { ...prev, news: mergedNews };
          });
        }
      } catch (err) {
        console.warn('Failed to fetch live news stream', err);
      }
    };
    
    // Call immediately on mount/symbol change
    fetchNews();
    
    const interval = setInterval(fetchNews, 3500);
    return () => clearInterval(interval);
  }, [symbol]);

  return {
    data: liveData || query.data,
    isLoading: query.isLoading && !liveData,
    isError: query.isError,
    error: query.error,
    isFetching: query.isFetching,
    refetch: query.refetch,
    isLiveBackend: query.data ? !query.data.isSimulationMode : false,
  };
}

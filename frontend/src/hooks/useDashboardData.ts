import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';
import { DashboardResponse } from '../types';

export function useDashboardData(symbol = 'AAPL') {
  const [liveData, setLiveData] = useState<DashboardResponse | null>(null);

  const query = useQuery({
    queryKey: ['dashboard', symbol],
    queryFn: () => api.getDashboard(symbol),
    refetchInterval: 10000,
    staleTime: 5000,
    retry: 2,
  });

  // Sync initial query data whenever query data updates
  const queryData = query.data;
  useEffect(() => {
    if (queryData) {
      setTimeout(() => setLiveData(queryData), 0);
    }
  }, [queryData]);

  // Subtle real-time market tick jitter to simulate high-frequency institutional feed
  useEffect(() => {
    const interval = setInterval(() => {
      setLiveData((prev) => {
        if (!prev) return prev;
        
        // Random micro tick between -0.04 and +0.05
        const delta = (Math.random() - 0.48) * 0.06;
        const newPrice = Math.round((prev.ticker.price + delta) * 100) / 100;
        const newChange = Math.round((newPrice - prev.ticker.previousClose) * 100) / 100;
        const newChangePct = Math.round((newChange / prev.ticker.previousClose) * 10000) / 100;

        // Jitter top-of-book depth slightly
        const updatedBids = [...prev.orderBook.bids];
        if (updatedBids[0]) {
          updatedBids[0] = {
            ...updatedBids[0],
            size: Math.max(800, Math.min(2500, updatedBids[0].size + Math.floor((Math.random() - 0.5) * 60))),
          };
        }

        const updatedAsks = [...prev.orderBook.asks];
        if (updatedAsks[0]) {
          updatedAsks[0] = {
            ...updatedAsks[0],
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
          orderBook: {
            ...prev.orderBook,
            bids: updatedBids,
            asks: updatedAsks,
          },
        };
      });
    }, 3000);

    return () => clearInterval(interval);
  }, []);

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

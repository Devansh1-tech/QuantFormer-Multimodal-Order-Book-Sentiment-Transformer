import React, { useState } from 'react';
import { Sidebar } from './components/layout/Sidebar';
import { TopNavbar } from './components/layout/TopNavbar';
import { BottomTicker } from './components/layout/BottomTicker';
import { MetricCardsGrid } from './components/dashboard/MetricCardsGrid';
import { MainPriceChart } from './components/dashboard/MainPriceChart';
import { PredictionGauge } from './components/dashboard/PredictionGauge';
import { OrderBookCard } from './components/dashboard/OrderBookCard';
import { NewsSentimentCard } from './components/dashboard/NewsSentimentCard';
import { ModelPerformanceCard } from './components/dashboard/ModelPerformanceCard';

// Secondary views
import { MarketOverviewView } from './components/views/MarketOverviewView';
import { PredictionsView } from './components/views/PredictionsView';
import { BacktestingView } from './components/views/BacktestingView';
import { ReportsView } from './components/views/ReportsView';
import { ModelsView } from './components/views/ModelsView';
import { SettingsView } from './components/views/SettingsView';

// Modals
import { SentimentAnalysisModal } from './components/modals/SentimentAnalysisModal';
import { ExplainPredictionModal } from './components/modals/ExplainPredictionModal';
import { TickerSearchModal } from './components/modals/TickerSearchModal';

import { useDashboardData } from './hooks/useDashboardData';
import { NewsItem } from './types';
import { RefreshCw, AlertCircle } from 'lucide-react';

export function App() {
  const [currentSymbol, setCurrentSymbol] = useState('AAPL');
  const [activeTab, setActiveTab] = useState('dashboard');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  // Modals state
  const [selectedNews, setSelectedNews] = useState<NewsItem | null>(null);
  const [sentimentModalOpen, setSentimentModalOpen] = useState(false);
  const [explainModalOpen, setExplainModalOpen] = useState(false);
  const [searchModalOpen, setSearchModalOpen] = useState(false);

  const { data, isLoading, isError, isLiveBackend, refetch } = useDashboardData(currentSymbol);

  const handleSelectNews = (item: NewsItem) => {
    setSelectedNews(item);
    setSentimentModalOpen(true);
  };

  if (isLoading && !data) {
    return (
      <div className="flex items-center justify-center h-screen bg-[#080c14] text-white flex-col gap-4">
        <div className="relative w-12 h-12">
          <div className="absolute inset-0 rounded-xl bg-gradient-to-tr from-cyan-500 to-indigo-600 animate-spin opacity-75 blur-sm" />
          <div className="relative w-full h-full rounded-xl bg-[#0d1322] border border-indigo-500 flex items-center justify-center">
            <span className="text-xs font-mono font-bold text-cyan-400">QF</span>
          </div>
        </div>
        <div className="text-sm font-semibold tracking-wider text-slate-300 flex items-center gap-2">
          <span>Initializing QuantFormer Financial Intelligence</span>
          <span className="animate-pulse">...</span>
        </div>
      </div>
    );
  }

  if (isError && !data) {
    return (
      <div className="flex items-center justify-center h-screen bg-[#080c14] text-white p-6">
        <div className="max-w-md p-6 rounded-2xl bg-[#0d1424] border border-[#1f2b45] text-center space-y-4 shadow-2xl">
          <div className="w-12 h-12 rounded-full bg-rose-500/20 border border-rose-500/40 text-rose-400 flex items-center justify-center mx-auto">
            <AlertCircle size={24} />
          </div>
          <h2 className="text-lg font-bold text-white">Connection Error</h2>
          <p className="text-xs text-slate-300 leading-relaxed">
            Unable to load dashboard intelligence. The system can retry or automatically launch in simulation mode.
          </p>
          <button
            onClick={() => refetch()}
            className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold flex items-center justify-center gap-2 w-full transition-all"
          >
            <RefreshCw size={14} />
            <span>Retry Connection</span>
          </button>
        </div>
      </div>
    );
  }

  // Guaranteed fallback data
  const safeData = data!;

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#080c14] text-slate-100 font-sans">
      {/* Left Sidebar */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        collapsed={sidebarCollapsed}
        setCollapsed={setSidebarCollapsed}
        systemHealth={safeData.systemHealth}
        insight={safeData.insight}
        onOpenExplainModal={() => setExplainModalOpen(true)}
      />

      {/* Main Workspace (Top Navbar + Dashboard Content + Bottom Ticker) */}
      <div className="flex flex-col flex-1 min-w-0 h-screen overflow-hidden">
        {/* Top Navbar */}
        <TopNavbar
          currentSymbol={currentSymbol}
          isLiveBackend={isLiveBackend}
          onSelectSymbol={setCurrentSymbol}
          onToggleSidebar={() => setSidebarCollapsed(!sidebarCollapsed)}
          onOpenSearchModal={() => setSearchModalOpen(true)}
        />

        {/* Scrollable Center Main Area */}
        <main className="flex-1 overflow-y-auto px-4 md:px-5 py-4 space-y-4 scrollbar-none bg-gradient-to-b from-[#090d16] to-[#060911]">
          {activeTab === 'dashboard' && (
            <div className="space-y-4">
              {/* Row 1: Top 5 Metric Cards */}
              <MetricCardsGrid
                ticker={safeData.ticker}
                prediction={safeData.prediction}
                onPredictionClick={() => setExplainModalOpen(true)}
              />

              {/* Row 2: Main Price Chart + QuantFormer Prediction Gauge */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
                {/* Left 2 Cols: Main Price Chart */}
                <div className="lg:col-span-2">
                  <MainPriceChart
                    ticker={safeData.ticker}
                    candles={safeData.candles}
                  />
                </div>

                {/* Right 1 Col: QuantFormer Prediction Speedometer */}
                <div className="lg:col-span-1">
                  <PredictionGauge
                    prediction={safeData.prediction}
                    onOpenExplainModal={() => setExplainModalOpen(true)}
                  />
                </div>
              </div>

              {/* Row 3: Market News & Sentiment (Left) + Order Book & Model Performance (Right) */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
                {/* Left 2 Cols: Market News & Sentiment Feed */}
                <div className="lg:col-span-2">
                  <NewsSentimentCard
                    news={safeData.news}
                    onSelectNews={handleSelectNews}
                    onViewAll={() => setActiveTab('news')}
                  />
                </div>

                {/* Right 1 Col: Stacked Order Book & Model Performance Cards */}
                <div className="lg:col-span-1 space-y-4">
                  {/* Order Book (Level 2) */}
                  <OrderBookCard orderBook={safeData.orderBook} />

                  {/* Model Performance */}
                  <ModelPerformanceCard performance={safeData.modelPerformance} />
                </div>
              </div>
            </div>
          )}

          {activeTab === 'market' && (
            <MarketOverviewView onSelectTicker={(sym) => {
              setCurrentSymbol(sym);
              setActiveTab('dashboard');
            }} />
          )}

          {activeTab === 'orderbook' && (
            <div className="space-y-4 animate-in fade-in duration-200">
              <h2 className="text-xl font-bold text-white">Full Level 2 Depth & Liquidity Matrix</h2>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                <OrderBookCard orderBook={safeData.orderBook} />
                <div className="p-6 rounded-2xl bg-[#0c1322] border border-[#18233c] space-y-3">
                  <h3 className="text-sm font-bold text-white">Kafka L2 Streaming Feed Stats</h3>
                  <div className="text-xs text-slate-300 space-y-2 font-mono">
                    <div className="flex justify-between py-1 border-b border-slate-800">
                      <span>Stream Broker:</span>
                      <span className="text-emerald-400">Connected (Live)</span>
                    </div>
                    <div className="flex justify-between py-1 border-b border-slate-800">
                      <span>Exchange Feed:</span>
                      <span className="text-slate-200">NASDAQ TotalView ITCH 5.0</span>
                    </div>
                    <div className="flex justify-between py-1 border-b border-slate-800">
                      <span>Message Throughput:</span>
                      <span className="text-cyan-300">1,480 msgs/sec</span>
                    </div>
                    <div className="flex justify-between py-1 border-b border-slate-800">
                      <span>Pipeline Latency:</span>
                      <span className="text-emerald-400">1.2ms</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'news' && (
            <div className="space-y-4 animate-in fade-in duration-200">
              <h2 className="text-xl font-bold text-white">FinBERT Real-Time Financial News Stream</h2>
              <NewsSentimentCard
                news={safeData.news}
                onSelectNews={handleSelectNews}
              />
            </div>
          )}

          {activeTab === 'predictions' && (
            <PredictionsView
              prediction={safeData.prediction}
              insight={safeData.insight}
              onOpenExplain={() => setExplainModalOpen(true)}
            />
          )}

          {activeTab === 'backtesting' && <BacktestingView />}

          {activeTab === 'reports' && <ReportsView />}

          {activeTab === 'models' && (
            <ModelsView performance={safeData.modelPerformance} />
          )}

          {activeTab === 'settings' && <SettingsView />}
        </main>

        {/* Bottom Ticker Footer */}
        <BottomTicker indices={safeData.indices} />
      </div>

      {/* Interactive Modals */}
      <SentimentAnalysisModal
        newsItem={selectedNews}
        isOpen={sentimentModalOpen}
        onClose={() => setSentimentModalOpen(false)}
        currentTicker={currentSymbol}
      />

      <ExplainPredictionModal
        prediction={safeData.prediction}
        insight={safeData.insight}
        isOpen={explainModalOpen}
        onClose={() => setExplainModalOpen(false)}
      />

      <TickerSearchModal
        isOpen={searchModalOpen}
        onClose={() => setSearchModalOpen(false)}
        onSelectTicker={setCurrentSymbol}
      />
    </div>
  );
}

export default App;

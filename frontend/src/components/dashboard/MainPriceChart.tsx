import React, { useState, useEffect, useRef } from 'react';
import { 
  SlidersHorizontal, 
  Maximize2, 
  Camera, 
  Plus, 
  Settings2
} from 'lucide-react';
import { CandleData, TickerInfo } from '../../types';

interface MainPriceChartProps {
  ticker: TickerInfo;
  candles: CandleData[];
}

export const MainPriceChart: React.FC<MainPriceChartProps> = ({
  ticker,
  candles,
}) => {
  const [timeframe, setTimeframe] = useState<'1D' | '5D' | '1M' | '3M' | '6M' | '1Y' | 'All'>('1D');
  const [showIndicators, setShowIndicators] = useState(false);
  const [activeIndicators, setActiveIndicators] = useState({
    ema20: true,
    ema50: false,
    volume: true,
    bollinger: false,
  });

  const [hoveredCandle, setHoveredCandle] = useState<CandleData | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const timeframes: ('1D' | '5D' | '1M' | '3M' | '6M' | '1Y' | 'All')[] = [
    '1D', '5D', '1M', '3M', '6M', '1Y', 'All'
  ];

  // Active display OHLC values (either hovered candle or latest ticker)
  const currentO = hoveredCandle ? hoveredCandle.open : ticker.open;
  const currentH = hoveredCandle ? hoveredCandle.high : ticker.high;
  const currentL = hoveredCandle ? hoveredCandle.low : ticker.low;
  const currentC = hoveredCandle ? hoveredCandle.close : ticker.price;
  const currentChg = currentC - (hoveredCandle ? hoveredCandle.open : ticker.previousClose);
  const currentChgPct = ((currentChg / (hoveredCandle ? hoveredCandle.open : ticker.previousClose)) * 100);

  // Render high-precision Candlesticks & Volume onto HTML5 Canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Handle high DPI displays
    const rect = canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);

    const width = rect.width;
    const height = rect.height;
    const paddingRight = 65; // For price scale
    const paddingBottom = 28; // For date labels
    const paddingTop = 15;
    const chartWidth = width - paddingRight;
    const chartHeight = height - paddingBottom - paddingTop;
    const volumeHeight = chartHeight * 0.22;
    const priceChartHeight = chartHeight - volumeHeight;

    ctx.clearRect(0, 0, width, height);

    if (candles.length === 0) return;

    // Price extremes
    let minPrice = Math.min(...candles.map((c) => c.low));
    let maxPrice = Math.max(...candles.map((c) => c.high));
    const pricePadding = (maxPrice - minPrice) * 0.08 || 2;
    minPrice -= pricePadding;
    maxPrice += pricePadding;
    const priceRange = maxPrice - minPrice;

    // Volume max
    const maxVol = Math.max(...candles.map((c) => c.volume || 1));

    // Coordinate helpers
    const getY = (price: number) => {
      return paddingTop + (1 - (price - minPrice) / priceRange) * priceChartHeight;
    };

    const getVolY = (vol: number) => {
      return paddingTop + priceChartHeight + (1 - vol / maxVol) * volumeHeight;
    };

    // Draw grid horizontal lines and price labels
    const stepCount = 7;
    ctx.font = '10.5px JetBrains Mono, monospace';
    ctx.fillStyle = '#64748b';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';

    for (let i = 0; i <= stepCount; i++) {
      const price = minPrice + (priceRange * (stepCount - i)) / stepCount;
      const y = getY(price);

      // Grid line
      ctx.strokeStyle = 'rgba(30, 41, 59, 0.45)';
      ctx.lineWidth = 1;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(chartWidth, y);
      ctx.stroke();

      // Right axis price text
      ctx.fillText(price.toFixed(2), chartWidth + 10, y);
    }
    ctx.setLineDash([]);

    // Candle layout
    const numCandles = candles.length;
    const candleSlotWidth = chartWidth / numCandles;
    const candleBodyWidth = Math.max(2, candleSlotWidth * 0.65);

    // Calculate EMA 20 if enabled
    const emaPoints: { x: number; y: number }[] = [];
    let k = 2 / (20 + 1);
    let ema = candles[0].close;

    candles.forEach((c, idx) => {
      ema = c.close * k + ema * (1 - k);
      const x = idx * candleSlotWidth + candleSlotWidth / 2;
      emaPoints.push({ x, y: getY(ema) });
    });

    // Draw Candlesticks & Volume Bars
    candles.forEach((c, idx) => {
      const xCenter = idx * candleSlotWidth + candleSlotWidth / 2;
      const isUp = c.close >= c.open;
      const color = isUp ? '#10b981' : '#ef4444';
      const volColor = isUp ? 'rgba(16, 185, 129, 0.4)' : 'rgba(239, 68, 68, 0.4)';

      // 1. Volume Bar
      if (activeIndicators.volume) {
        const vY = getVolY(c.volume);
        const vH = (paddingTop + chartHeight) - vY;
        ctx.fillStyle = volColor;
        ctx.fillRect(xCenter - candleBodyWidth / 2, vY, candleBodyWidth, Math.max(1, vH));
      }

      // 2. High-Low Wick
      const yHigh = getY(c.high);
      const yLow = getY(c.low);
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(xCenter, yHigh);
      ctx.lineTo(xCenter, yLow);
      ctx.stroke();

      // 3. Open-Close Body
      const yOpen = getY(c.open);
      const yClose = getY(c.close);
      const bodyTop = Math.min(yOpen, yClose);
      const bodyHeight = Math.max(2, Math.abs(yClose - yOpen));

      ctx.fillStyle = color;
      ctx.fillRect(xCenter - candleBodyWidth / 2, bodyTop, candleBodyWidth, bodyHeight);
    });

    // Draw EMA 20 Line
    if (activeIndicators.ema20 && emaPoints.length > 0) {
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 1.8;
      ctx.beginPath();
      emaPoints.forEach((pt, idx) => {
        if (idx === 0) ctx.moveTo(pt.x, pt.y);
        else ctx.lineTo(pt.x, pt.y);
      });
      ctx.stroke();
    }

    // Horizontal Current Price dashed line & Right badge ($188.72)
    const currentY = getY(ticker.price);
    ctx.strokeStyle = '#10b981';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([3, 3]);
    ctx.beginPath();
    ctx.moveTo(0, currentY);
    ctx.lineTo(chartWidth, currentY);
    ctx.stroke();
    ctx.setLineDash([]);

    // Price badge on the right axis
    ctx.fillStyle = '#10b981';
    const badgeW = 56;
    const badgeH = 18;
    ctx.beginPath();
    ctx.roundRect(chartWidth + 6, currentY - badgeH / 2, badgeW, badgeH, 4);
    ctx.fill();

    ctx.fillStyle = '#080c14';
    ctx.font = 'bold 10.5px JetBrains Mono, monospace';
    ctx.textAlign = 'center';
    ctx.fillText(ticker.price.toFixed(2), chartWidth + 6 + badgeW / 2, currentY + 1);

    // Month & Day X-axis Labels (Feb, Mar, Apr, May, 20)
    ctx.font = '11px sans-serif';
    ctx.fillStyle = '#64748b';
    ctx.textAlign = 'center';
    const xLabels = [
      { label: 'Feb', pos: 0.15 },
      { label: 'Mar', pos: 0.38 },
      { label: 'Apr', pos: 0.62 },
      { label: 'May', pos: 0.85 },
      { label: '20',  pos: 0.98 },
    ];
    xLabels.forEach((lbl) => {
      ctx.fillText(lbl.label, chartWidth * lbl.pos, height - 8);
    });

  }, [candles, ticker.price, activeIndicators]);

  // Handle mouse move for crosshairs
  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas || candles.length === 0) return;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const chartWidth = rect.width - 65;
    const candleSlotWidth = chartWidth / candles.length;
    const idx = Math.floor(x / candleSlotWidth);
    if (idx >= 0 && idx < candles.length) {
      setHoveredCandle(candles[idx]);
    }
  };

  const handleMouseLeave = () => {
    setHoveredCandle(null);
  };

  return (
    <div 
      ref={containerRef}
      className="p-5 rounded-2xl bg-[#0c1322]/85 backdrop-blur-md border border-[#18233c] shadow-[0_8px_32px_rgba(0,0,0,0.4)] flex flex-col justify-between"
    >
      {/* Chart Top Header & Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-[#162035]">
        {/* Title and Timeframe Buttons */}
        <div className="flex items-center gap-4">
          <div className="text-base font-bold text-white tracking-wide">
            {ticker.symbol} Price Chart
          </div>

          {/* Timeframe pill selector */}
          <div className="flex items-center bg-[#0a0f1d] p-1 rounded-xl border border-[#1a253d] text-xs font-semibold">
            {timeframes.map((tf) => (
              <button
                key={tf}
                onClick={() => setTimeframe(tf)}
                className={`px-2.5 py-1 rounded-lg transition-all ${
                  timeframe === tf
                    ? 'bg-indigo-600 text-white shadow-[0_0_12px_rgba(99,102,241,0.5)]'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {tf}
              </button>
            ))}
          </div>
        </div>

        {/* Toolbar Tools: Indicators, Compare, Settings, Fullscreen, Camera */}
        <div className="flex items-center gap-2 text-xs">
          {/* Indicators dropdown toggle */}
          <div className="relative">
            <button
              onClick={() => setShowIndicators(!showIndicators)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl border transition-all ${
                showIndicators || activeIndicators.ema20
                  ? 'bg-indigo-950/60 border-indigo-500/50 text-indigo-300'
                  : 'bg-[#0e1626] border-[#1e2a44] text-slate-300 hover:text-white'
              }`}
            >
              <SlidersHorizontal size={13} />
              <span>Indicators</span>
            </button>

            {showIndicators && (
              <>
                <div className="fixed inset-0 z-20" onClick={() => setShowIndicators(false)} />
                <div className="absolute right-0 mt-2 w-48 p-2 rounded-xl bg-[#0d1424] border border-[#1f2b45] shadow-2xl z-30 space-y-1">
                  <div className="text-[11px] font-semibold text-slate-400 px-2 py-1 uppercase">
                    Overlay Indicators
                  </div>
                  <label className="flex items-center justify-between px-2.5 py-1.5 rounded-lg hover:bg-slate-800/60 cursor-pointer text-xs text-slate-300">
                    <span>EMA 20 (Trend)</span>
                    <input 
                      type="checkbox" 
                      checked={activeIndicators.ema20} 
                      onChange={(e) => setActiveIndicators(prev => ({ ...prev, ema20: e.target.checked }))}
                      className="rounded accent-indigo-500"
                    />
                  </label>
                  <label className="flex items-center justify-between px-2.5 py-1.5 rounded-lg hover:bg-slate-800/60 cursor-pointer text-xs text-slate-300">
                    <span>Volume Histogram</span>
                    <input 
                      type="checkbox" 
                      checked={activeIndicators.volume} 
                      onChange={(e) => setActiveIndicators(prev => ({ ...prev, volume: e.target.checked }))}
                      className="rounded accent-indigo-500"
                    />
                  </label>
                </div>
              </>
            )}
          </div>

          <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#0e1626] border border-[#1e2a44] text-slate-300 hover:text-white transition-colors">
            <Plus size={13} />
            <span>Compare</span>
          </button>

          <button 
            className="p-1.5 rounded-xl bg-[#0e1626] border border-[#1e2a44] text-slate-400 hover:text-white transition-colors"
            title="Chart Settings"
          >
            <Settings2 size={15} />
          </button>

          <button 
            className="p-1.5 rounded-xl bg-[#0e1626] border border-[#1e2a44] text-slate-400 hover:text-white transition-colors"
            title="Fullscreen Chart"
          >
            <Maximize2 size={15} />
          </button>

          <button 
            className="p-1.5 rounded-xl bg-[#0e1626] border border-[#1e2a44] text-slate-400 hover:text-white transition-colors"
            title="Take Snapshot"
          >
            <Camera size={15} />
          </button>
        </div>
      </div>

      {/* OHLC Bar (matching screenshot: O 187.71  H 189.15  L 187.10  C 188.72  +2.35 (+1.26%)) */}
      <div className="flex items-center gap-4 py-2 text-xs font-mono">
        <div className="flex items-center gap-1.5">
          <span className="text-slate-400">O</span>
          <span className="text-emerald-400 font-semibold">{currentO.toFixed(2)}</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="text-slate-400">H</span>
          <span className="text-emerald-400 font-semibold">{currentH.toFixed(2)}</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="text-slate-400">L</span>
          <span className="text-emerald-400 font-semibold">{currentL.toFixed(2)}</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="text-slate-400">C</span>
          <span className="text-emerald-400 font-semibold">{currentC.toFixed(2)}</span>
        </div>
        <div className={`font-semibold ${currentChg >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
          {currentChg >= 0 ? '+' : ''}{currentChg.toFixed(2)} ({currentChg >= 0 ? '+' : ''}{currentChgPct.toFixed(2)}%)
        </div>
      </div>

      {/* Canvas Chart Area */}
      <div className="relative w-full h-[320px] lg:h-[350px]">
        <canvas 
          ref={canvasRef} 
          onMouseMove={handleMouseMove}
          onMouseLeave={handleMouseLeave}
          className="w-full h-full cursor-crosshair block"
        />
      </div>
    </div>
  );
};

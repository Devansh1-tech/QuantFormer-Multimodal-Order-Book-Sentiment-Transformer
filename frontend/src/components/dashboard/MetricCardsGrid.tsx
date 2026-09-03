import React from 'react';
import { motion } from 'framer-motion';
import { TickerInfo, TFTPrediction } from '../../types';

interface MetricCardsGridProps {
  ticker: TickerInfo;
  prediction: TFTPrediction;
  onPredictionClick?: () => void;
}

export const MetricCardsGrid: React.FC<MetricCardsGridProps> = ({
  ticker,
  prediction,
  onPredictionClick,
}) => {
  const isUp = ticker.change >= 0;
  const isPredBullish = prediction.prediction === 'Bullish' || prediction.prediction === 'BUY' || (prediction.marketTrend === 'Bullish');

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3.5">
      {/* 1. Current Price */}
      <motion.div 
        whileHover={{ y: -2, transition: { duration: 0.15 } }}
        className="p-4 rounded-2xl bg-[#0c1322]/85 backdrop-blur-md border border-[#18233c] hover:border-indigo-500/40 shadow-[0_4px_24px_rgba(0,0,0,0.35)] transition-all flex flex-col justify-between"
      >
        <div className="text-[12px] font-medium text-slate-400">Current Price</div>
        <div className="flex items-center justify-between mt-2">
          <div>
            <div className="text-2xl font-bold font-mono text-white tracking-tight">
              ${ticker.price.toFixed(2)}
            </div>
            <div className={`flex items-center gap-1 mt-1 text-[11.5px] font-mono font-medium ${isUp ? 'text-emerald-400' : 'text-rose-400'}`}>
              <span>{isUp ? '↑' : '↓'} {isUp ? '+' : ''}{ticker.change.toFixed(2)} ({isUp ? '+' : ''}{ticker.changePercent.toFixed(2)}%)</span>
            </div>
          </div>

          {/* Mini sparkline */}
          <div className="w-20 h-10">
            <svg viewBox="0 0 100 40" className="w-full h-full overflow-visible">
              <defs>
                <linearGradient id="priceSparkGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor={isUp ? "#10b981" : "#ef4444"} stopOpacity="0.4" />
                  <stop offset="100%" stopColor={isUp ? "#10b981" : "#ef4444"} stopOpacity="0.0" />
                </linearGradient>
              </defs>
              <path
                d={isUp ? "M0,32 Q15,30 30,24 T60,20 T80,12 L100,6" : "M0,6 Q15,12 30,18 T60,24 T80,30 L100,34"}
                fill="none"
                stroke={isUp ? "#10b981" : "#ef4444"}
                strokeWidth="2.5"
                strokeLinecap="round"
              />
              <circle cx="100" cy={isUp ? "6" : "34"} r="3" fill={isUp ? "#10b981" : "#ef4444"} className="animate-pulse" />
            </svg>
          </div>
        </div>
      </motion.div>

      {/* 2. 24h Change */}
      <motion.div 
        whileHover={{ y: -2, transition: { duration: 0.15 } }}
        className={`p-4 rounded-2xl bg-[#0c1322]/85 backdrop-blur-md border border-[#18233c] hover:border-${isUp ? 'emerald' : 'rose'}-500/40 shadow-[0_4px_24px_rgba(0,0,0,0.35)] transition-all flex flex-col justify-between`}
      >
        <div className="text-[12px] font-medium text-slate-400">24h Change</div>
        <div className="flex items-center justify-between mt-2">
          <div>
            <div className={`text-2xl font-bold font-mono tracking-tight ${isUp ? 'text-emerald-400' : 'text-rose-400'}`}>
              {isUp ? '+' : ''}{ticker.changePercent.toFixed(2)}%
            </div>
            <div className={`flex items-center gap-1 mt-1 text-[11.5px] font-mono font-medium ${isUp ? 'text-emerald-400' : 'text-rose-400'}`}>
              <span>{isUp ? '↑ +' : '↓ '}{ticker.change.toFixed(2)}</span>
            </div>
          </div>

          {/* Area Wave Sparkline */}
          <div className="w-20 h-10">
            <svg viewBox="0 0 100 40" className="w-full h-full overflow-visible">
              <defs>
                <linearGradient id="changeSparkArea" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor={isUp ? "#10b981" : "#ef4444"} stopOpacity="0.35" />
                  <stop offset="100%" stopColor={isUp ? "#10b981" : "#ef4444"} stopOpacity="0.0" />
                </linearGradient>
              </defs>
              <path
                d={isUp ? "M0,28 C20,28 30,18 50,22 C70,26 80,10 100,4 L100,40 L0,40 Z" : "M0,10 C20,12 30,22 50,20 C70,18 80,30 100,36 L100,40 L0,40 Z"}
                fill="url(#changeSparkArea)"
              />
              <path
                d={isUp ? "M0,28 C20,28 30,18 50,22 C70,26 80,10 100,4" : "M0,10 C20,12 30,22 50,20 C70,18 80,30 100,36"}
                fill="none"
                stroke={isUp ? "#10b981" : "#ef4444"}
                strokeWidth="2"
                strokeLinecap="round"
              />
            </svg>
          </div>
        </div>
      </motion.div>

      {/* 3. Volume */}
      <motion.div 
        whileHover={{ y: -2, transition: { duration: 0.15 } }}
        className="p-4 rounded-2xl bg-[#0c1322]/85 backdrop-blur-md border border-[#18233c] hover:border-cyan-500/40 shadow-[0_4px_24px_rgba(0,0,0,0.35)] transition-all flex flex-col justify-between"
      >
        <div className="text-[12px] font-medium text-slate-400">Volume</div>
        <div className="flex items-center justify-between mt-2">
          <div>
            <div className="text-2xl font-bold font-mono text-white tracking-tight">
              {ticker.volume}
            </div>
            <div className="mt-1 text-[11.5px] font-mono text-slate-400">
              Avg. {ticker.avgVolume}
            </div>
          </div>

          {/* Mini Blue/Cyan Bar Chart */}
          <div className="w-16 h-10 flex items-end justify-between gap-1">
            {[35, 50, 75, 45, 60, 85, 95, 70].map((h, i) => (
              <div 
                key={i} 
                className="w-1.5 rounded-t bg-cyan-500/80 hover:bg-cyan-400 transition-colors"
                style={{ height: `${h}%` }}
              />
            ))}
          </div>
        </div>
      </motion.div>

      {/* 4. Volatility (24h) */}
      <motion.div 
        whileHover={{ y: -2, transition: { duration: 0.15 } }}
        className="p-4 rounded-2xl bg-[#0c1322]/85 backdrop-blur-md border border-[#18233c] hover:border-purple-500/40 shadow-[0_4px_24px_rgba(0,0,0,0.35)] transition-all flex flex-col justify-between"
      >
        <div className="text-[12px] font-medium text-slate-400">Volatility (24h)</div>
        <div className="flex items-center justify-between mt-2">
          <div>
            <div className="text-2xl font-bold font-mono text-white tracking-tight">
              {ticker.volatility.toFixed(2)}%
            </div>
            <div className="flex items-center gap-1 mt-1 text-[11.5px] font-mono font-medium text-rose-400">
              <span>↓ {ticker.volatilityChange}%</span>
            </div>
          </div>

          {/* Purple Mini Wave */}
          <div className="w-20 h-10">
            <svg viewBox="0 0 100 40" className="w-full h-full overflow-visible">
              <path
                d="M0,15 Q25,35 50,18 T100,25"
                fill="none"
                stroke="#a855f7"
                strokeWidth="2.2"
                strokeLinecap="round"
              />
            </svg>
          </div>
        </div>
      </motion.div>

      {/* 5. Prediction (Next Move) */}
      <motion.div 
        whileHover={{ y: -2, transition: { duration: 0.15 } }}
        onClick={onPredictionClick}
        className="p-4 rounded-2xl bg-[#0c1322]/85 backdrop-blur-md border border-[#18233c] hover:border-emerald-500/50 shadow-[0_4px_24px_rgba(16,185,129,0.12)] transition-all flex flex-col justify-between cursor-pointer group"
      >
        <div className="text-[12px] font-medium text-slate-400">Prediction (Next Move)</div>
        <div className="flex items-center justify-between mt-2">
          <div>
            <div className={`text-2xl font-black font-sans tracking-wide drop-shadow-[0_0_12px_rgba(16,185,129,0.4)] ${isPredBullish ? 'text-emerald-400' : 'text-rose-400'}`}>
              {prediction.prediction}
            </div>
            <div className="mt-1 text-[11px] font-medium text-slate-300">
              Confidence: <span className="font-mono text-emerald-300 font-semibold">{prediction.confidence}%</span>
            </div>
          </div>

          {/* Circular Progress Meter */}
          <div className="relative w-12 h-12 flex items-center justify-center shrink-0">
            <svg className="w-full h-full -rotate-90" viewBox="0 0 36 36">
              {/* Background ring */}
              <circle
                cx="18"
                cy="18"
                r="15"
                fill="none"
                stroke="#182338"
                strokeWidth="3.5"
              />
              {/* Foreground arc */}
              <circle
                cx="18"
                cy="18"
                r="15"
                fill="none"
                stroke={isPredBullish ? "#10b981" : "#ef4444"}
                strokeWidth="3.5"
                strokeDasharray="94.2"
                strokeDashoffset={94.2 - (94.2 * prediction.confidence) / 100}
                strokeLinecap="round"
                className="transition-all duration-1000 ease-out drop-shadow-[0_0_6px_#10b981]"
              />
            </svg>
            <span className="absolute text-[10.5px] font-mono font-bold text-white">
              {prediction.confidence}%
            </span>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

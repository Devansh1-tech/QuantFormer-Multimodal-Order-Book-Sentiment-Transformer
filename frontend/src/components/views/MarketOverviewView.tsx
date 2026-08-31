import React from 'react';
import { Globe } from 'lucide-react';
import { AVAILABLE_TICKERS, INITIAL_INDICES } from '../../services/mockData';

export const MarketOverviewView: React.FC<{ onSelectTicker: (sym: string) => void }> = ({ onSelectTicker }) => {
  return (
    <div className="space-y-6 pb-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Globe size={22} className="text-indigo-400" />
            Global Market Overview
          </h2>
          <p className="text-xs text-slate-400">
            Cross-asset intelligence, multi-exchange liquidity, and macro volatility telemetry
          </p>
        </div>
      </div>

      {/* Major Indices Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {INITIAL_INDICES.map((idx, i) => (
          <div key={i} className="p-3.5 rounded-2xl bg-[#0c1322]/85 border border-[#18233c] shadow-md">
            <div className="text-xs text-slate-400 font-medium">{idx.name}</div>
            <div className="text-lg font-bold font-mono text-white mt-1">{idx.value}</div>
            <div className={`text-xs font-mono mt-1 ${idx.isPositive ? 'text-emerald-400' : 'text-rose-400'}`}>
              {idx.isPositive ? '↑ ' : '↓ '}{idx.change}
            </div>
          </div>
        ))}
      </div>

      {/* Asset Class Matrix */}
      <div className="p-5 rounded-2xl bg-[#0c1322]/85 border border-[#18233c] shadow-lg space-y-4">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider">
          Monitored Equities & Assets
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {AVAILABLE_TICKERS.map((t) => (
            <div
              key={t.symbol}
              onClick={() => onSelectTicker(t.symbol)}
              className="p-4 rounded-xl bg-[#0a101e] border border-[#18233a] hover:border-indigo-500/50 hover:bg-[#121c32] cursor-pointer transition-all flex items-center justify-between group"
            >
              <div className="flex items-center gap-3">
                <span className="text-2xl">{t.icon}</span>
                <div>
                  <div className="font-mono font-bold text-white group-hover:text-indigo-300">
                    {t.symbol}
                  </div>
                  <div className="text-xs text-slate-400">{t.name}</div>
                </div>
              </div>
              <div className="text-right font-mono">
                <div className="text-sm font-bold text-white">${t.price.toFixed(2)}</div>
                <div className={`text-xs ${t.change >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                  {t.change >= 0 ? '+' : ''}{t.changePercent}%
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

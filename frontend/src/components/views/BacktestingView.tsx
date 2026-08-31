import React from 'react';
import { History } from 'lucide-react';

export const BacktestingView: React.FC = () => {
  return (
    <div className="space-y-6 pb-6 animate-in fade-in duration-200">
      <div>
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <History size={22} className="text-indigo-400" />
          Quantitative Backtesting Engine
        </h2>
        <p className="text-xs text-slate-400">
          Historical validation of TFT predictions & FinBERT sentiment signal strategies
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-3.5">
        <div className="p-4 rounded-2xl bg-[#0c1322]/85 border border-[#18233c]">
          <div className="text-xs text-slate-400">Cumulative Alpha</div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">+34.8%</div>
          <div className="text-[11px] text-slate-400 mt-0.5">vs Benchmark +14.2%</div>
        </div>
        <div className="p-4 rounded-2xl bg-[#0c1322]/85 border border-[#18233c]">
          <div className="text-xs text-slate-400">Sharpe Ratio</div>
          <div className="text-2xl font-bold font-mono text-indigo-300 mt-1">2.41</div>
          <div className="text-[11px] text-slate-400 mt-0.5">Risk-adjusted return</div>
        </div>
        <div className="p-4 rounded-2xl bg-[#0c1322]/85 border border-[#18233c]">
          <div className="text-xs text-slate-400">Max Drawdown</div>
          <div className="text-2xl font-bold font-mono text-rose-400 mt-1">-5.2%</div>
          <div className="text-[11px] text-slate-400 mt-0.5">Peak to trough</div>
        </div>
        <div className="p-4 rounded-2xl bg-[#0c1322]/85 border border-[#18233c]">
          <div className="text-xs text-slate-400">Win Rate</div>
          <div className="text-2xl font-bold font-mono text-cyan-300 mt-1">72.6%</div>
          <div className="text-[11px] text-slate-400 mt-0.5">482 trade signals</div>
        </div>
      </div>
    </div>
  );
};

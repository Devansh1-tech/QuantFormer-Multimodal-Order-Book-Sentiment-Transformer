import React from 'react';
import { MarketIndexTicker } from '../../types';
import { INITIAL_INDICES } from '../../services/mockData';

interface BottomTickerProps {
  indices?: MarketIndexTicker[];
}

export const BottomTicker: React.FC<BottomTickerProps> = ({ indices = INITIAL_INDICES }) => {
  // Duplicate array for seamless infinite marquee loop
  const tickerItems = [...indices, ...indices, ...indices];

  return (
    <footer className="h-9 bg-[#060911] border-t border-[#151e30] flex items-center justify-between px-4 text-xs select-none z-20 overflow-hidden shrink-0">
      {/* Marquee ticker container */}
      <div className="flex-1 overflow-hidden relative">
        <div className="animate-marquee flex items-center gap-8 whitespace-nowrap">
          {tickerItems.map((item, idx) => (
            <div key={`${item.name}-${idx}`} className="flex items-center gap-2 font-mono text-[11px]">
              <span className="font-semibold text-slate-300 font-sans">{item.name}</span>
              <span className="text-slate-100">{item.value}</span>
              <span className={`font-semibold ${item.isPositive ? 'text-emerald-400' : 'text-rose-400'}`}>
                {item.isPositive ? '↑ ' : '↓ '}{item.change}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Yahoo Finance Attribution badge matching screenshot */}
      <div className="shrink-0 pl-4 border-l border-slate-800/80 flex items-center gap-1.5 text-[11px] text-slate-400 font-sans">
        <span>Data provided by</span>
        <span className="font-bold text-purple-400 hover:text-purple-300 transition-colors">
          yahoo<span className="text-pink-500">!</span>finance
        </span>
      </div>
    </footer>
  );
};

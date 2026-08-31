import React from 'react';
import { OrderBookData } from '../../types';

interface OrderBookCardProps {
  orderBook: OrderBookData;
}

export const OrderBookCard: React.FC<OrderBookCardProps> = ({ orderBook }) => {
  return (
    <div className="p-5 rounded-2xl bg-[#0c1322]/85 backdrop-blur-md border border-[#18233c] shadow-[0_8px_32px_rgba(0,0,0,0.4)] flex flex-col justify-between">
      {/* Header */}
      <div className="flex items-center justify-between pb-2.5 border-b border-[#162035]">
        <div className="text-base font-bold text-white tracking-wide">
          Order Book (Level 2)
        </div>
      </div>

      {/* Section Subheaders: BIDS vs ASKS */}
      <div className="grid grid-cols-2 gap-4 text-xs font-semibold pt-2 pb-1 border-b border-[#141c2e]">
        <div className="flex items-center justify-between text-emerald-400">
          <span className="font-bold">BIDS</span>
        </div>
        <div className="flex items-center justify-between text-rose-400 text-right">
          <span className="w-full text-right font-bold">ASKS</span>
        </div>
      </div>

      {/* Column Headers */}
      <div className="grid grid-cols-2 gap-4 text-[11px] text-slate-500 font-mono py-1">
        <div className="flex items-center justify-between pr-2">
          <span>Price</span>
          <span>Size</span>
          <span>Total</span>
        </div>
        <div className="flex items-center justify-between pl-2">
          <span>Price</span>
          <span>Size</span>
          <span>Total</span>
        </div>
      </div>

      {/* Level 2 Rows with Mirrored Center Depth Bars matching screenshot */}
      <div className="space-y-1 my-1 text-xs font-mono">
        {orderBook.bids.map((bid, idx) => {
          const ask = orderBook.asks[idx] || orderBook.asks[0];
          return (
            <div key={idx} className="grid grid-cols-2 gap-4 items-center relative py-0.5 hover:bg-slate-800/30 rounded px-1 transition-colors">
              {/* Bid row (Green) */}
              <div className="relative flex items-center justify-between pr-2">
                <span className="text-emerald-400 font-semibold z-10">{bid.price.toFixed(2)}</span>
                <span className="text-slate-300 z-10">{bid.size.toLocaleString()}</span>
                <span className="text-slate-400 text-[11px] z-10">{bid.total.toLocaleString()}</span>

                {/* Depth bar indicator extending from right to left */}
                <div 
                  className="absolute right-0 top-0 bottom-0 bg-emerald-500/20 rounded-l transition-all duration-300 pointer-events-none"
                  style={{ width: `${bid.depthPercent}%` }}
                />
              </div>

              {/* Ask row (Red) */}
              <div className="relative flex items-center justify-between pl-2">
                <span className="text-rose-400 font-semibold z-10">{ask.price.toFixed(2)}</span>
                <span className="text-slate-300 z-10">{ask.size.toLocaleString()}</span>
                <span className="text-slate-400 text-[11px] z-10">{ask.total.toLocaleString()}</span>

                {/* Depth bar indicator extending from left to right */}
                <div 
                  className="absolute left-0 top-0 bottom-0 bg-rose-500/20 rounded-r transition-all duration-300 pointer-events-none"
                  style={{ width: `${ask.depthPercent}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>

      {/* Footer Spread matching screenshot: Spread: 0.03 (0.02%) */}
      <div className="pt-2 border-t border-[#162035] text-center text-xs font-mono text-slate-400">
        Spread: <span className="text-slate-200 font-semibold">{orderBook.spread.toFixed(2)}</span> ({orderBook.spreadPercent.toFixed(2)}%)
      </div>
    </div>
  );
};

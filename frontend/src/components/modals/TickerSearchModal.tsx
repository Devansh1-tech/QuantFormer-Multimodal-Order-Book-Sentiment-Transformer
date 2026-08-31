import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, X, TrendingUp, TrendingDown } from 'lucide-react';
import { AVAILABLE_TICKERS } from '../../services/mockData';

interface TickerSearchModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectTicker: (symbol: string) => void;
}

export const TickerSearchModal: React.FC<TickerSearchModalProps> = ({
  isOpen,
  onClose,
  onSelectTicker,
}) => {
  const [query, setQuery] = useState('');

  const filteredTickers = AVAILABLE_TICKERS.filter((t) =>
    t.symbol.toLowerCase().includes(query.toLowerCase()) ||
    t.name.toLowerCase().includes(query.toLowerCase())
  );

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        {/* Backdrop */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="fixed inset-0 bg-black/80 backdrop-blur-md"
        />

        {/* Modal Window */}
        <motion.div
          initial={{ scale: 0.95, opacity: 0, y: 15 }}
          animate={{ scale: 1, opacity: 1, y: 0 }}
          exit={{ scale: 0.95, opacity: 0, y: 15 }}
          className="relative w-full max-w-lg rounded-2xl bg-[#0d1424] border border-[#1f2d4a] shadow-2xl p-5 z-10 space-y-4"
        >
          {/* Search Input */}
          <div className="relative flex items-center">
            <Search size={18} className="absolute left-3.5 text-slate-400" />
            <input
              type="text"
              autoFocus
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search ticker or company (AAPL, NVDA, MSFT...)"
              className="w-full pl-10 pr-10 py-3 rounded-xl bg-[#080d18] border border-[#1e2a44] focus:border-indigo-500 text-sm text-white placeholder-slate-500 outline-none font-sans"
            />
            <button
              onClick={onClose}
              className="absolute right-3 text-slate-400 hover:text-white"
            >
              <X size={18} />
            </button>
          </div>

          {/* Results List */}
          <div className="space-y-1.5 max-h-80 overflow-y-auto scrollbar-none">
            {filteredTickers.map((t) => (
              <button
                key={t.symbol}
                onClick={() => {
                  onSelectTicker(t.symbol);
                  onClose();
                }}
                className="w-full flex items-center justify-between p-3 rounded-xl bg-[#0a101e] hover:bg-[#131d33] border border-transparent hover:border-indigo-500/30 transition-all text-left group"
              >
                <div className="flex items-center gap-3">
                  <span className="text-xl">{t.icon}</span>
                  <div>
                    <div className="font-mono font-bold text-white group-hover:text-indigo-300 transition-colors">
                      {t.symbol}
                    </div>
                    <div className="text-xs text-slate-400">{t.name}</div>
                  </div>
                </div>

                <div className="text-right font-mono">
                  <div className="text-sm font-semibold text-white">${t.price.toFixed(2)}</div>
                  <div className={`text-xs flex items-center justify-end gap-0.5 ${t.change >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                    {t.change >= 0 ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
                    <span>{t.change >= 0 ? '+' : ''}{t.changePercent}%</span>
                  </div>
                </div>
              </button>
            ))}

            {filteredTickers.length === 0 && (
              <div className="py-8 text-center text-slate-500 text-xs">
                No matching financial instruments found.
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};

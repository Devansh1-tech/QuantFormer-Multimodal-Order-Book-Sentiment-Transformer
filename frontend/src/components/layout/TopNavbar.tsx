import React, { useState, useEffect } from 'react';
import { 
  Menu, 
  ChevronDown, 
  Bell, 
  Moon, 
  Sun, 
  Search, 
  Clock 
} from 'lucide-react';
import { AVAILABLE_TICKERS } from '../../services/mockData';

interface TopNavbarProps {
  currentSymbol: string;
  isLiveBackend?: boolean;
  onSelectSymbol: (symbol: string) => void;
  onToggleSidebar?: () => void;
  onOpenSearchModal: () => void;
}

export const TopNavbar: React.FC<TopNavbarProps> = ({
  currentSymbol,
  isLiveBackend = true,
  onSelectSymbol,
  onToggleSidebar,
  onOpenSearchModal,
}) => {
  const [timeStr, setTimeStr] = useState('10:45:32 AM');
  const [dateStr, setDateStr] = useState('May 20, 2025');
  const [tickerDropdownOpen, setTickerDropdownOpen] = useState(false);
  const [themeDark, setThemeDark] = useState(true);

  // Real-time ticking clock matching institutional terminal
  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setTimeStr(now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true }));
      setDateStr(now.toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' }));
    };
    updateTime();
    const timer = setInterval(updateTime, 1000);
    return () => clearInterval(timer);
  }, []);

  const activeTicker = AVAILABLE_TICKERS.find((t) => t.symbol === currentSymbol) || {
    symbol: currentSymbol,
    name: `${currentSymbol} Equity`,
    exchange: 'NASDAQ',
    price: 188.72,
    change: 2.35,
    changePercent: 1.26,
    icon: '📈',
  };

  return (
    <header className="h-16 px-4 md:px-6 bg-[#080d17]/95 backdrop-blur-md border-b border-[#151e30] flex items-center justify-between z-20 shrink-0">
      {/* Left side: Hamburger + Ticker & Exchange Selector */}
      <div className="flex items-center gap-3">
        <button 
          onClick={onToggleSidebar}
          className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/60 transition-colors"
          title="Toggle Navigation"
        >
          <Menu size={18} />
        </button>

        {/* Ticker Dropdown Selector */}
        <div className="relative">
          <button
            onClick={() => setTickerDropdownOpen(!tickerDropdownOpen)}
            className="flex items-center gap-2.5 px-3 py-1.5 rounded-xl bg-[#0e1626] border border-[#1e2a44] hover:border-indigo-500/50 hover:bg-[#121c32] text-sm font-semibold text-white shadow-sm transition-all group"
          >
            <span className="text-base">{activeTicker.icon}</span>
            <span className="tracking-wide font-mono">{activeTicker.symbol}</span>
            <ChevronDown size={14} className={`text-slate-400 transition-transform ${tickerDropdownOpen ? 'rotate-180' : ''}`} />
          </button>

          {/* Dropdown Menu */}
          {tickerDropdownOpen && (
            <>
              <div 
                className="fixed inset-0 z-30" 
                onClick={() => setTickerDropdownOpen(false)} 
              />
              <div className="absolute top-full left-0 mt-2 w-64 rounded-xl bg-[#0d1424] border border-[#1f2b45] shadow-2xl p-2 z-40 backdrop-blur-xl animate-in fade-in zoom-in-95 duration-150">
                <div className="text-[11px] font-semibold text-slate-400 px-2.5 py-1 uppercase tracking-wider">
                  Select Instrument
                </div>
                <div className="space-y-1 mt-1 max-h-60 overflow-y-auto scrollbar-none">
                  {AVAILABLE_TICKERS.map((t) => (
                    <button
                      key={t.symbol}
                      onClick={() => {
                        onSelectSymbol(t.symbol);
                        setTickerDropdownOpen(false);
                      }}
                      className={`w-full flex items-center justify-between px-2.5 py-2 rounded-lg text-xs font-medium transition-all ${
                        t.symbol === currentSymbol
                          ? 'bg-indigo-600/20 text-indigo-200 border border-indigo-500/40'
                          : 'text-slate-300 hover:bg-slate-800/60'
                      }`}
                    >
                      <div className="flex items-center gap-2">
                        <span>{t.icon}</span>
                        <div className="text-left">
                          <div className="font-mono font-semibold text-white">{t.symbol}</div>
                          <div className="text-[10px] text-slate-400 truncate max-w-[100px]">{t.name}</div>
                        </div>
                      </div>
                      <div className="text-right font-mono text-xs">
                        <div>${t.price.toFixed(2)}</div>
                        <div className={t.change >= 0 ? 'text-emerald-400 text-[10px]' : 'text-rose-400 text-[10px]'}>
                          {t.change >= 0 ? '+' : ''}{t.changePercent}%
                        </div>
                      </div>
                    </button>
                  ))}
                </div>

                <button
                  onClick={() => {
                    setTickerDropdownOpen(false);
                    onOpenSearchModal();
                  }}
                  className="w-full mt-2 pt-2 border-t border-slate-800/80 flex items-center justify-center gap-1.5 text-xs text-indigo-400 hover:text-indigo-300 py-1 font-medium"
                >
                  <Search size={12} />
                  <span>Search All Instruments</span>
                </button>
              </div>
            </>
          )}
        </div>

        {/* Live Backend vs Simulation Mode Badge */}
        <div 
          className={`hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-full border text-[11px] font-semibold transition-all ${
            isLiveBackend
              ? 'bg-emerald-950/40 text-emerald-300 border-emerald-500/40 shadow-[0_0_10px_rgba(16,185,129,0.15)]'
              : 'bg-amber-950/40 text-amber-300 border-amber-500/40 shadow-[0_0_10px_rgba(245,158,11,0.15)]'
          }`}
          title={isLiveBackend ? "Connected to FastAPI Backend at http://localhost:8000" : "Backend offline, running in High-Fidelity Simulation Mode"}
        >
          <span className={`w-2 h-2 rounded-full ${isLiveBackend ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`} />
          <span>{isLiveBackend ? 'Live Backend' : 'Simulation Mode'}</span>
        </div>
      </div>

      {/* Center / Right info: Market Status + Digital Clock + Actions */}
      <div className="flex items-center gap-3 md:gap-5">
        {/* Market Status */}
        <div className="hidden lg:flex items-center gap-2.5 px-3.5 py-1.5 rounded-full bg-[#0c1422]/90 border border-[#17243c]">
          <span className="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_#34d399] status-dot-pulse" />
          <div className="flex items-center gap-2 text-xs">
            <span className="font-semibold text-slate-200">Market Open</span>
            <span className="text-[11px] text-slate-400 font-mono">Closes in 05:06:32</span>
          </div>
        </div>

        {/* Real-time Institutional Clock & Date */}
        <div className="text-right font-mono hidden sm:block">
          <div className="text-xs font-semibold text-slate-200 tracking-wider flex items-center justify-end gap-1.5">
            <Clock size={12} className="text-indigo-400" />
            {timeStr}
          </div>
          <div className="text-[10.5px] text-slate-400 font-sans">{dateStr}</div>
        </div>

        {/* Action icons: Notifications & Theme toggle */}
        <div className="flex items-center gap-1.5 md:gap-2 border-l border-[#1b263e] pl-3 md:pl-4">
          <button 
            onClick={onOpenSearchModal}
            className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/60 transition-colors"
            title="Search Instruments"
          >
            <Search size={16} />
          </button>

          <button 
            className="relative p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/60 transition-colors"
            title="Market Alerts"
          >
            <Bell size={16} />
            <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 rounded-full bg-indigo-500 shadow-[0_0_6px_#6366f1]" />
          </button>

          <button 
            onClick={() => setThemeDark(!themeDark)}
            className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/60 transition-colors"
            title="Toggle theme"
          >
            {themeDark ? <Moon size={16} className="text-indigo-400" /> : <Sun size={16} className="text-amber-400" />}
          </button>
        </div>
      </div>
    </header>
  );
};

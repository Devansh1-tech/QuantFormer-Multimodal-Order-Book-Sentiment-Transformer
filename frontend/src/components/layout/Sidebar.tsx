import React from 'react';
import { 
  LayoutDashboard, 
  Globe, 
  BookOpen, 
  Newspaper, 
  Sparkles, 
  History, 
  FileText, 
  Brain, 
  Settings, 
  ChevronDown,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { SystemHealthStatus, AIInsightData } from '../../types';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  collapsed: boolean;
  setCollapsed: (collapsed: boolean) => void;
  systemHealth?: SystemHealthStatus;
  insight?: AIInsightData;
  onOpenExplainModal?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  setActiveTab,
  collapsed,
  setCollapsed,
  systemHealth,
  insight,
  onOpenExplainModal,
}) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'market', label: 'Market Overview', icon: Globe },
    { id: 'orderbook', label: 'Order Book', icon: BookOpen },
    { id: 'news', label: 'News & Sentiment', icon: Newspaper },
    { id: 'predictions', label: 'Predictions', icon: Sparkles },
    { id: 'backtesting', label: 'Backtesting', icon: History },
    { id: 'reports', label: 'Reports', icon: FileText },
    { id: 'models', label: 'Model Performance', icon: Brain },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  const isHealthy = systemHealth?.status === 'Operational' || systemHealth?.status === 'healthy';

  return (
    <aside 
      className={`relative flex flex-col justify-between h-screen bg-[#070b13] border-r border-[#151d2f] transition-all duration-300 select-none z-30 shrink-0 ${
        collapsed ? 'w-20' : 'w-[260px]'
      }`}
    >
      {/* Top Header Logo */}
      <div className="p-4 border-b border-[#151d2f]/60 flex items-center justify-between">
        <div className="flex items-center gap-3 overflow-hidden cursor-pointer" onClick={() => setActiveTab('dashboard')}>
          <div className="relative w-9 h-9 flex items-center justify-center rounded-xl bg-gradient-to-tr from-cyan-500/20 via-indigo-500/20 to-purple-600/30 border border-indigo-500/40 shadow-glow-purple shrink-0">
            <svg className="w-6 h-6" viewBox="0 0 32 32" fill="none">
              <path d="M16 3 L28 10 L28 22 L16 29 L4 22 L4 10 Z" stroke="url(#sidebarLogoGrad)" strokeWidth="2" fill="rgba(99, 102, 241, 0.1)"/>
              <path d="M16 10 L23 14 L23 20 L16 24 L9 20 L9 14 Z" stroke="#38bdf8" strokeWidth="1.5"/>
              <circle cx="16" cy="17" r="2.5" fill="#a855f7" className="animate-pulse"/>
              <defs>
                <linearGradient id="sidebarLogoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#06b6d4"/>
                  <stop offset="50%" stopColor="#6366f1"/>
                  <stop offset="100%" stopColor="#a855f7"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          
          <AnimatePresence>
            {!collapsed && (
              <motion.div 
                initial={{ opacity: 0, x: -10 }} 
                animate={{ opacity: 1, x: 0 }} 
                exit={{ opacity: 0, x: -10 }}
                className="flex flex-col"
              >
                <span className="text-lg font-bold tracking-tight text-white font-sans flex items-center gap-1.5">
                  QuantFormer
                </span>
                <span className="text-[10.5px] font-medium text-slate-400 tracking-tight whitespace-nowrap">
                  AI-Powered Market Intelligence
                </span>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        <button 
          onClick={() => setCollapsed(!collapsed)}
          className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/60 transition-colors"
          title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {collapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
        </button>
      </div>

      {/* Navigation Links */}
      <div className="flex-1 overflow-y-auto py-3 px-3 space-y-1 scrollbar-none">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-3.5 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all group relative ${
                isActive
                  ? 'text-white font-semibold bg-gradient-to-r from-indigo-600/90 to-purple-600/80 shadow-[0_0_20px_rgba(99,102,241,0.4)] border border-indigo-400/30'
                  : 'text-slate-400 hover:text-slate-100 hover:bg-[#121a2c]/60'
              }`}
              title={collapsed ? item.label : undefined}
            >
              <Icon 
                size={18} 
                className={`shrink-0 transition-colors ${
                  isActive ? 'text-white' : 'text-slate-400 group-hover:text-indigo-300'
                }`} 
              />
              
              {!collapsed && (
                <span className="truncate">{item.label}</span>
              )}

              {isActive && (
                <motion.div 
                  layoutId="activePillGlow"
                  className="absolute right-2 w-1.5 h-1.5 rounded-full bg-cyan-300 shadow-[0_0_8px_#38bdf8]"
                />
              )}
            </button>
          );
        })}
      </div>

      {/* Bottom Area: AI Insight Card, System Status, User Card */}
      <div className="p-3 space-y-2.5 border-t border-[#151d2f]/60">
        {/* AI Insight Sidebar Card */}
        {!collapsed && (
          <div 
            onClick={onOpenExplainModal}
            className="p-3 rounded-xl bg-gradient-to-br from-[#201138]/90 via-[#151128]/80 to-[#0c1222]/90 border border-purple-500/30 shadow-[0_4px_20px_rgba(168,85,247,0.15)] cursor-pointer hover:border-purple-400/50 transition-all group"
          >
            <div className="flex items-center gap-2 mb-1.5">
              <div className="p-1 rounded-lg bg-purple-500/20 text-purple-300 border border-purple-500/30">
                <Brain size={15} className="text-purple-400 group-hover:rotate-12 transition-transform" />
              </div>
              <span className="text-xs font-semibold text-purple-200">AI Insight</span>
            </div>
            <p className="text-[11px] leading-relaxed text-purple-100/80 line-clamp-3">
              {insight?.summary || 'Market trend is bullish with positive news sentiment. High-confidence multi-horizon transformer alignment detected.'}
            </p>
          </div>
        )}

        {/* System Status connected to live backend */}
        {!collapsed ? (
          <div className="p-3 rounded-xl bg-[#0c1220]/70 border border-[#172136] space-y-2 text-xs">
            <div className="flex items-center justify-between text-slate-300 font-medium">
              <span className="text-[11.5px]">System Status</span>
            </div>
            <div className="flex items-center gap-2 text-[11px] font-medium text-emerald-400">
              <span className={`w-2 h-2 rounded-full ${isHealthy ? 'bg-emerald-400 shadow-[0_0_8px_#34d399]' : 'bg-amber-400'} status-dot-pulse`}></span>
              {isHealthy ? 'All Systems Operational' : 'Degraded (Simulation)'}
            </div>

            <div className="grid grid-cols-2 gap-y-1.5 pt-1 text-[10.5px] border-t border-slate-800/60">
              <div className="flex items-center justify-between pr-2 text-slate-400">
                <span>API Status</span>
                <span className="text-emerald-400 font-mono font-medium">{systemHealth?.apiStatus || 'Online'}</span>
              </div>
              <div className="flex items-center justify-between pl-2 border-l border-slate-800/60 text-slate-400">
                <span>Kafka Stream</span>
                <span className="text-emerald-400 font-mono font-medium">{systemHealth?.kafkaStream || 'Connected'}</span>
              </div>
              <div className="flex items-center justify-between pr-2 text-slate-400">
                <span>Models</span>
                <span className="text-emerald-400 font-mono font-medium">{systemHealth?.models || 'Loaded'}</span>
              </div>
              <div className="flex items-center justify-between pl-2 border-l border-slate-800/60 text-slate-400">
                <span>Data Feeds</span>
                <span className="text-emerald-400 font-mono font-medium">{systemHealth?.dataFeeds || 'Live'}</span>
              </div>
            </div>
          </div>
        ) : (
          <div className="flex justify-center p-2 rounded-xl bg-[#0c1220] border border-[#172136]" title="All Systems Operational">
            <span className={`w-2.5 h-2.5 rounded-full ${isHealthy ? 'bg-emerald-400 shadow-[0_0_8px_#34d399]' : 'bg-amber-400'} status-dot-pulse`}></span>
          </div>
        )}

        {/* User Card */}
        <div className="flex items-center justify-between p-2 rounded-xl bg-[#0c1220]/90 border border-[#172136] hover:bg-[#131b2e] transition-colors cursor-pointer">
          <div className="flex items-center gap-2.5 overflow-hidden">
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-600 to-purple-600 flex items-center justify-center text-xs font-bold text-white shadow-inner shrink-0 border border-indigo-400/30">
              QF
            </div>
            {!collapsed && (
              <div className="truncate text-left">
                <div className="text-xs font-semibold text-slate-200 truncate">Quant Trader</div>
                <div className="text-[10px] text-indigo-400 font-medium">Institutional AI</div>
              </div>
            )}
          </div>
          {!collapsed && <ChevronDown size={14} className="text-slate-400 shrink-0" />}
        </div>
      </div>
    </aside>
  );
};

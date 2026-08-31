import React from 'react';
import { NewsItem } from '../../types';

interface NewsSentimentCardProps {
  news: NewsItem[];
  onSelectNews: (item: NewsItem) => void;
  onViewAll?: () => void;
}

export const NewsSentimentCard: React.FC<NewsSentimentCardProps> = ({
  news,
  onSelectNews,
  onViewAll,
}) => {
  // Publisher logo renderer matching screenshot icons
  const renderPublisherIcon = (publisher: string) => {
    switch (publisher.toLowerCase()) {
      case 'apple':
      case 'reuters':
        return (
          <div className="w-8 h-8 rounded-xl bg-[#141b2c] border border-[#202b44] flex items-center justify-center text-sm text-slate-200 shrink-0">
            🍎
          </div>
        );
      case 'bloomberg':
        return (
          <div className="w-8 h-8 rounded-xl bg-black border border-[#2d3748] flex items-center justify-center font-serif font-black text-sm text-white shrink-0">
            B
          </div>
        );
      case 'cnbc':
        return (
          <div className="w-8 h-8 rounded-xl bg-[#032046] border border-blue-600/40 flex items-center justify-center text-[10px] font-black text-rose-400 tracking-tighter shrink-0">
            CNBC
          </div>
        );
      case 'marketwatch':
        return (
          <div className="w-8 h-8 rounded-xl bg-[#004f2f] border border-emerald-500/40 flex items-center justify-center text-[11px] font-bold text-emerald-300 shrink-0">
            MW
          </div>
        );
      default:
        return (
          <div className="w-8 h-8 rounded-xl bg-[#141b2c] border border-[#202b44] flex items-center justify-center text-xs font-bold text-indigo-400 shrink-0">
            {publisher.slice(0, 2).toUpperCase()}
          </div>
        );
    }
  };

  return (
    <div className="p-5 rounded-2xl bg-[#0c1322]/85 backdrop-blur-md border border-[#18233c] shadow-[0_8px_32px_rgba(0,0,0,0.4)] flex flex-col justify-between">
      {/* Header with View All Button */}
      <div className="flex items-center justify-between pb-3 border-b border-[#162035]">
        <div className="text-base font-bold text-white tracking-wide">
          Market News & Sentiment
        </div>

        <button
          onClick={onViewAll}
          className="px-3 py-1 rounded-xl bg-[#141a2e] border border-[#232f4e] text-xs font-medium text-indigo-300 hover:text-white hover:bg-indigo-600/30 transition-all shadow-sm"
        >
          View All
        </button>
      </div>

      {/* News list */}
      <div className="divide-y divide-[#151e33] overflow-y-auto max-h-[300px] scrollbar-none">
        {news.map((item) => {
          const isPositive = item.sentiment === 'Positive';
          const isNegative = item.sentiment === 'Negative';

          return (
            <div
              key={item.id}
              onClick={() => onSelectNews(item)}
              className="py-3 px-1 flex items-center justify-between gap-4 hover:bg-slate-800/20 rounded-xl transition-all cursor-pointer group"
            >
              {/* Left: Publisher Icon + Headline + Timestamp */}
              <div className="flex items-center gap-3 min-w-0">
                {renderPublisherIcon(item.publisher)}

                <div className="min-w-0">
                  <div className="text-xs font-medium text-slate-100 group-hover:text-indigo-300 transition-colors line-clamp-1">
                    {item.headline}
                  </div>
                  <div className="text-[11px] text-slate-400 mt-0.5 flex items-center gap-1.5 font-sans">
                    <span className="font-semibold text-slate-300">{item.publisher}</span>
                    <span>•</span>
                    <span>{item.publishedAt}</span>
                  </div>
                </div>
              </div>

              {/* Right: Sentiment Badge matching screenshot */}
              <div className="shrink-0">
                <span
                  className={`px-3 py-1 rounded-full text-xs font-medium border ${
                    isPositive
                      ? 'bg-emerald-950/40 text-emerald-400 border-emerald-500/40 shadow-[0_0_10px_rgba(16,185,129,0.15)]'
                      : isNegative
                      ? 'bg-rose-950/40 text-rose-400 border-rose-500/40 shadow-[0_0_10px_rgba(239,68,68,0.15)]'
                      : 'bg-amber-950/40 text-amber-300 border-amber-500/40'
                  }`}
                >
                  {item.sentiment}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

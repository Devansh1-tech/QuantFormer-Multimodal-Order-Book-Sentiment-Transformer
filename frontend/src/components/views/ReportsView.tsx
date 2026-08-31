import React from 'react';
import { FileText, Download } from 'lucide-react';

export const ReportsView: React.FC = () => {
  const reports = [
    { title: 'AAPL Weekly TFT Forecast & Order Flow Analysis', date: 'May 20, 2025', size: '2.4 MB', type: 'PDF' },
    { title: 'Mega-Cap Technology FinBERT Sentiment Aggregation', date: 'May 19, 2025', size: '1.8 MB', type: 'PDF' },
    { title: 'Kafka Streaming Latency & Execution Benchmark', date: 'May 18, 2025', size: '4.1 MB', type: 'PDF' },
  ];

  return (
    <div className="space-y-6 pb-6 animate-in fade-in duration-200">
      <div>
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <FileText size={22} className="text-indigo-400" />
          Institutional Intelligence Reports
        </h2>
        <p className="text-xs text-slate-400">
          Automated executive summaries, risk disclosures, and model audit records
        </p>
      </div>

      <div className="space-y-3">
        {reports.map((r, i) => (
          <div key={i} className="p-4 rounded-2xl bg-[#0c1322]/85 border border-[#18233c] hover:border-indigo-500/40 flex items-center justify-between transition-all">
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">
                <FileText size={18} />
              </div>
              <div>
                <div className="text-sm font-semibold text-white">{r.title}</div>
                <div className="text-xs text-slate-400 mt-0.5">{r.date} • {r.size}</div>
              </div>
            </div>
            <button className="px-3 py-1.5 rounded-xl bg-[#141d33] border border-[#243354] text-xs font-semibold text-indigo-300 hover:text-white flex items-center gap-1.5 transition-all">
              <Download size={13} />
              <span>Export {r.type}</span>
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

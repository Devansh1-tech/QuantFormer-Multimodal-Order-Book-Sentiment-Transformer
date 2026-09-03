import React, { useState } from 'react';
import { ModelPerformanceData } from '../../types';
import { ChevronDown } from 'lucide-react';

interface ModelPerformanceCardProps {
  performance: ModelPerformanceData;
}

export const ModelPerformanceCard: React.FC<ModelPerformanceCardProps> = ({ performance }) => {
  const [selectedTimeframe, setSelectedTimeframe] = useState('7D');
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const history = performance.history;

  // Render high fidelity SVG line chart matching screenshot
  const width = 380;
  const height = 110;
  const paddingLeft = 32;
  const paddingRight = 10;
  const paddingTop = 10;
  const paddingBottom = 20;

  const chartW = width - paddingLeft - paddingRight;
  const chartH = height - paddingTop - paddingBottom;

  const getX = (idx: number) => paddingLeft + (idx / (history.length - 1)) * chartW;
  // Map 0-100% to Y coordinate
  const getY = (val: number) => paddingTop + (1 - val / 100) * chartH;

  const makePath = (key: 'accuracy' | 'precision' | 'recall' | 'f1Score') => {
    return history
      .map((pt, idx) => {
        const val = key === 'f1Score' ? pt.f1Score * 100 : (pt[key] as number);
        const x = getX(idx);
        const y = getY(val);
        return `${idx === 0 ? 'M' : 'L'} ${x.toFixed(1)} ${y.toFixed(1)}`;
      })
      .join(' ');
  };

  return (
    <div className="p-5 rounded-2xl bg-[#0c1322]/85 backdrop-blur-md border border-[#18233c] shadow-[0_8px_32px_rgba(0,0,0,0.4)] flex flex-col justify-between">
      {/* Header with 7D dropdown */}
      <div className="flex items-center justify-between pb-2 border-b border-[#162035]">
        <div className="text-base font-bold text-white tracking-wide">
          Model Performance
        </div>

        {/* Timeframe Dropdown */}
        <div className="relative">
          <button
            onClick={() => setDropdownOpen(!dropdownOpen)}
            className="flex items-center gap-1.5 px-2.5 py-1 rounded-xl bg-[#12192c] border border-[#202c46] text-xs font-semibold text-slate-300 hover:text-white"
          >
            <span>{selectedTimeframe}</span>
            <ChevronDown size={13} />
          </button>

          {dropdownOpen && (
            <>
              <div className="fixed inset-0 z-20" onClick={() => setDropdownOpen(false)} />
              <div className="absolute right-0 mt-1 w-24 rounded-xl bg-[#0d1424] border border-[#1f2b45] shadow-2xl p-1 z-30 text-xs">
                {['24H', '7D', '30D', '90D', 'ALL'].map((tf) => (
                  <button
                    key={tf}
                    onClick={() => {
                      setSelectedTimeframe(tf);
                      setDropdownOpen(false);
                    }}
                    className="w-full text-left px-2 py-1.5 rounded-lg hover:bg-slate-800 text-slate-300 hover:text-white"
                  >
                    {tf}
                  </button>
                ))}
              </div>
            </>
          )}
        </div>
      </div>

      {/* 4 Summary metric badges matching screenshot */}
      <div className="grid grid-cols-4 gap-2 pt-2 pb-1 text-center">
        <div>
          <div className="text-[11px] text-slate-400 font-medium">Accuracy</div>
          <div className="text-sm font-bold font-mono text-[#a855f7] mt-0.5">
            {performance.accuracy}%
          </div>
        </div>

        <div>
          <div className="text-[11px] text-slate-400 font-medium">F1 Score</div>
          <div className="text-sm font-bold font-mono text-[#38bdf8] mt-0.5">
            {performance.f1Score}
          </div>
        </div>

        <div>
          <div className="text-[11px] text-slate-400 font-medium">Precision</div>
          <div className="text-sm font-bold font-mono text-[#10b981] mt-0.5">
            {performance.precision}
          </div>
        </div>

        <div>
          <div className="text-[11px] text-slate-400 font-medium">Recall</div>
          <div className="text-sm font-bold font-mono text-[#f59e0b] mt-0.5">
            {performance.recall}
          </div>
        </div>
      </div>

      {/* Multi-metric Line Chart */}
      <div className="relative w-full h-[120px]">
        <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-full overflow-visible">
          {/* Y-axis Labels & Grid lines */}
          {[100, 75, 50, 25, 0].map((val) => {
            const y = getY(val);
            return (
              <g key={val}>
                <text x="24" y={y + 3} fill="#64748b" fontSize="8" textAnchor="end" fontFamily="sans-serif">
                  {val}%
                </text>
                <line
                  x1={paddingLeft}
                  y1={y}
                  x2={width - paddingRight}
                  y2={y}
                  stroke="#1b253b"
                  strokeWidth="0.8"
                  strokeDasharray="2 2"
                />
              </g>
            );
          })}

          {/* Metric Lines */}
          <path d={makePath('accuracy')} fill="none" stroke="#a855f7" strokeWidth="2" strokeLinecap="round" />
          <path d={makePath('precision')} fill="none" stroke="#38bdf8" strokeWidth="2" strokeLinecap="round" />
          <path d={makePath('recall')} fill="none" stroke="#10b981" strokeWidth="2" strokeLinecap="round" />
          <path d={makePath('f1Score')} fill="none" stroke="#f59e0b" strokeWidth="2" strokeLinecap="round" />

          {/* Data point dots on the lines */}
          {history.map((pt, idx) => (
            <g key={idx}>
              <circle cx={getX(idx)} cy={getY(pt.accuracy)} r="2.5" fill="#a855f7" />
              <circle cx={getX(idx)} cy={getY(pt.precision)} r="2.5" fill="#38bdf8" />
              <circle cx={getX(idx)} cy={getY(pt.recall)} r="2.5" fill="#10b981" />
              <circle cx={getX(idx)} cy={getY(pt.f1Score * 100)} r="2.5" fill="#f59e0b" />
            </g>
          ))}

          {/* X-axis date labels */}
          {history.map((pt, idx) => (
            <text
              key={idx}
              x={getX(idx)}
              y={height - 2}
              fill="#64748b"
              fontSize="8.5"
              textAnchor="middle"
              fontFamily="sans-serif"
            >
              {pt.date}
            </text>
          ))}
        </svg>
      </div>

      {/* Legend matching screenshot: — Accuracy   — Precision   — Recall   — F1 Score */}
      <div className="flex items-center justify-center gap-4 pt-1.5 border-t border-[#162035] text-[10.5px] text-slate-300">
        <div className="flex items-center gap-1.5">
          <span className="w-2.5 h-0.5 bg-[#a855f7] rounded-full inline-block" />
          <span>Accuracy</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-2.5 h-0.5 bg-[#38bdf8] rounded-full inline-block" />
          <span>Precision</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-2.5 h-0.5 bg-[#10b981] rounded-full inline-block" />
          <span>Recall</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-2.5 h-0.5 bg-[#f59e0b] rounded-full inline-block" />
          <span>F1 Score</span>
        </div>
      </div>
    </div>
  );
};

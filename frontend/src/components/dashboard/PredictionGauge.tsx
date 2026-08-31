import React from 'react';
import { Info } from 'lucide-react';
import { TFTPrediction } from '../../types';

interface PredictionGaugeProps {
  prediction: TFTPrediction;
  onOpenExplainModal?: () => void;
}

export const PredictionGauge: React.FC<PredictionGaugeProps> = ({
  prediction,
  onOpenExplainModal,
}) => {
  // Needle rotation calculation:
  // 0% confidence -> -90 deg (left)
  // 50% confidence -> 0 deg (top)
  // 100% confidence -> +90 deg (right)
  const needleAngle = -90 + (prediction.confidence / 100) * 180;

  return (
    <div className="p-5 rounded-2xl bg-[#0c1322]/85 backdrop-blur-md border border-[#18233c] shadow-[0_8px_32px_rgba(0,0,0,0.4)] flex flex-col justify-between relative overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between pb-2 border-b border-[#162035]">
        <div className="text-base font-bold text-white tracking-wide flex items-center gap-2">
          <span>QuantFormer Prediction</span>
        </div>

        <button
          onClick={onOpenExplainModal}
          className="p-1 rounded-lg text-slate-400 hover:text-indigo-300 hover:bg-slate-800/60 transition-colors flex items-center gap-1 text-xs"
          title="Explain TFT Model"
        >
          <Info size={14} />
        </button>
      </div>

      {/* Speedometer Arc Gauge (matching screenshot) */}
      <div className="relative flex flex-col items-center justify-center my-2">
        <div className="relative w-64 h-36 flex items-center justify-center">
          <svg viewBox="0 0 240 140" className="w-full h-full overflow-visible">
            <defs>
              {/* Arc gradient: Red -> Yellow -> Green */}
              <linearGradient id="gaugeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#ef4444" />
                <stop offset="50%" stopColor="#f59e0b" />
                <stop offset="85%" stopColor="#10b981" />
                <stop offset="100%" stopColor="#059669" />
              </linearGradient>
              <filter id="arcGlow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="3" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
              </filter>
            </defs>

            {/* Arc Track */}
            <path
              d="M 30 120 A 90 90 0 0 1 210 120"
              fill="none"
              stroke="url(#gaugeGradient)"
              strokeWidth="12"
              strokeLinecap="round"
              filter="url(#arcGlow)"
            />

            {/* Scale percentage marks: 0%, 50%, 100% */}
            <text x="18" y="130" fill="#64748b" fontSize="10" fontFamily="sans-serif" textAnchor="middle">0%</text>
            <text x="120" y="18" fill="#94a3b8" fontSize="10" fontFamily="sans-serif" textAnchor="middle">50%</text>
            <text x="222" y="130" fill="#64748b" fontSize="10" fontFamily="sans-serif" textAnchor="middle">100%</text>

            {/* Needle Pivot Center */}
            <g transform="translate(120, 120)">
              {/* Animated Needle */}
              <g 
                style={{
                  transform: `rotate(${needleAngle}deg)`,
                  transition: 'transform 1.2s cubic-bezier(0.34, 1.56, 0.64, 1)'
                }}
              >
                <line
                  x1="0"
                  y1="0"
                  x2="0"
                  y2="-85"
                  stroke="#ffffff"
                  strokeWidth="3.5"
                  strokeLinecap="round"
                  className="drop-shadow-[0_0_8px_rgba(255,255,255,0.8)]"
                />
                <circle cx="0" cy="-85" r="3" fill="#ffffff" />
              </g>
              <circle cx="0" cy="0" r="8" fill="#1e293b" stroke="#ffffff" strokeWidth="2.5" />
              <circle cx="0" cy="0" r="3.5" fill="#38bdf8" />
            </g>
          </svg>
        </div>

        {/* Center BUY Text & Confidence matching screenshot */}
        <div className="text-center -mt-4">
          <div className="text-3xl font-extrabold text-emerald-400 font-sans tracking-wider drop-shadow-[0_0_16px_rgba(16,185,129,0.6)]">
            {prediction.prediction}
          </div>
          <div className="text-xs font-semibold text-slate-200 mt-0.5">
            {prediction.confidence}% Confidence
          </div>
        </div>
      </div>

      {/* Bottom Probability Distribution Breakdown: Down / Stable / Up */}
      <div className="grid grid-cols-3 gap-2 pt-3 border-t border-[#162035] text-center">
        <div className="flex flex-col items-center">
          <span className="text-xs text-rose-400 font-semibold flex items-center gap-0.5">
            <span>↓</span> Down
          </span>
          <span className="text-sm font-mono font-bold text-rose-400 mt-0.5">
            {prediction.probabilityDistribution.down}%
          </span>
        </div>

        <div className="flex flex-col items-center border-x border-[#162035]">
          <span className="text-xs text-amber-400 font-semibold flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-400" /> Stable
          </span>
          <span className="text-sm font-mono font-bold text-amber-400 mt-0.5">
            {prediction.probabilityDistribution.stable}%
          </span>
        </div>

        <div className="flex flex-col items-center">
          <span className="text-xs text-emerald-400 font-semibold flex items-center gap-0.5">
            <span>↑</span> Up
          </span>
          <span className="text-sm font-mono font-bold text-emerald-400 mt-0.5">
            {prediction.probabilityDistribution.up}%
          </span>
        </div>
      </div>
    </div>
  );
};

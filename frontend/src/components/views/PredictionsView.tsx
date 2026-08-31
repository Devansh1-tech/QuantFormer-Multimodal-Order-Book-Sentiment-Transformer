import React from 'react';
import { Sparkles, Brain, BarChart2 } from 'lucide-react';
import { TFTPrediction, AIInsightData } from '../../types';

interface PredictionsViewProps {
  prediction: TFTPrediction;
  insight: AIInsightData;
  onOpenExplain: () => void;
}

export const PredictionsView: React.FC<PredictionsViewProps> = ({
  prediction,
  insight,
  onOpenExplain,
}) => {
  return (
    <div className="space-y-6 pb-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Sparkles size={22} className="text-indigo-400" />
            Temporal Fusion Transformer (TFT) Engine
          </h2>
          <p className="text-xs text-slate-400">
            Multi-horizon deep neural network combining recurrent layers, self-attention, and FinBERT vectors
          </p>
        </div>

        <button
          onClick={onOpenExplain}
          className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold flex items-center gap-2 transition-all shadow-[0_0_15px_rgba(99,102,241,0.4)]"
        >
          <Brain size={15} />
          <span>Explain TFT Weights</span>
        </button>
      </div>

      {/* Main Prediction Banner */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-[#11192e] via-[#16122d] to-[#0c1322] border border-indigo-500/30 shadow-2xl flex flex-col md:flex-row items-center justify-between gap-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-mono text-indigo-400 uppercase tracking-wider">
            <span>Production Forecast Horizon: {prediction.horizon}</span>
            <span>•</span>
            <span>Model: {prediction.modelVersion}</span>
          </div>
          <div className="text-4xl font-extrabold text-emerald-400 font-sans mt-2 tracking-wide flex items-center gap-3">
            {prediction.prediction}
            <span className="text-sm font-semibold px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
              {prediction.confidence}% Confidence
            </span>
          </div>
          <p className="text-xs text-slate-300 mt-2 max-w-xl leading-relaxed">
            {insight.summary}
          </p>
        </div>

        <div className="p-4 rounded-xl bg-[#090d18] border border-[#1b263e] text-center space-y-1 min-w-[200px]">
          <div className="text-xs text-slate-400">Target Range (24H)</div>
          <div className="text-xl font-bold font-mono text-white">
            ${prediction.expectedPriceRange.target.toFixed(2)}
          </div>
          <div className="text-[11px] font-mono text-emerald-400">
            Low ${prediction.expectedPriceRange.low} — High ${prediction.expectedPriceRange.high}
          </div>
        </div>
      </div>

      {/* Feature Importance Grid */}
      <div className="p-5 rounded-2xl bg-[#0c1322]/85 border border-[#18233c] shadow-lg space-y-4">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
          <BarChart2 size={16} className="text-cyan-400" />
          TFT Feature Importance & Attention Distribution
        </h3>

        <div className="space-y-3">
          {prediction.featureWeights.map((f, i) => (
            <div key={i} className="space-y-1">
              <div className="flex justify-between text-xs">
                <span className="text-slate-300 font-medium">{f.feature}</span>
                <span className="font-mono text-indigo-300 font-semibold">{(f.importance * 100).toFixed(1)}%</span>
              </div>
              <div className="w-full h-2 rounded-full bg-[#121b2d] overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-indigo-500 to-cyan-400 rounded-full"
                  style={{ width: `${f.importance * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

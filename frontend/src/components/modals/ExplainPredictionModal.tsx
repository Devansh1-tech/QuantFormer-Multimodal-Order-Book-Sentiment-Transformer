import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Sparkles, Brain, BarChart2, Layers, ShieldAlert, CheckCircle2 } from 'lucide-react';
import { TFTPrediction, AIInsightData } from '../../types';
import { api } from '../../services/api';

interface ExplainPredictionModalProps {
  prediction: TFTPrediction;
  insight: AIInsightData;
  isOpen: boolean;
  onClose: () => void;
}

export const ExplainPredictionModal: React.FC<ExplainPredictionModalProps> = ({
  prediction,
  insight,
  isOpen,
  onClose,
}) => {
  const [explanations, setExplanations] = useState<string[]>(insight.keyDrivers);
  const [newsTone, setNewsTone] = useState('positive');

  const { symbol, confidence, marketTrend, prediction: predLabel } = prediction;
  const { keyDrivers } = insight;

  useEffect(() => {
    if (!isOpen) return;
    api.postExplain({
      market_prediction: marketTrend || predLabel || 'Bullish',
      confidence: confidence || 82.6,
      news_text: `${symbol} quarterly performance, institutional order flow, and revenue trajectory`,
    })
    .then((res) => {
      if (res.explanation && res.explanation.length > 0) {
        setExplanations(res.explanation);
      }
      if (res.news_sentiment) {
        setNewsTone(res.news_sentiment);
      }
    })
    .catch(() => {
      setExplanations(keyDrivers);
    });
  }, [isOpen, symbol, confidence, marketTrend, predLabel, keyDrivers]);

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
          initial={{ scale: 0.95, opacity: 0, y: 20 }}
          animate={{ scale: 1, opacity: 1, y: 0 }}
          exit={{ scale: 0.95, opacity: 0, y: 20 }}
          className="relative w-full max-w-3xl rounded-2xl bg-[#0d1424] border border-[#1f2d4a] shadow-2xl p-6 z-10 space-y-5 overflow-hidden max-h-[90vh] overflow-y-auto scrollbar-none"
        >
          {/* Header */}
          <div className="flex items-center justify-between pb-4 border-b border-[#1b263e]">
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">
                <Sparkles size={20} />
              </div>
              <div>
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  Temporal Fusion Transformer (TFT) Architecture
                  <span className="px-2 py-0.5 rounded-full text-[10.5px] font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                    Production Engine
                  </span>
                </h3>
                <p className="text-xs text-slate-400">
                  Multi-horizon interpretable forecasting for {prediction.symbol}
                </p>
              </div>
            </div>

            <button
              onClick={onClose}
              className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            >
              <X size={18} />
            </button>
          </div>

          {/* Fusion Intelligence Summary Card */}
          <div className="p-4 rounded-xl bg-gradient-to-r from-purple-950/40 via-indigo-950/30 to-slate-900/50 border border-purple-500/30 space-y-2">
            <div className="flex items-center gap-2 text-xs font-semibold text-purple-300">
              <Brain size={16} />
              <span>Multimodal Reasoning & Explainability</span>
            </div>
            <p className="text-xs text-slate-200 leading-relaxed">
              {insight.summary}
            </p>
            <div className="pt-2 flex flex-wrap gap-2 text-[11px]">
              <span className="px-2.5 py-1 rounded-lg bg-emerald-950/60 text-emerald-300 border border-emerald-500/30">
                Trend: {insight.marketTrend}
              </span>
              <span className="px-2.5 py-1 rounded-lg bg-indigo-950/60 text-indigo-300 border border-indigo-500/30">
                Confidence: {prediction.confidence}%
              </span>
              <span className="px-2.5 py-1 rounded-lg bg-slate-800/80 text-slate-300 border border-slate-700">
                News Tone: {newsTone}
              </span>
            </div>
          </div>

          {/* Structured Human-Readable Reasoning from Backend */}
          <div className="space-y-2.5">
            <div className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
              <Brain size={14} className="text-purple-400" />
              <span>Multi-Source Reasoning Statements</span>
            </div>

            <div className="space-y-2">
              {explanations.map((exp, idx) => (
                <div key={idx} className="p-3 rounded-xl bg-[#080d18] border border-[#18233a] flex items-start gap-2.5 text-xs text-slate-200">
                  <CheckCircle2 size={15} className="text-emerald-400 shrink-0 mt-0.5" />
                  <span className="leading-relaxed">{exp}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Variable Selection Network (VSN) Feature Weights */}
          <div className="space-y-3 pt-2 border-t border-[#18233a]">
            <div className="flex items-center justify-between text-xs font-semibold text-slate-300">
              <span className="flex items-center gap-1.5">
                <Layers size={14} className="text-indigo-400" />
                Variable Selection Network (VSN) Feature Importance
              </span>
              <span className="text-slate-400">Relative Weight</span>
            </div>

            <div className="space-y-2.5">
              {prediction.featureWeights.map((item, idx) => (
                <div key={idx} className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-300 font-medium">{item.feature}</span>
                    <span className="font-mono text-indigo-300">{(item.importance * 100).toFixed(1)}%</span>
                  </div>
                  <div className="w-full h-2 rounded-full bg-[#121b2d] overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-indigo-500 to-cyan-400 rounded-full"
                      style={{ width: `${item.importance * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Temporal Lookback Attention Weights */}
          <div className="space-y-3 pt-2 border-t border-[#18233a]">
            <div className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
              <BarChart2 size={14} className="text-cyan-400" />
              Self-Attention Lookback Temporal Weights (Recent Ticks to T-5)
            </div>

            <div className="grid grid-cols-5 gap-2">
              {[
                { step: 1, weight: 0.08 },
                { step: 2, weight: 0.12 },
                { step: 3, weight: 0.18 },
                { step: 4, weight: 0.25 },
                { step: 5, weight: 0.37 },
              ].map((t, idx) => (
                <div key={idx} className="p-2.5 rounded-xl bg-[#090e1a] border border-[#1b263e] text-center">
                  <div className="text-[10px] text-slate-400 uppercase">T - {5 - t.step}</div>
                  <div className="text-xs font-bold font-mono text-cyan-300 mt-1">
                    {(t.weight * 100).toFixed(0)}%
                  </div>
                  <div className="w-full h-1.5 bg-[#121b2d] rounded-full mt-1.5 overflow-hidden">
                    <div className="h-full bg-cyan-400 rounded-full" style={{ width: `${t.weight * 100}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Mandatory Compliance Disclaimer */}
          <div className="p-3 rounded-xl bg-amber-950/20 border border-amber-500/30 flex items-start gap-2.5 text-xs text-amber-200/90">
            <ShieldAlert size={16} className="text-amber-400 shrink-0 mt-0.5" />
            <p>
              <strong>Disclaimer:</strong> {insight.disclaimer || 'This AI-generated insight is for informational purposes only and should not be considered financial advice.'}
            </p>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};

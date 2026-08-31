import React, { useState } from 'react';
import { Settings, Server, Database, Check, Activity, AlertCircle } from 'lucide-react';
import { api, client } from '../../services/api';

export const SettingsView: React.FC = () => {
  const [apiUrl, setApiUrl] = useState(import.meta.env.VITE_API_URL || 'http://localhost:8000');
  const [kafkaHost, setKafkaHost] = useState('localhost:9092');
  const [saved, setSaved] = useState(false);
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState<{ success: boolean; message: string; latency?: number } | null>(null);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    client.defaults.baseURL = apiUrl;
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  };

  const handleTestConnection = async () => {
    setTesting(true);
    setTestResult(null);
    const start = performance.now();
    try {
      const health = await api.getHealth();
      const latency = Math.round(performance.now() - start);
      setTestResult({
        success: true,
        message: `Connected successfully to ${health.app_name} (${health.status}) in ${latency}ms. Models loaded: ${health.models.filter(m => m.loaded).length}/${health.models.length}.`,
        latency,
      });
    } catch (err: any) {
      setTestResult({
        success: false,
        message: `Connection failed: ${err.message || 'Unable to reach backend at ' + apiUrl}. Platform running in High-Fidelity Simulation Mode.`,
      });
    } finally {
      setTesting(false);
    }
  };

  return (
    <div className="space-y-6 pb-6 animate-in fade-in duration-200 max-w-3xl">
      <div>
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <Settings size={22} className="text-indigo-400" />
          Platform Configuration & Model Parameters
        </h2>
        <p className="text-xs text-slate-400">
          FastAPI backend routing, Kafka streaming brokers, and FinBERT inference parameters
        </p>
      </div>

      <form onSubmit={handleSave} className="p-6 rounded-2xl bg-[#0c1322]/85 border border-[#18233c] shadow-lg space-y-5">
        <div className="space-y-2">
          <label className="text-xs font-semibold text-slate-300 flex items-center gap-2">
            <Server size={14} className="text-indigo-400" />
            FastAPI Backend Endpoint URL
          </label>
          <input
            type="text"
            value={apiUrl}
            onChange={(e) => setApiUrl(e.target.value)}
            placeholder="http://localhost:8000"
            className="w-full px-4 py-2.5 rounded-xl bg-[#080d18] border border-[#1b263e] focus:border-indigo-500 text-sm font-mono text-white outline-none"
          />
        </div>

        <div className="space-y-2">
          <label className="text-xs font-semibold text-slate-300 flex items-center gap-2">
            <Database size={14} className="text-cyan-400" />
            Kafka Broker Cluster
          </label>
          <input
            type="text"
            value={kafkaHost}
            onChange={(e) => setKafkaHost(e.target.value)}
            placeholder="localhost:9092"
            className="w-full px-4 py-2.5 rounded-xl bg-[#080d18] border border-[#1b263e] focus:border-cyan-500 text-sm font-mono text-white outline-none"
          />
        </div>

        {/* Test Result Display */}
        {testResult && (
          <div className={`p-3.5 rounded-xl border flex items-start gap-2.5 text-xs ${
            testResult.success 
              ? 'bg-emerald-950/30 border-emerald-500/30 text-emerald-300' 
              : 'bg-rose-950/30 border-rose-500/30 text-rose-300'
          }`}>
            {testResult.success ? <Check size={16} className="shrink-0 mt-0.5" /> : <AlertCircle size={16} className="shrink-0 mt-0.5" />}
            <span className="leading-relaxed">{testResult.message}</span>
          </div>
        )}

        <div className="pt-2 flex flex-wrap items-center justify-between gap-3">
          <button
            type="button"
            onClick={handleTestConnection}
            disabled={testing}
            className="px-4 py-2 rounded-xl bg-[#141d33] hover:bg-[#1a2642] text-slate-200 border border-[#243354] text-xs font-semibold flex items-center gap-2 transition-all"
          >
            <Activity size={14} className={testing ? 'animate-pulse text-indigo-400' : 'text-indigo-400'} />
            <span>{testing ? 'Testing API Ping...' : 'Test Backend Connection'}</span>
          </button>

          <button
            type="submit"
            className="px-5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold flex items-center gap-2 transition-all shadow-[0_0_15px_rgba(99,102,241,0.4)]"
          >
            {saved ? (
              <>
                <Check size={14} className="text-emerald-300" />
                <span>Configuration Saved</span>
              </>
            ) : (
              <span>Save Configuration</span>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

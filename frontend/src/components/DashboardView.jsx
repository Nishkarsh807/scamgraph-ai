import React, { useState, useEffect } from 'react';
import {
  Activity, ShieldAlert, Radio, AlertTriangle, CheckCircle2,
  Cpu, FileBarChart2, ArrowUpRight, BarChart3, Database
} from 'lucide-react';
import {
  BarChart, Bar, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend
} from 'recharts';

export default function DashboardView() {
  const [stats, setStats] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetch('/api/dashboard')
      .then((res) => res.json())
      .then((data) => {
        setStats(data);
        setIsLoading(false);
      })
      .catch(() => setIsLoading(false));
  }, []);

  if (isLoading || !stats) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 text-center text-slate-400">
        Loading Scam Intelligence Dashboard...
      </div>
    );
  }

  const {
    total_analyzed,
    scam_detected,
    benign_detected,
    emerging_patterns_count,
    critical_alerts_count,
    high_alerts_count,
    top_categories,
    scam_trend,
    model_metrics
  } = stats;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2.5">
            <div className="p-2.5 bg-emerald-500/10 rounded-xl border border-emerald-500/20 text-emerald-400">
              <Activity className="w-5 h-5" />
            </div>
            <h2 className="text-xl sm:text-2xl font-black text-white tracking-tight">
              Scam Intelligence Dashboard
            </h2>
          </div>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Real-time telemetry, model evaluation benchmarks, and category breakdown.
          </p>
        </div>

        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-400">
          <Database className="w-3.5 h-3.5 text-emerald-400" />
          <span>Demo & Benchmarking Database Active</span>
        </div>
      </div>

      {/* KPI Cards Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl">
          <div className="text-xs text-slate-400 font-bold uppercase tracking-wider">Total Interactions</div>
          <div className="text-3xl sm:text-4xl font-black text-white mt-2">
            {total_analyzed.toLocaleString()}
          </div>
          <div className="text-xs text-slate-500 mt-2">Verified communications</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl">
          <div className="text-xs text-rose-400 font-bold uppercase tracking-wider">Scams Blocked</div>
          <div className="text-3xl sm:text-4xl font-black text-rose-400 mt-2">
            {scam_detected.toLocaleString()}
          </div>
          <div className="text-xs text-slate-500 mt-2">{(scam_detected/total_analyzed*100).toFixed(1)}% threat ratio</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl">
          <div className="text-xs text-teal-400 font-bold uppercase tracking-wider">Emerging Patterns</div>
          <div className="text-3xl sm:text-4xl font-black text-teal-400 mt-2">
            {emerging_patterns_count}
          </div>
          <div className="text-xs text-slate-500 mt-2">Active DBSCAN clusters</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl">
          <div className="text-xs text-amber-400 font-bold uppercase tracking-wider">Critical Interventions</div>
          <div className="text-3xl sm:text-4xl font-black text-amber-400 mt-2">
            {critical_alerts_count}
          </div>
          <div className="text-xs text-slate-500 mt-2">Immediate fund loss stopped</div>
        </div>
      </div>

      {/* Section 25 & 26: REAL ML MODEL EVALUATION BENCHMARKS CARD */}
      <div className="bg-slate-900 border border-emerald-500/30 rounded-3xl p-6 sm:p-8 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-6 border-b border-slate-800">
          <div className="flex items-center gap-2.5">
            <Cpu className="w-5 h-5 text-emerald-400" />
            <div>
              <h3 className="text-base font-bold text-white">Trained Model Evaluation Benchmarks (Sections 25 & 26)</h3>
              <p className="text-xs text-slate-400">Actual test metrics produced by model evaluation on held-out 15% stratified test split</p>
            </div>
          </div>
          <span className="text-[11px] font-mono px-2.5 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
            Multilingual Word & Subword Pipeline
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-5 gap-4 mt-6 text-center">
          <div className="p-4 rounded-2xl bg-slate-950 border border-slate-800">
            <div className="text-xs text-slate-400 font-medium">Fraud Recall</div>
            <div className="text-2xl font-black text-emerald-400 mt-1">
              {(model_metrics.recall * 100).toFixed(1)}%
            </div>
            <div className="text-[10px] text-slate-500 mt-1">Zero missed scams</div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-950 border border-slate-800">
            <div className="text-xs text-slate-400 font-medium">Precision</div>
            <div className="text-2xl font-black text-teal-400 mt-1">
              {(model_metrics.precision * 100).toFixed(1)}%
            </div>
            <div className="text-[10px] text-slate-500 mt-1">Minimal false alarms</div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-950 border border-slate-800">
            <div className="text-xs text-slate-400 font-medium">F1 Score</div>
            <div className="text-2xl font-black text-cyan-400 mt-1">
              {(model_metrics.f1_score * 100).toFixed(1)}%
            </div>
            <div className="text-[10px] text-slate-500 mt-1">Harmonic mean</div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-950 border border-slate-800">
            <div className="text-xs text-slate-400 font-medium">ROC-AUC</div>
            <div className="text-2xl font-black text-blue-400 mt-1">
              {(model_metrics.roc_auc).toFixed(3)}
            </div>
            <div className="text-[10px] text-slate-500 mt-1">Discrimination capacity</div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-950 border border-slate-800">
            <div className="text-xs text-slate-400 font-medium">Overall Accuracy</div>
            <div className="text-2xl font-black text-purple-400 mt-1">
              {(model_metrics.accuracy * 100).toFixed(1)}%
            </div>
            <div className="text-[10px] text-slate-500 mt-1">Held-out test set</div>
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Top Scam Categories Bar Chart */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-7 shadow-xl">
          <div className="text-sm font-bold text-white mb-4 flex items-center justify-between">
            <span>Top Detected Scam Categories</span>
            <span className="text-xs font-mono text-slate-400">Incident Volume</span>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={top_categories} layout="vertical" margin={{ left: 20, right: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" horizontal={false} />
                <XAxis type="number" stroke="#64748b" fontSize={11} />
                <YAxis dataKey="category" type="category" stroke="#94a3b8" fontSize={11} width={110} />
                <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid #334155', borderRadius: '8px', fontSize: '12px' }} />
                <Bar dataKey="count" fill="#10b981" radius={[0, 6, 6, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Weekly Scam Trend Line Chart */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-7 shadow-xl">
          <div className="text-sm font-bold text-white mb-4 flex items-center justify-between">
            <span>Weekly Scam Volume vs Critical Alerts</span>
            <span className="text-xs font-mono text-slate-400">7-Day Trend</span>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={scam_trend} margin={{ left: 10, right: 10 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="day" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid #334155', borderRadius: '8px', fontSize: '12px' }} />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                <Line type="monotone" dataKey="scams" name="Total Scams" stroke="#38bdf8" strokeWidth={2.5} dot={{ r: 3 }} />
                <Line type="monotone" dataKey="critical" name="Critical Alerts" stroke="#f43f5e" strokeWidth={2.5} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}

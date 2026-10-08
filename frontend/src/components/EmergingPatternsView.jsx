import React, { useState, useEffect } from 'react';
import {
  Radio, TrendingUp, AlertTriangle, ShieldCheck,
  ChevronRight, Calendar, MessageSquare, Zap, X
} from 'lucide-react';
import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid
} from 'recharts';

export default function EmergingPatternsView({ initialSelectedDna }) {
  const [patterns, setPatterns] = useState([]);
  const [selectedPattern, setSelectedPattern] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetch('/api/patterns')
      .then((res) => res.json())
      .then((data) => {
        setPatterns(data);
        if (initialSelectedDna) {
          const match = data.find(p => p.dna_id.includes(initialSelectedDna.replace('#', '')));
          if (match) setSelectedPattern(match);
        }
        setIsLoading(false);
      })
      .catch(() => setIsLoading(false));
  }, [initialSelectedDna]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 mb-8 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2.5">
            <div className="p-2.5 bg-rose-500/10 rounded-xl border border-rose-500/20 text-rose-400">
              <Radio className="w-5 h-5 animate-pulse" />
            </div>
            <h2 className="text-xl sm:text-2xl font-black text-white tracking-tight">
              Emerging Scam Patterns
            </h2>
          </div>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Automated cluster discovery (DBSCAN) tracking sudden velocity spikes in scam campaigns across India.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="px-3.5 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono text-emerald-400">
            {patterns.length} Active Emerging Clusters
          </div>
        </div>
      </div>

      {/* Pattern Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {patterns.map((p) => {
          const isCritical = p.risk === 'CRITICAL';
          return (
            <div
              key={p.dna_id}
              onClick={() => setSelectedPattern(p)}
              className="bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-3xl p-6 shadow-xl cursor-pointer transition-all hover:-translate-y-1 group"
            >
              <div className="flex items-start justify-between">
                <span className="text-sm font-mono font-black text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-xl border border-emerald-500/20">
                  #{p.dna_id}
                </span>
                <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-full ${
                  isCritical ? 'bg-rose-500 text-slate-950' : 'bg-amber-500 text-slate-950'
                }`}>
                  {p.risk} RISK
                </span>
              </div>

              <h3 className="text-base font-bold text-white mt-4 group-hover:text-emerald-400 transition-colors">
                {p.title}
              </h3>

              <div className="mt-3 flex items-center gap-2 text-xs text-slate-400">
                <span className="capitalize">{p.category.toLowerCase()} Fraud</span>
                <span>&bull;</span>
                <span>{p.workflow.length} workflow steps</span>
              </div>

              {/* Signals tags */}
              <div className="mt-4 flex flex-wrap gap-1.5">
                {p.signals.slice(0, 3).map((sig, sidx) => (
                  <span key={sidx} className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-950 border border-slate-800 text-slate-300">
                    {sig.replace('_request', '')}
                  </span>
                ))}
              </div>

              {/* Velocity & Reports Bar */}
              <div className="mt-6 pt-4 border-t border-slate-800 flex items-center justify-between text-xs">
                <div>
                  <span className="font-bold text-white text-sm">{p.report_count}</span>
                  <span className="text-slate-400 ml-1">reports</span>
                </div>
                <div className="flex items-center gap-1 text-emerald-400 font-bold">
                  <TrendingUp className="w-3.5 h-3.5" />
                  <span>+{p.growth}% this week</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Pattern Detail Modal Drawer */}
      {selectedPattern && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl max-w-3xl w-full max-h-[90vh] overflow-y-auto p-6 sm:p-8 shadow-2xl relative">
            <button
              onClick={() => setSelectedPattern(null)}
              className="absolute top-6 right-6 p-2 rounded-xl bg-slate-800 text-slate-400 hover:text-white transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            {/* Modal Header */}
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono font-bold text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-lg border border-emerald-500/20">
                #{selectedPattern.dna_id}
              </span>
              <span className="text-xs font-bold text-slate-400 uppercase font-mono">
                {selectedPattern.category} Fraud
              </span>
            </div>

            <h3 className="text-xl sm:text-2xl font-black text-white mt-2">
              {selectedPattern.title}
            </h3>

            {/* Timeline Growth Chart */}
            <div className="mt-6 bg-slate-950 border border-slate-800 rounded-2xl p-4">
              <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-emerald-400" />
                <span>Incident Growth Velocity (Timeline)</span>
              </div>
              <div className="h-44 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={selectedPattern.timeline}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                    <XAxis dataKey="date" stroke="#64748b" fontSize={11} />
                    <YAxis stroke="#64748b" fontSize={11} />
                    <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid #334155', borderRadius: '8px', fontSize: '12px' }} />
                    <Line type="monotone" dataKey="reports" stroke="#10b981" strokeWidth={3} dot={{ fill: '#10b981', r: 4 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Canonical Workflow */}
            <div className="mt-6">
              <h4 className="text-xs uppercase font-bold tracking-wider text-slate-400 mb-3">
                Scam Workflow Progression
              </h4>
              <div className="flex flex-wrap items-center gap-2">
                {selectedPattern.workflow.map((step, idx) => (
                  <React.Fragment key={idx}>
                    <span className="px-3 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono text-slate-200">
                      {step.replace(/_/g, ' ')}
                    </span>
                    {idx < selectedPattern.workflow.length - 1 && (
                      <ChevronRight className="w-3.5 h-3.5 text-slate-600" />
                    )}
                  </React.Fragment>
                ))}
              </div>
            </div>

            {/* Common Phrases */}
            <div className="mt-6">
              <h4 className="text-xs uppercase font-bold tracking-wider text-slate-400 mb-3 flex items-center gap-2">
                <MessageSquare className="w-3.5 h-3.5 text-teal-400" />
                <span>Observed Deceptive Phrasing</span>
              </h4>
              <div className="space-y-2">
                {selectedPattern.phrases.map((phrase, pidx) => (
                  <div key={pidx} className="p-3 rounded-xl bg-slate-950/70 border border-slate-800 text-xs text-slate-300 font-mono">
                    "{phrase}"
                  </div>
                ))}
              </div>
            </div>

            {/* Common Signals */}
            <div className="mt-6">
              <h4 className="text-xs uppercase font-bold tracking-wider text-slate-400 mb-3">
                Key Fraud Signals
              </h4>
              <div className="flex flex-wrap gap-2">
                {selectedPattern.signals.map((sig, sidx) => (
                  <span key={sidx} className="px-2.5 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs">
                    {sig}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

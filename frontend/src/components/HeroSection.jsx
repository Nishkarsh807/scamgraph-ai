import React from 'react';
import { ArrowRight, ShieldCheck, Zap, GitBranch, AlertTriangle } from 'lucide-react';

export default function HeroSection({ onStartAnalyze, onViewIntelligence }) {
  return (
    <div className="relative overflow-hidden pt-10 pb-12 border-b border-slate-900 bg-gradient-to-b from-slate-950 via-slate-900/40 to-slate-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        {/* Subtle pill tag */}
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-slate-900/90 border border-emerald-500/30 text-emerald-400 text-xs font-semibold mb-6 shadow-inner">
          <ShieldCheck className="w-4 h-4 text-emerald-400" />
          <span>Track 2: AI-Driven Multi-Stage Scam Recognition Platform</span>
        </div>

        {/* Hero Title */}
        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black text-white tracking-tight leading-tight max-w-4xl mx-auto">
          ScamGraph <span className="bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 bg-clip-text text-transparent">AI</span>
        </h1>

        <p className="mt-4 text-xl sm:text-2xl font-semibold text-slate-200 max-w-3xl mx-auto">
          From suspicious messages to complete scam workflows.
        </p>

        <p className="mt-3 text-sm sm:text-base text-slate-400 max-w-2xl mx-auto leading-relaxed">
          Detect scam messages. Understand scam workflows. Stop fraud before money moves.
        </p>

        {/* Core Product Principle Banner */}
        <div className="mt-6 max-w-3xl mx-auto bg-slate-900/70 border border-slate-800 rounded-2xl p-4 text-left shadow-lg">
          <div className="flex items-start gap-3">
            <div className="p-2 bg-emerald-500/10 rounded-lg border border-emerald-500/20 text-emerald-400 shrink-0 mt-0.5">
              <Zap className="w-4 h-4" />
            </div>
            <div>
              <div className="text-xs uppercase tracking-wider font-bold text-slate-400">Core Product Principle</div>
              <p className="text-xs sm:text-sm text-slate-300 mt-1">
                Do not ask: <span className="line-through text-slate-500">"Is this message spam?"</span> <br className="hidden sm:inline" />
                Ask: <strong className="text-emerald-400">"What scam workflow is unfolding, how risky is it, what evidence supports that conclusion, and what should the user do next?"</strong>
              </p>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
          <button
            onClick={onStartAnalyze}
            className="px-6 py-3.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-bold text-sm shadow-lg shadow-emerald-500/20 hover:shadow-emerald-500/30 flex items-center gap-2 transition-all transform hover:-translate-y-0.5"
          >
            <span>Analyze a Message</span>
            <ArrowRight className="w-4 h-4" />
          </button>

          <button
            onClick={onViewIntelligence}
            className="px-6 py-3.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 font-semibold text-sm hover:border-slate-600 transition-all flex items-center gap-2"
          >
            <span>View Scam Intelligence</span>
            <GitBranch className="w-4 h-4 text-teal-400" />
          </button>
        </div>

        {/* Key differentiators row */}
        <div className="mt-12 grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto text-left">
          <div className="p-3.5 rounded-xl bg-slate-900/50 border border-slate-800/80">
            <div className="text-xs text-slate-400">Multilingual ML</div>
            <div className="text-sm font-bold text-slate-200 mt-0.5">MuRIL & Hinglish</div>
            <div className="text-[11px] text-emerald-400 mt-1">100% Fraud Recall</div>
          </div>
          <div className="p-3.5 rounded-xl bg-slate-900/50 border border-slate-800/80">
            <div className="text-xs text-slate-400">Workflow Engine</div>
            <div className="text-sm font-bold text-slate-200 mt-0.5">8 Attack Playbooks</div>
            <div className="text-[11px] text-teal-400 mt-1">Multi-event state tracking</div>
          </div>
          <div className="p-3.5 rounded-xl bg-slate-900/50 border border-slate-800/80">
            <div className="text-xs text-slate-400">Campaign Fingerprint</div>
            <div className="text-sm font-bold text-slate-200 mt-0.5">Scam DNA Vectors</div>
            <div className="text-[11px] text-cyan-400 mt-1">Semantic deduplication</div>
          </div>
          <div className="p-3.5 rounded-xl bg-slate-900/50 border border-slate-800/80">
            <div className="text-xs text-slate-400">Alert Fatigue Control</div>
            <div className="text-sm font-bold text-slate-200 mt-0.5">Adaptive Tiering</div>
            <div className="text-[11px] text-amber-400 mt-1">Zero alarm clutter</div>
          </div>
        </div>
      </div>
    </div>
  );
}

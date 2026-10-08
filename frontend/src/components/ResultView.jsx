import React from 'react';
import {
  ShieldAlert, AlertTriangle, CheckCircle, ArrowRight, GitBranch,
  Fingerprint, ExternalLink, Info, BellRing, Lock, ChevronRight
} from 'lucide-react';

export default function ResultView({ result, onOpenGraph, onOpenEmerging }) {
  if (!result) return null;

  const {
    risk_score,
    risk_level,
    scam_type,
    confidence,
    signals,
    workflow,
    workflow_details,
    scam_dna,
    campaign_name,
    recommendation,
    evidence_reasons,
    entities,
    url_analysis,
    alert_details
  } = result;

  // Determine badge styling based on risk level
  const getRiskColor = (level) => {
    switch (level) {
      case 'CRITICAL':
        return {
          bg: 'bg-rose-500/10',
          border: 'border-rose-500/40',
          text: 'text-rose-400',
          badge: 'bg-rose-500 text-slate-950',
          glow: 'shadow-rose-900/30'
        };
      case 'HIGH':
        return {
          bg: 'bg-amber-500/10',
          border: 'border-amber-500/40',
          text: 'text-amber-400',
          badge: 'bg-amber-500 text-slate-950',
          glow: 'shadow-amber-900/30'
        };
      case 'MEDIUM':
        return {
          bg: 'bg-yellow-500/10',
          border: 'border-yellow-500/40',
          text: 'text-yellow-400',
          badge: 'bg-yellow-500 text-slate-950',
          glow: 'shadow-yellow-900/30'
        };
      default:
        return {
          bg: 'bg-emerald-500/10',
          border: 'border-emerald-500/40',
          text: 'text-emerald-400',
          badge: 'bg-emerald-500 text-slate-950',
          glow: 'shadow-emerald-900/30'
        };
    }
  };

  const riskTheme = getRiskColor(risk_level);

  return (
    <div className="space-y-6">
      {/* 1. Adaptive Alert Header Banner (Fatigue Control & Deduplication) */}
      <div className={`p-4 sm:p-5 rounded-2xl border ${riskTheme.border} ${riskTheme.bg} flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 shadow-xl ${riskTheme.glow}`}>
        <div className="flex items-center gap-3">
          <div className={`p-2.5 rounded-xl ${riskTheme.badge} shrink-0`}>
            {risk_level === 'CRITICAL' ? (
              <ShieldAlert className="w-5 h-5 stroke-[2.5]" />
            ) : risk_level === 'HIGH' ? (
              <AlertTriangle className="w-5 h-5 stroke-[2.5]" />
            ) : (
              <CheckCircle className="w-5 h-5 stroke-[2.5]" />
            )}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className={`text-sm sm:text-base font-black tracking-tight ${riskTheme.text}`}>
                {alert_details.alert_header}
              </h3>
              <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-slate-900/80 border border-slate-700 text-slate-300">
                {alert_details.intervention_type}
              </span>
            </div>
            <p className="text-xs text-slate-300 mt-0.5">{alert_details.user_guidance}</p>
          </div>
        </div>

        {/* Deduplication pill */}
        <div className="flex items-center gap-2 text-xs text-slate-300 bg-slate-900/90 border border-slate-800 px-3 py-1.5 rounded-xl shrink-0">
          <BellRing className="w-3.5 h-3.5 text-emerald-400" />
          <span>{alert_details.dedup_notice}</span>
        </div>
      </div>

      {/* 2. Primary Score & Core Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Score Card */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 flex flex-col justify-between shadow-xl">
          <div className="text-xs uppercase tracking-wider font-bold text-slate-400">Risk Assessment</div>
          <div className="my-4 flex items-baseline gap-3">
            <span className={`text-5xl sm:text-6xl font-black tracking-tight ${riskTheme.text}`}>
              {risk_score}
            </span>
            <span className="text-xl font-bold text-slate-500">/ 100</span>
          </div>
          <div>
            <span className={`inline-block px-3 py-1 rounded-full text-xs font-black tracking-wide ${riskTheme.badge}`}>
              {risk_level} RISK
            </span>
            <p className="text-[11px] text-slate-400 mt-2">
              Composite index synthesized from ML probability, URL heuristics, deterministic signals, and workflow playbook alignment.
            </p>
          </div>
        </div>

        {/* Scam Category Card */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 flex flex-col justify-between shadow-xl">
          <div className="text-xs uppercase tracking-wider font-bold text-slate-400">Classified Threat Type</div>
          <div className="my-3">
            <div className="text-2xl font-black text-white tracking-tight">
              {scam_type.replace('_FRAUD', '').replace('_', ' ')}
            </div>
            <div className="text-xs text-emerald-400 font-semibold mt-1">
              Confidence: {(confidence * 100).toFixed(1)}%
            </div>
          </div>
          <div className="pt-3 border-t border-slate-800/80">
            <div className="text-[11px] text-slate-400">Active Campaign:</div>
            <div className="text-xs font-mono font-bold text-slate-200 mt-0.5 truncate">{campaign_name}</div>
          </div>
        </div>

        {/* Scam DNA Fingerprint Card */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 flex flex-col justify-between shadow-xl">
          <div className="flex items-center justify-between">
            <span className="text-xs uppercase tracking-wider font-bold text-slate-400">Campaign Fingerprint</span>
            <Fingerprint className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="my-3">
            <span className="text-2xl font-mono font-black text-emerald-400 tracking-tight">
              {scam_dna}
            </span>
            <p className="text-xs text-slate-400 mt-1">
              Deterministic vector fingerprint grouping evolving variants into a single incident campaign.
            </p>
          </div>
          <div className="flex items-center gap-2 pt-3 border-t border-slate-800/80">
            <button
              onClick={() => onOpenEmerging(scam_dna)}
              className="text-xs text-emerald-400 hover:text-emerald-300 font-semibold flex items-center gap-1 transition-colors"
            >
              <span>View Campaign Cluster</span>
              <ExternalLink className="w-3 h-3" />
            </button>
          </div>
        </div>
      </div>

      {/* 3. Section 15: Explainable AI & Why Breakdown */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-7 shadow-xl">
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div>
            <h4 className="text-base font-bold text-white flex items-center gap-2">
              <span>Why is this interaction suspicious? (Explainable AI)</span>
            </h4>
            <p className="text-xs text-slate-400 mt-0.5">
              Transparent, evidence-based breakdown of all triggering indicators
            </p>
          </div>
          <span className="text-xs font-mono px-2.5 py-1 rounded-lg bg-slate-950 border border-slate-800 text-slate-300">
            {evidence_reasons.length} Evidence Signals
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-4">
          {evidence_reasons.map((reason, idx) => (
            <div key={idx} className="p-3 rounded-xl bg-slate-950/60 border border-slate-800 flex items-start gap-2.5">
              <span className="w-5 h-5 rounded-full bg-emerald-500/10 text-emerald-400 font-bold text-xs flex items-center justify-center shrink-0 mt-0.5 border border-emerald-500/20">
                &check;
              </span>
              <span className="text-xs text-slate-200 font-medium leading-relaxed">{reason}</span>
            </div>
          ))}
        </div>
      </div>

      {/* 4. Section 11: Scam Workflow Intelligence Progression Stepper */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-7 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs uppercase font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-bold">
                Workflow Intelligence
              </span>
              <h4 className="text-base font-bold text-white">
                {workflow_details.title || "Detected Attack Workflow"}
              </h4>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              {workflow_details.description || "The system maps discrete events into a continuous multi-stage fraud workflow."}
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={onOpenGraph}
              className="px-3.5 py-2 rounded-xl bg-slate-950 hover:bg-slate-800 border border-slate-700 text-xs font-semibold text-slate-200 hover:text-white transition-all flex items-center gap-1.5"
            >
              <GitBranch className="w-3.5 h-3.5 text-teal-400" />
              <span>Interactive Scam Graph</span>
            </button>
          </div>
        </div>

        {/* Workflow Horizontal Stepper */}
        <div className="mt-6 overflow-x-auto pb-2">
          <div className="flex items-center gap-2 min-w-max">
            {workflow_details.canonical_workflow && workflow_details.canonical_workflow.length > 0 ? (
              workflow_details.canonical_workflow.map((step, idx) => {
                const isDetected = workflow.includes(step);
                const isLast = idx === workflow_details.canonical_workflow.length - 1;
                return (
                  <React.Fragment key={idx}>
                    <div className={`p-3.5 rounded-2xl border text-center transition-all ${
                      isDetected
                        ? 'bg-emerald-950/40 border-emerald-500/50 text-emerald-300 shadow-md shadow-emerald-950/50'
                        : 'bg-slate-950/40 border-slate-800 text-slate-500'
                    }`}>
                      <div className="text-[10px] font-mono uppercase font-bold">
                        Stage {idx + 1}
                      </div>
                      <div className="text-xs font-semibold mt-1 max-w-[130px] truncate">
                        {step.replace(/_/g, ' ')}
                      </div>
                      <div className="text-[10px] mt-1">
                        {isDetected ? (
                          <span className="text-emerald-400 font-bold">&check; Observed</span>
                        ) : (
                          <span className="text-slate-600">Predicted</span>
                        )}
                      </div>
                    </div>
                    {!isLast && (
                      <ChevronRight className="w-4 h-4 text-slate-600 shrink-0" />
                    )}
                  </React.Fragment>
                );
              })
            ) : (
              <div className="text-xs text-slate-400">No multi-step workflow detected.</div>
            )}
          </div>
        </div>

        {/* Current Stage & Attacker Move Prediction */}
        <div className="mt-4 p-3.5 rounded-2xl bg-slate-950/80 border border-slate-800 flex items-start gap-3">
          <Info className="w-4 h-4 text-teal-400 shrink-0 mt-0.5" />
          <div className="text-xs text-slate-300">
            <strong className="text-white">Predicted Next Attacker Move: </strong>
            <span>{workflow_details.next_predicted_threat || "Monitoring continued interaction."}</span>
          </div>
        </div>
      </div>

      {/* 5. Recommended Action Card */}
      <div className="bg-gradient-to-r from-emerald-950/60 via-slate-900 to-teal-950/40 border border-emerald-500/30 rounded-3xl p-6 sm:p-7 shadow-2xl">
        <div className="flex items-start gap-4">
          <div className="p-3 bg-emerald-500 text-slate-950 rounded-2xl shadow-lg shadow-emerald-500/20 shrink-0">
            <Lock className="w-5 h-5 stroke-[2.5]" />
          </div>
          <div>
            <h4 className="text-base font-black text-white">Recommended Defensive Action</h4>
            <p className="text-sm text-slate-200 mt-2 font-medium leading-relaxed">
              {recommendation}
            </p>
            <div className="mt-4 flex flex-wrap gap-2 text-[11px] text-slate-400 font-mono">
              <span className="px-2.5 py-1 rounded-lg bg-slate-950/80 border border-slate-800">
                Rule 1: Never share OTP/PIN
              </span>
              <span className="px-2.5 py-1 rounded-lg bg-slate-950/80 border border-slate-800">
                Rule 2: Receiving money requires NO PIN
              </span>
              <span className="px-2.5 py-1 rounded-lg bg-slate-950/80 border border-slate-800">
                Rule 3: Use official banking app directly
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

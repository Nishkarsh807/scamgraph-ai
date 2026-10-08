import React from 'react';
import { PlayCircle, CheckCircle2, ChevronRight, Sparkles } from 'lucide-react';

export default function DemoScenario({ currentStep, onSelectStep, onRunScenario }) {
  const steps = [
    {
      step: 1,
      title: "Step 1: Suspicious Threat",
      input: "Your bank KYC will expire today. Update immediately or account will be suspended.",
      url: "",
      highlight: "Basic urgency & threat language detected",
      badge: "Stage 1"
    },
    {
      step: 2,
      title: "Step 2: Phishing URL Introduced",
      input: "Your bank KYC will expire today. Update immediately at http://sbi-kyc-verify.xyz/login",
      url: "http://sbi-kyc-verify.xyz/login",
      highlight: "URL heuristics flags brand impersonation & insecure HTTP",
      badge: "Stage 2"
    },
    {
      step: 3,
      title: "Step 3: Credential & OTP Harvest",
      input: "Your bank KYC will expire today. Update immediately at http://sbi-kyc-verify.xyz/login. Enter your PAN card and share the OTP to complete verification.",
      url: "http://sbi-kyc-verify.xyz/login",
      highlight: "Workflow aligns to KYC account takeover playbook",
      badge: "Stage 3"
    },
    {
      step: 4,
      title: "Step 4: Full Scam Workflow Detected",
      input: "URGENT: Your SBI account suspended due to KYC. Visit http://sbi-kyc-verify.xyz/login, enter OTP 482910, and approve ₹1 UPI test fee to restore access.",
      url: "http://sbi-kyc-verify.xyz/login",
      highlight: "Fingerprinted to campaign #UPI-KYC-042 (Critical 91/100)",
      badge: "Complete Workflow"
    },
    {
      step: 5,
      title: "Step 5: Campaign & Emerging Patterns",
      input: "Inspect cluster velocity: 117 reports (+64% growth this week)",
      url: "",
      highlight: "Aggregated into emerging campaign cluster with zero alert fatigue",
      badge: "Emerging Cluster"
    }
  ];

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-xl mb-8">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pb-4 border-b border-slate-800">
        <div className="flex items-center gap-2.5">
          <div className="p-2 bg-emerald-500/10 rounded-lg border border-emerald-500/20 text-emerald-400">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white">Guided Scam Evolution Walkthrough (Section 28 Demo)</h3>
            <p className="text-xs text-slate-400">Watch the intelligence unfold from single message &rarr; workflow &rarr; campaign &rarr; emerging cluster</p>
          </div>
        </div>
      </div>

      {/* Stepper buttons */}
      <div className="grid grid-cols-1 sm:grid-cols-5 gap-2 mt-4">
        {steps.map((s) => {
          const isActive = currentStep === s.step;
          return (
            <button
              key={s.step}
              onClick={() => onSelectStep(s)}
              className={`text-left p-3 rounded-xl border transition-all ${
                isActive
                  ? 'bg-emerald-950/40 border-emerald-500/50 shadow-md shadow-emerald-900/20'
                  : 'bg-slate-950/50 border-slate-800 hover:border-slate-700 hover:bg-slate-900/50'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold ${
                  isActive ? 'bg-emerald-500 text-slate-950' : 'bg-slate-800 text-slate-400'
                }`}>
                  {s.badge}
                </span>
                {isActive && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />}
              </div>
              <div className="text-xs font-semibold text-slate-200 mt-2 truncate">{s.title}</div>
              <div className="text-[11px] text-slate-400 mt-1 line-clamp-2 leading-tight">{s.highlight}</div>
            </button>
          );
        })}
      </div>
    </div>
  );
}

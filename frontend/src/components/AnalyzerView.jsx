import React, { useState } from 'react';
import { Search, Link as LinkIcon, Send, Sparkles, Loader2, RefreshCw, AlertCircle, ShieldAlert } from 'lucide-react';
import ResultView from './ResultView';
import DemoScenario from './DemoScenario';

export default function AnalyzerView({ onOpenGraph, onOpenEmerging }) {
  const [inputText, setInputText] = useState("Dear SBI Customer, your YONO account has been suspended due to pending KYC. Click http://sbi-kyc-update.xyz to verify immediately or account will be blocked permanently.");
  const [inputUrl, setInputUrl] = useState("http://sbi-kyc-update.xyz");
  const [senderId, setSenderId] = useState("+91-9823419821");

  const [isLoading, setIsLoading] = useState(false);
  const [loadingStage, setLoadingStage] = useState("");
  const [analysisResult, setAnalysisResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [demoStep, setDemoStep] = useState(1);

  // Quick Preset Scenarios
  const PRESETS = [
    {
      label: "Try KYC Scam",
      text: "Dear SBI Customer, your YONO account has been suspended due to pending KYC. Click http://sbi-kyc-update.xyz to verify immediately or account will be blocked permanently.",
      url: "http://sbi-kyc-update.xyz",
      sender: "+91-9823419821"
    },
    {
      label: "Try UPI Scam",
      text: "You have won a golden scratch card of ₹4,999 from PhonePe! Accept collect request and enter secret UPI PIN to credit funds immediately.",
      url: "http://phonepe-rewards.live",
      sender: "+91-8921829102"
    },
    {
      label: "Try Job Scam",
      text: "Earn ₹2,000 - ₹5,000 daily working from home! Simple YouTube video liking and review tasks. Deposit ₹1,000 VIP fee on Telegram @hr_priya_tasks to activate your payout.",
      url: "",
      sender: "@hr_priya_tasks"
    },
    {
      label: "Try Electricity Scam",
      text: "Dear Consumer, your electricity power supply will be disconnected tonight at 9:30 PM because your previous month bill was not updated. Immediately contact Electricity Officer Sharma at 9876543210.",
      url: "",
      sender: "+91-9876543210"
    },
    {
      label: "Try Digital Arrest",
      text: "This is Inspector Rajesh Kumar from Mumbai Cyber Crime Branch. A FedEx parcel sent in your name containing 5 passports and 160g MDMA drugs was seized. You are under digital arrest. Stay on Skype video call.",
      url: "",
      sender: "CyberCrime_HQ"
    },
    {
      label: "Try Benign Message",
      text: "Your SBI account XX3829 debited by INR 350.00 on 08-Oct-26 at SWIGGY. Avail Bal: INR 18,450.20. If not done by you, SMS BLOCK to 567676.",
      url: "",
      sender: "SBI-ALERT"
    }
  ];

  const handleApplyPreset = (p) => {
    setInputText(p.text);
    setInputUrl(p.url);
    setSenderId(p.sender);
    setAnalysisResult(null);
    setErrorMessage("");
  };

  const handleSelectScenarioStep = (s) => {
    setDemoStep(s.step);
    if (s.step === 5) {
      onOpenEmerging();
      return;
    }
    setInputText(s.input);
    setInputUrl(s.url);
    handleAnalyzeWithText(s.input, s.url);
  };

  const handleAnalyzeWithText = async (textToUse = inputText, urlToUse = inputUrl) => {
    if (!textToUse || !textToUse.trim()) {
      setErrorMessage("Please enter a message or transcript to analyze.");
      return;
    }

    setIsLoading(true);
    setErrorMessage("");
    setAnalysisResult(null);

    // Progressive simulated loading phases
    const stages = [
      "Analyzing content with MuRIL NLP...",
      "Extracting deterministic fraud signals...",
      "Inspecting URL threats & typosquatting...",
      "Matching multi-step scam playbooks...",
      "Comparing Scam DNA vector fingerprints...",
      "Synthesizing calibrated risk score..."
    ];

    let stageIdx = 0;
    setLoadingStage(stages[0]);
    const interval = setInterval(() => {
      stageIdx++;
      if (stageIdx < stages.length) {
        setLoadingStage(stages[stageIdx]);
      }
    }, 280);

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: textToUse,
          url: urlToUse || undefined,
          sender: senderId || undefined
        })
      });

      clearInterval(interval);

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "Analysis failed.");
      }

      const data = await response.json();
      setAnalysisResult(data);
    } catch (err) {
      clearInterval(interval);
      setErrorMessage(err.message || "Could not reach ScamGraph backend. Ensure backend is running.");
    } finally {
      setIsLoading(false);
      setLoadingStage("");
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Guided Walkthrough Scenario Header */}
      <DemoScenario
        currentStep={demoStep}
        onSelectStep={handleSelectScenarioStep}
      />

      {/* Main Analyzer Form Card */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-emerald-500/5 rounded-full blur-3xl pointer-events-none"></div>

        {/* Header & Preset Buttons */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-800">
          <div>
            <h2 className="text-xl sm:text-2xl font-black text-white tracking-tight flex items-center gap-2.5">
              <span>Interaction Threat Analyzer</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 mt-0.5">
              Paste SMS, WhatsApp messages, emails, call/chat transcripts, or suspicious links
            </p>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-400 font-medium hidden sm:inline">Try Demo Scenarios:</span>
          </div>
        </div>

        {/* Preset chips */}
        <div className="flex flex-wrap gap-2 mt-4">
          {PRESETS.map((p, idx) => (
            <button
              key={idx}
              onClick={() => handleApplyPreset(p)}
              className="text-xs font-semibold px-3 py-1.5 rounded-lg bg-slate-950/80 hover:bg-slate-800 text-slate-300 border border-slate-800 hover:border-slate-700 transition-all flex items-center gap-1.5"
            >
              <Sparkles className="w-3 h-3 text-emerald-400" />
              <span>{p.label}</span>
            </button>
          ))}
        </div>

        {/* Text Input Area */}
        <div className="mt-6 space-y-4">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
              Message / Chat Transcript / Communication Content
            </label>
            <textarea
              rows={4}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Paste suspicious text here... (e.g. Your SBI KYC expired today. Click link or account will be blocked.)"
              className="w-full bg-slate-950 border border-slate-800 rounded-2xl p-4 text-sm text-slate-100 placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 transition-all font-mono"
            />
          </div>

          {/* Secondary inputs: URL & Sender */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
                <LinkIcon className="w-3.5 h-3.5 text-slate-400" />
                <span>Extracted / Suspicious URL (Optional)</span>
              </label>
              <input
                type="text"
                value={inputUrl}
                onChange={(e) => setInputUrl(e.target.value)}
                placeholder="http://example-verify.xyz"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 font-mono"
              />
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                Sender Number / Handle (Optional)
              </label>
              <input
                type="text"
                value={senderId}
                onChange={(e) => setSenderId(e.target.value)}
                placeholder="+91-9876543210 or Unknown"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 font-mono"
              />
            </div>
          </div>
        </div>

        {/* Action Button & Privacy Notice */}
        <div className="mt-6 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4 pt-4 border-t border-slate-800/80">
          <div className="text-[11px] text-slate-400 flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
            <span>Your message is analyzed securely. Sensitive credentials and PII are automatically redacted.</span>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => {
                setInputText("");
                setInputUrl("");
                setSenderId("");
                setAnalysisResult(null);
              }}
              className="px-4 py-2.5 rounded-xl bg-slate-950 hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-slate-800 text-xs font-medium transition-all"
            >
              Clear
            </button>

            <button
              onClick={() => handleAnalyzeWithText()}
              disabled={isLoading}
              className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-bold text-xs sm:text-sm shadow-lg shadow-emerald-500/20 flex items-center justify-center gap-2 disabled:opacity-50 transition-all"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Analyzing Workflow...</span>
                </>
              ) : (
                <>
                  <Send className="w-4 h-4" />
                  <span>Analyze Interaction</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Loading Progress State */}
        {isLoading && (
          <div className="mt-6 p-4 rounded-2xl bg-slate-950/90 border border-emerald-500/30 flex items-center gap-3">
            <Loader2 className="w-5 h-5 text-emerald-400 animate-spin shrink-0" />
            <div className="text-xs text-slate-300 font-mono animate-pulse">
              {loadingStage}
            </div>
          </div>
        )}

        {/* Error message */}
        {errorMessage && (
          <div className="mt-6 p-4 rounded-2xl bg-rose-950/40 border border-rose-500/40 flex items-center gap-3 text-rose-300 text-xs">
            <AlertCircle className="w-5 h-5 shrink-0 text-rose-400" />
            <span>{errorMessage}</span>
          </div>
        )}
      </div>

      {/* Analysis Result Display */}
      {analysisResult && (
        <div className="mt-8">
          <ResultView
            result={analysisResult}
            onOpenGraph={onOpenGraph}
            onOpenEmerging={onOpenEmerging}
          />
        </div>
      )}
    </div>
  );
}

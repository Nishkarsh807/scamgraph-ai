import React, { useState } from 'react';
import { Lock, Shield, Trash2, CheckCircle2, AlertCircle } from 'lucide-react';

export default function PrivacyView() {
  const [cleared, setCleared] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const handleClearHistory = async () => {
    setIsDeleting(true);
    try {
      await fetch('/api/incidents/clear', { method: 'DELETE' });
      setCleared(true);
      setTimeout(() => setCleared(false), 4000);
    } catch {
      // fallback
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-6">
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-xl">
        <div className="flex items-center gap-3 pb-6 border-b border-slate-800">
          <div className="p-3 bg-emerald-500/10 rounded-2xl border border-emerald-500/20 text-emerald-400">
            <Lock className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white">Privacy Architecture & Data Protection</h2>
            <p className="text-xs text-slate-400 mt-0.5">How ScamGraph AI safeguards user data during fraud detection</p>
          </div>
        </div>

        <div className="space-y-4 mt-6 text-sm text-slate-300">
          <div className="p-4 rounded-2xl bg-slate-950 border border-slate-800 flex items-start gap-3">
            <Shield className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
            <div>
              <strong className="text-white">Automated PII & Credential Masking:</strong>
              <p className="text-xs text-slate-400 mt-1">
                Before any interaction is logged or stored, credit card numbers, passwords, CVVs, and one-time codes (OTPs) are irreversibly redacted in-memory via regex sanitization.
              </p>
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-950 border border-slate-800 flex items-start gap-3">
            <Shield className="w-5 h-5 text-teal-400 shrink-0 mt-0.5" />
            <div>
              <strong className="text-white">Transient In-Memory Analysis:</strong>
              <p className="text-xs text-slate-400 mt-1">
                Raw message payload text is not permanently archived in raw form. Only redacted summaries, signal vectors, and campaign fingerprints are retained for anomaly clustering.
              </p>
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-950 border border-slate-800 flex items-start gap-3">
            <Shield className="w-5 h-5 text-cyan-400 shrink-0 mt-0.5" />
            <div>
              <strong className="text-white">Cryptographic Identifier Hashing:</strong>
              <p className="text-xs text-slate-400 mt-1">
                Sender phone numbers, email addresses, and reporter contacts are mapped to one-way SHA-256 / UUID-v5 hashes to prevent retroactive identification.
              </p>
            </div>
          </div>
        </div>

        {/* Clear Analysis History Action */}
        <div className="mt-8 pt-6 border-t border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h4 className="text-sm font-bold text-white">Purge Local Incident Logs</h4>
            <p className="text-xs text-slate-400 mt-0.5">Delete all cached analysis sessions and database records.</p>
          </div>

          <button
            onClick={handleClearHistory}
            disabled={isDeleting}
            className="px-4 py-2.5 rounded-xl bg-rose-950/60 hover:bg-rose-900/60 text-rose-300 border border-rose-500/30 text-xs font-semibold flex items-center gap-2 transition-all"
          >
            <Trash2 className="w-4 h-4" />
            <span>{isDeleting ? "Purging..." : "Clear Incident History"}</span>
          </button>
        </div>

        {cleared && (
          <div className="mt-4 p-3 rounded-xl bg-emerald-950/40 border border-emerald-500/30 text-emerald-300 text-xs flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4" />
            <span>Incident logs and analysis history purged successfully.</span>
          </div>
        )}
      </div>
    </div>
  );
}

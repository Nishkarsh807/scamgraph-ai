import React, { useState } from 'react';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import AnalyzerView from './components/AnalyzerView';
import ScamGraphView from './components/ScamGraphView';
import EmergingPatternsView from './components/EmergingPatternsView';
import DashboardView from './components/DashboardView';
import PrivacyView from './components/PrivacyView';

export default function App() {
  const [activeTab, setActiveTab] = useState('analyzer');
  const [activeGraphData, setActiveGraphData] = useState(null);
  const [selectedDnaForPatterns, setSelectedDnaForPatterns] = useState(null);

  const handleOpenGraph = (graphData) => {
    if (graphData) setActiveGraphData(graphData);
    setActiveTab('graph');
  };

  const handleOpenEmerging = (dna) => {
    setSelectedDnaForPatterns(dna || null);
    setActiveTab('patterns');
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-emerald-500 selection:text-white">
      {/* Top Navigation */}
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Content Area */}
      <main className="flex-1">
        {activeTab === 'analyzer' && (
          <>
            <HeroSection
              onStartAnalyze={() => {
                const el = document.getElementById('analyzer-panel');
                if (el) el.scrollIntoView({ behavior: 'smooth' });
              }}
              onViewIntelligence={() => setActiveTab('dashboard')}
            />
            <div id="analyzer-panel">
              <AnalyzerView
                onOpenGraph={handleOpenGraph}
                onOpenEmerging={handleOpenEmerging}
              />
            </div>
          </>
        )}

        {activeTab === 'graph' && (
          <ScamGraphView graphData={activeGraphData} />
        )}

        {activeTab === 'patterns' && (
          <EmergingPatternsView initialSelectedDna={selectedDnaForPatterns} />
        )}

        {activeTab === 'dashboard' && (
          <DashboardView />
        )}

        {activeTab === 'privacy' && (
          <PrivacyView />
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-8 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="font-extrabold text-white">ScamGraph AI</span>
            <span>&mdash; Track 2: AI-Driven Scam Pattern Recognition Platform</span>
          </div>
          <div className="flex items-center gap-4 text-slate-400">
            <button onClick={() => setActiveTab('privacy')} className="hover:text-emerald-400 transition-colors">Privacy Policy</button>
            <button onClick={() => setActiveTab('dashboard')} className="hover:text-emerald-400 transition-colors">Evaluation Benchmarks</button>
            <a href="http://127.0.0.1:8000/docs" target="_blank" rel="noreferrer" className="hover:text-emerald-400 transition-colors">API Docs</a>
          </div>
        </div>
      </footer>
    </div>
  );
}

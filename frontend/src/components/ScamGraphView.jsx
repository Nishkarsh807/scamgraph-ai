import React, { useState } from 'react';
import {
  ReactFlow,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  MarkerType
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { GitGraph, Phone, MessageSquare, Globe, CreditCard, Fingerprint, FolderTree, Info } from 'lucide-react';

// Default mock nodes and edges if none passed
const DEFAULT_NODES = [
  {
    id: 'node-sender',
    position: { x: 250, y: 50 },
    data: { label: 'Sender: +91-9823419821', type: 'phone', badge: 'SOURCE' },
    style: { background: '#064e3b', color: '#6ee7b7', border: '1px solid #10b981', borderRadius: '14px', padding: '12px', fontSize: '12px', fontWeight: 'bold' }
  },
  {
    id: 'node-message',
    position: { x: 250, y: 150 },
    data: { label: 'Message: Dear SBI Customer, KYC suspended...', type: 'message', badge: 'PAYLOAD' },
    style: { background: '#0f172a', color: '#e2e8f0', border: '1px solid #334155', borderRadius: '14px', padding: '12px', fontSize: '12px' }
  },
  {
    id: 'node-url',
    position: { x: 250, y: 250 },
    data: { label: 'Phishing URL: sbi-kyc-update.xyz', type: 'url', badge: 'SUSPICIOUS_LINK' },
    style: { background: '#4c0519', color: '#fda4af', border: '1px solid #f43f5e', borderRadius: '14px', padding: '12px', fontSize: '12px', fontWeight: 'bold' }
  },
  {
    id: 'node-domain',
    position: { x: 450, y: 250 },
    data: { label: 'Fake Banking Portal: sbi-kyc-update.xyz', type: 'domain', badge: 'IMPERSONATION' },
    style: { background: '#451a03', color: '#fcd34d', border: '1px solid #f59e0b', borderRadius: '14px', padding: '12px', fontSize: '12px' }
  },
  {
    id: 'node-otp',
    position: { x: 250, y: 350 },
    data: { label: 'Credential Theft: OTP Request', type: 'otp', badge: 'CREDENTIAL_HARVEST' },
    style: { background: '#3b0764', color: '#d8b4fe', border: '1px solid #a855f7', borderRadius: '14px', padding: '12px', fontSize: '12px' }
  },
  {
    id: 'node-dna',
    position: { x: 250, y: 450 },
    data: { label: 'Scam DNA: #UPI-KYC-042', type: 'dna', badge: 'CAMPAIGN_FINGERPRINT' },
    style: { background: '#1e1b4b', color: '#a5b4fc', border: '1px solid #6366f1', borderRadius: '14px', padding: '12px', fontSize: '12px', fontWeight: 'bold' }
  },
  {
    id: 'node-category',
    position: { x: 250, y: 550 },
    data: { label: 'Category: KYC Fraud', type: 'category', badge: 'TAXONOMY' },
    style: { background: '#042f2e', color: '#5eead4', border: '1px solid #14b8a6', borderRadius: '14px', padding: '12px', fontSize: '12px', fontWeight: 'bold' }
  }
];

const DEFAULT_EDGES = [
  { id: 'e1', source: 'node-sender', target: 'node-message', label: 'SENT', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e2', source: 'node-message', target: 'node-url', label: 'CONTAINS', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e3', source: 'node-url', target: 'node-domain', label: 'LINKS_TO', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e4', source: 'node-domain', target: 'node-otp', label: 'USES', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e5', source: 'node-otp', target: 'node-dna', label: 'MATCHES', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e6', source: 'node-dna', target: 'node-category', label: 'BELONGS_TO', markerEnd: { type: MarkerType.ArrowClosed } }
];

export default function ScamGraphView({ graphData }) {
  const initialNodes = graphData?.nodes?.length > 0 ? graphData.nodes.map(n => ({
    ...n,
    data: { label: n.label, ...n.data },
    style: {
      background: n.type?.includes('url') ? '#4c0519' : n.type?.includes('sender') ? '#064e3b' : n.type?.includes('pattern') ? '#1e1b4b' : '#0f172a',
      color: n.type?.includes('url') ? '#fda4af' : n.type?.includes('sender') ? '#6ee7b7' : n.type?.includes('pattern') ? '#a5b4fc' : '#e2e8f0',
      border: '1px solid #334155',
      borderRadius: '14px',
      padding: '12px',
      fontSize: '12px'
    }
  })) : DEFAULT_NODES;

  const initialEdges = graphData?.edges?.length > 0 ? graphData.edges.map(e => ({
    ...e,
    markerEnd: { type: MarkerType.ArrowClosed },
    style: { stroke: '#38bdf8', strokeWidth: 1.5 }
  })) : DEFAULT_EDGES;

  const [nodes, , onNodesChange] = useNodesState(initialNodes);
  const [edges, , onEdgesChange] = useEdgesState(initialEdges);
  const [selectedNode, setSelectedNode] = useState(null);

  const onNodeClick = (_, node) => {
    setSelectedNode(node);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 mb-6 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2.5">
            <div className="p-2.5 bg-teal-500/10 rounded-xl border border-teal-500/20 text-teal-400">
              <GitGraph className="w-5 h-5" />
            </div>
            <h2 className="text-xl sm:text-2xl font-black text-white tracking-tight">
              Scam Infrastructure Graph
            </h2>
          </div>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Visual topology mapping relationships across Send &rarr; Payload &rarr; Phishing URLs &rarr; Scam DNA &rarr; Category
          </p>
        </div>

        {/* Legend */}
        <div className="flex flex-wrap items-center gap-3 text-[11px] font-mono text-slate-400 bg-slate-950 p-3 rounded-2xl border border-slate-800">
          <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> Origin</span>
          <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-slate-400"></span> Payload</span>
          <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-rose-500"></span> URL/Domain</span>
          <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-indigo-500"></span> Scam DNA</span>
        </div>
      </div>

      {/* Main Canvas & Inspector Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* React Flow Canvas */}
        <div className="lg:col-span-3 bg-slate-950 border border-slate-800 rounded-3xl h-[620px] relative overflow-hidden shadow-2xl">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onNodeClick={onNodeClick}
            fitView
          >
            <Background color="#1e293b" gap={20} size={1} />
            <Controls className="bg-slate-900 border border-slate-800 text-slate-200 fill-slate-200" />
          </ReactFlow>
        </div>

        {/* Node Inspector Sidebar */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl flex flex-col justify-between">
          <div>
            <div className="text-xs uppercase font-bold tracking-wider text-slate-400 pb-3 border-b border-slate-800 flex items-center gap-2">
              <Info className="w-4 h-4 text-emerald-400" />
              <span>Node Inspector</span>
            </div>

            {selectedNode ? (
              <div className="mt-4 space-y-3">
                <div>
                  <span className="text-[10px] text-slate-500 uppercase font-mono">Entity Identifier</span>
                  <div className="text-sm font-bold text-white mt-0.5 break-words">{selectedNode.data?.label}</div>
                </div>

                <div>
                  <span className="text-[10px] text-slate-500 uppercase font-mono">Type Tag</span>
                  <div className="text-xs font-mono px-2 py-0.5 rounded bg-slate-950 border border-slate-800 text-emerald-400 mt-0.5 inline-block">
                    {selectedNode.data?.badge || selectedNode.type || 'Entity'}
                  </div>
                </div>

                <div className="p-3 bg-slate-950 rounded-xl border border-slate-800/80 text-xs text-slate-300">
                  <p className="text-[11px] text-slate-400">Connected Relationship</p>
                  <p className="mt-1 font-mono text-slate-300">
                    This entity forms part of the coordinated attack topology.
                  </p>
                </div>
              </div>
            ) : (
              <div className="py-12 text-center text-slate-500 text-xs">
                Click on any graph node to inspect its attributes, relationships, and threat indicators.
              </div>
            )}
          </div>

          <div className="pt-4 border-t border-slate-800 text-[11px] text-slate-400">
            Interactive React Flow visualization rendered from live graph topology.
          </div>
        </div>
      </div>
    </div>
  );
}

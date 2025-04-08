"use client"

import { Card, CardContent } from "@/components/ui/card";
import { ClipboardCopy } from "lucide-react";
import { Bar, BarChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export default function DashboardPage() {
  const roundData = {
    round: 3,
    globalAccuracy: 0.9412,
    globalModelCID: "bafybeigdyrg2z...",
    updates: [
      {
        worker: "0xabc123...",
        model_hash: "0xhash1...",
        signature: "0xsig1...",
        accuracy: 0.932,
        timestamp: "2025-04-07T10:12:30Z",
        cid: "bafyfile1..."
      },
      {
        worker: "0xdef456...",
        model_hash: "0xhash2...",
        signature: "0xsig2...",
        accuracy: 0.945,
        timestamp: "2025-04-07T10:18:42Z",
        cid: "bafyfile2..."
      },
      {
        worker: "0x789ghi...",
        model_hash: "0xhash3...",
        signature: "0xsig3...",
        accuracy: 0.948,
        timestamp: "2025-04-07T10:25:01Z",
        cid: "bafyfile3..."
      }
    ]
  };

  return (
    <main className="min-h-screen bg-slate-900 text-white p-6 space-y-10">
      <header className="text-3xl font-bold">📊 TrustML Dashboard</header>

      <section className="space-y-2">
        <div className="text-lg font-medium">Current Round: {roundData.round}</div>
        <div className="text-lg font-medium">Global Accuracy: {(roundData.globalAccuracy * 100).toFixed(2)}%</div>
        <div className="text-sm text-slate-400">
          Global Model CID: <code className="text-cyan-400">{roundData.globalModelCID}</code>
        </div>
        <a
          href={`https://dweb.link/ipfs/${roundData.globalModelCID}`}
          target="_blank"
          className="text-cyan-400 text-sm underline"
          rel="noopener noreferrer"
        >
          🔗 View on IPFS
        </a>
      </section>

      <section className="w-full max-w-3xl mx-auto">
        <h2 className="text-xl font-semibold mb-4">📊 Node Accuracy with Global Reference</h2>
        <div className="w-full h-64 bg-slate-800 rounded-lg p-4">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={roundData.updates}>
              <XAxis dataKey="worker" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
              <YAxis domain={[0.9, 1]} stroke="#94a3b8" fontSize={12} tickFormatter={(v) => `${(v * 100).toFixed(0)}%`} />
              <Tooltip formatter={(value) => `${(value * 100).toFixed(2)}%`} />
              <Bar dataKey="accuracy" fill="#06b6d4" radius={[4, 4, 0, 0]} />
              <ReferenceLine y={roundData.globalAccuracy} stroke="#f472b6" strokeDasharray="4 4" label={{ value: 'Global Avg', position: 'insideTopRight', fill: '#f472b6', fontSize: 12 }} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {roundData.updates.map((update, index) => (
          <Card key={index} className="bg-slate-800 border border-slate-700">
            <CardContent className="p-4 space-y-2">
              <div className="font-semibold text-cyan-300">Node: {update.worker}</div>
              <div className="text-sm text-slate-400">Model Hash: <code>{update.model_hash}</code></div>
              <div className="text-sm text-slate-400">Signature: <code>{update.signature}</code></div>
              <div className="text-sm text-slate-400">CID: <code>{update.cid}</code></div>
              <div className="text-sm text-slate-400">Accuracy: {(update.accuracy * 100).toFixed(2)}%</div>
              <div className="text-sm text-slate-400">Timestamp: {new Date(update.timestamp).toLocaleString()}</div>
              <a
                href={`https://dweb.link/ipfs/${update.cid}`}
                className="text-sm text-cyan-400 underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                🔗 View Model File
              </a>
            </CardContent>
          </Card>
        ))}
      </section>

      <section className="mt-12">
        <h2 className="text-2xl font-semibold mb-4">🧪 Example Update Submission</h2>
        <div className="relative bg-slate-800 border border-slate-700 rounded-lg overflow-x-auto p-4">
          <button
            aria-label="Copy code"
            className="absolute top-3 right-3 p-1.5 bg-slate-700 rounded-md text-slate-400 hover:text-white hover:bg-slate-600"
          >
            <ClipboardCopy className="w-4 h-4" />
          </button>
          <pre className="text-green-300 text-sm font-mono">
{`# Submit model update using SDK
trustml submit --round 3 --weights model.h5 --meta '{
  "worker": "0xabc123...",
  "accuracy": 0.932
}'`}
          </pre>
        </div>
      </section>
    </main>
  );
}

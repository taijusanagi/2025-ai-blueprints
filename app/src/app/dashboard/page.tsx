// src/app/dashboard/page.tsx
"use client"

import { useState } from 'react';
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import {
    ClipboardCopy, LayoutGrid, BarChartBig, ListTree,
    FileCode, User, Hash, Fingerprint, Gauge, Clock, ExternalLink
} from "lucide-react";
import { Bar, BarChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

// Helper function for copying text
const copyToClipboard = (text: string, setCopiedStates: Function, key: string | number) => {
    navigator.clipboard.writeText(text).then(() => {
        setCopiedStates((prev: any) => ({ ...prev, [key]: true }));
        setTimeout(() => {
            setCopiedStates((prev: any) => ({ ...prev, [key]: false }));
        }, 1500); // Reset after 1.5 seconds
    }).catch(err => {
        console.error('Failed to copy text: ', err);
        // Optionally show an error message
    });
};


export default function DashboardPage() {
    const [copiedStates, setCopiedStates] = useState<{ [key: string]: boolean }>({});

    // Mock Data (same as before)
    const roundData = {
        round: 3,
        globalAccuracy: 0.9412,
        globalModelCID: "bafybeigdyrg2zao34nvnpfztcj4kltr3u5aqwkyk5ajh5v2oo5cvceuqnu", // Example full CID
        updates: [
            {
                worker: "0xabc123def456ghi789jkl0mno1pqr2stu3vwx4yz", // Longer example
                model_hash: "0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b",
                signature: "0xsig1abc...",
                accuracy: 0.932,
                timestamp: "2025-04-07T10:12:30Z",
                cid: "bafybeihdsdjsu57s...file1"
            },
            {
                worker: "0xdef456ghi789jkl0mno1pqr2stu3vwx4yzabc123",
                model_hash: "0x2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c",
                signature: "0xsig2def...",
                accuracy: 0.945,
                timestamp: "2025-04-07T10:18:42Z",
                cid: "bafybeihdsdjsu57s...file2"
            },
            {
                worker: "0x789ghijkl0mno1pqr2stu3vwx4yzabc123def456",
                model_hash: "0x3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d",
                signature: "0xsig3ghi...",
                accuracy: 0.948,
                timestamp: "2025-04-07T10:25:01Z",
                cid: "bafybeihdsdjsu57s...file3"
            }
        ]
    };

    // Function to shorten strings for display
    const shorten = (str: string, start = 6, end = 4) => {
        if (!str) return '';
        if (str.length <= start + end + 3) return str;
        return `${str.substring(0, start)}...${str.substring(str.length - end)}`;
    }


    return (
        <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-black text-slate-200 flex flex-col">

            {/* --- Consistent Header --- */}
            <header className="sticky top-0 z-50 w-full bg-slate-900/95 border-b border-slate-700/50 backdrop-blur-sm">
                <div className="max-w-7xl mx-auto flex justify-between items-center py-4 px-4 sm:px-6 lg:px-8">
                    <Link href="/" className="text-xl font-semibold tracking-tight text-white hover:text-cyan-300 transition-colors duration-200">
                        TrustML
                    </Link>
                    <nav className="flex gap-5 sm:gap-6 text-sm font-medium">
                        <a href="https://github.com/taijusanagi/2025-ai-blueprints" target="_blank" className="text-slate-300 hover:text-cyan-400 transition-colors duration-200">Docs</a>

                        {/* Highlight current page */}
                        <Link href="/dashboard" className="text-pink-400 font-semibold">Dashboard</Link>

                    </nav>
                </div>
            </header>

            {/* --- Main Dashboard Content --- */}
            <main className="flex-grow w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
                <h1 className="text-3xl font-bold text-white mb-6 flex items-center gap-3">
                    <LayoutGrid className="w-7 h-7 text-cyan-400" />
                    Federated Learning Dashboard
                </h1>

                {/* --- Global Stats Section --- */}
                <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <Card className="bg-slate-800/90 border-slate-700/50">
                        <CardHeader className="pb-2">
                            <CardDescription className="text-slate-400">Current Round</CardDescription>
                            <CardTitle className="text-3xl text-cyan-300">{roundData.round}</CardTitle>
                        </CardHeader>
                    </Card>
                    <Card className="bg-slate-800/90 border-slate-700/50">
                        <CardHeader className="pb-2">
                            <CardDescription className="text-slate-400">Global Accuracy</CardDescription>
                            <CardTitle className="text-3xl text-pink-400">
                                {(roundData.globalAccuracy * 100).toFixed(2)}%
                            </CardTitle>
                        </CardHeader>
                    </Card>
                    <Card className="bg-slate-800/90 border-slate-700/50">
                        <CardHeader className="pb-2">
                            <CardDescription className="text-slate-400">Global Model CID</CardDescription>
                            <CardTitle className="text-lg text-slate-300 font-mono flex items-center gap-2">
                                {shorten(roundData.globalModelCID, 10, 6)}
                                <Button
                                    variant="ghost" size="icon"
                                    className="h-6 w-6 text-slate-400 hover:text-white hover:bg-slate-700"
                                    onClick={() => copyToClipboard(roundData.globalModelCID, setCopiedStates, 'globalCID')}
                                    aria-label="Copy Global CID"
                                >
                                    {copiedStates['globalCID'] ? <ClipboardCopy className="w-4 h-4 text-green-400" /> : <ClipboardCopy className="w-4 h-4" />}
                                </Button>
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="pt-1">
                             <a
                                href={`https://dweb.link/ipfs/${roundData.globalModelCID}`}
                                target="_blank"
                                className="text-xs text-cyan-400 hover:text-cyan-300 underline flex items-center gap-1"
                                rel="noopener noreferrer"
                            >
                                View on IPFS <ExternalLink className="w-3 h-3"/>
                            </a>
                        </CardContent>
                    </Card>
                </section>

                {/* --- Accuracy Chart Section --- */}
                <Card className="bg-slate-800/90 border-slate-700/50">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2 text-xl text-white">
                            <BarChartBig className="w-5 h-5 text-cyan-400" />
                            Node Accuracy Distribution (Round {roundData.round})
                        </CardTitle>
                        <CardDescription className="text-slate-400">
                            Accuracy of individual node updates compared to the global average.
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="w-full h-72 rounded-lg p-4 pt-0"> {/* Removed inner bg */}
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={roundData.updates} margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
                                    <XAxis
                                        dataKey="worker"
                                        stroke="#94a3b8"
                                        fontSize={10}
                                        tickLine={false}
                                        axisLine={false}
                                        tickFormatter={(value) => shorten(value)} // Shorten worker address
                                    />
                                    <YAxis
                                        domain={[0.9, 1]}
                                        stroke="#94a3b8"
                                        fontSize={12}
                                        tickFormatter={(v) => `${(v * 100).toFixed(0)}%`}
                                        tickCount={6}
                                        width={40}
                                    />
                                    <Tooltip
                                        contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '4px' }}
                                        labelStyle={{ color: '#cbd5e1', fontSize: '12px', marginBottom: '4px' }}
                                        itemStyle={{ color: '#e2e8f0', fontSize: '12px' }}
                                        formatter={(value: number, name: string, props: any) => [
                                            `${(value * 100).toFixed(2)}%`,
                                            `Accuracy (Node: ${shorten(props.payload.worker)})`
                                        ]}
                                        cursor={{ fill: 'rgba(100, 116, 139, 0.2)' }}
                                    />
                                    <Bar dataKey="accuracy" fill="#06b6d4" radius={[4, 4, 0, 0]} barSize={40} />
                                    <ReferenceLine
                                        y={roundData.globalAccuracy}
                                        stroke="#f472b6"
                                        strokeDasharray="4 4"
                                        label={{
                                            value: `Global Avg (${(roundData.globalAccuracy * 100).toFixed(1)}%)`,
                                            position: 'insideTopRight',
                                            fill: '#f472b6',
                                            fontSize: 12,
                                            dy: -5, // Adjust vertical position slightly
                                        }}
                                    />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </CardContent>
                </Card>

                {/* --- Node Updates Section --- */}
                <Card className="bg-slate-800/90 border-slate-700/50">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2 text-xl text-white">
                            <ListTree className="w-5 h-5 text-cyan-400" />
                            Node Updates (Round {roundData.round})
                        </CardTitle>
                        <CardDescription className="text-slate-400">
                            Details of individual model updates submitted by participating nodes.
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {roundData.updates.map((update, index) => (
                            <Card key={index} className="bg-slate-800 border border-slate-700 hover:border-slate-600 transition-colors duration-200 shadow-sm hover:shadow-md">
                                <CardContent className="p-4 space-y-3 text-sm">
                                    <div className="flex items-center justify-between">
                                        <span className="font-semibold text-cyan-300 flex items-center gap-2">
                                           <User className="w-4 h-4" /> Node Worker
                                        </span>
                                        <Button
                                            variant="ghost" size="icon"
                                            className="h-6 w-6 text-slate-400 hover:text-white hover:bg-slate-700"
                                            onClick={() => copyToClipboard(update.worker, setCopiedStates, `worker-${index}`)}
                                            aria-label="Copy Worker ID"
                                        >
                                            {copiedStates[`worker-${index}`] ? <ClipboardCopy className="w-4 h-4 text-green-400" /> : <ClipboardCopy className="w-4 h-4" />}
                                        </Button>
                                    </div>
                                     <code className="block text-slate-400 font-mono text-xs break-all">{update.worker}</code>

                                    <div className="text-slate-400 flex items-center gap-2 pt-1"><Hash className="w-4 h-4"/> Model Hash:</div>
                                    <code className="block text-slate-500 font-mono text-xs break-all">{shorten(update.model_hash, 10, 6)}</code>

                                    <div className="text-slate-400 flex items-center gap-2 pt-1"><Fingerprint className="w-4 h-4"/> Signature:</div>
                                    <code className="block text-slate-500 font-mono text-xs break-all">{shorten(update.signature, 10, 6)}</code>

                                     <div className="flex items-center justify-between pt-1">
                                         <span className="text-slate-400 flex items-center gap-2"><FileCode className="w-4 h-4"/> CID:</span>
                                         <Button
                                             variant="ghost" size="icon"
                                             className="h-6 w-6 text-slate-400 hover:text-white hover:bg-slate-700"
                                             onClick={() => copyToClipboard(update.cid, setCopiedStates, `cid-${index}`)}
                                             aria-label="Copy Update CID"
                                         >
                                             {copiedStates[`cid-${index}`] ? <ClipboardCopy className="w-4 h-4 text-green-400" /> : <ClipboardCopy className="w-4 h-4" />}
                                         </Button>
                                     </div>
                                     <code className="block text-slate-500 font-mono text-xs break-all">{update.cid}</code>
                                      <a
                                          href={`https://dweb.link/ipfs/${update.cid}`}
                                          className="text-xs text-cyan-400 hover:text-cyan-300 underline flex items-center gap-1 mt-1"
                                          target="_blank"
                                          rel="noopener noreferrer"
                                      >
                                          View Model File <ExternalLink className="w-3 h-3"/>
                                      </a>

                                    <div className="flex justify-between items-center pt-2">
                                        <span className="text-slate-400 flex items-center gap-2"><Gauge className="w-4 h-4"/> Accuracy:</span>
                                        <span className="font-medium text-white">{(update.accuracy * 100).toFixed(2)}%</span>
                                    </div>
                                    <div className="flex justify-between items-center">
                                         <span className="text-slate-400 flex items-center gap-2"><Clock className="w-4 h-4"/> Timestamp:</span>
                                         <span className="text-slate-400">{new Date(update.timestamp).toLocaleString()}</span>
                                    </div>
                                </CardContent>
                            </Card>
                        ))}
                    </CardContent>
                </Card>

            </main>

            {/* --- Consistent Footer --- */}
            <footer className="mt-12 text-center text-sm text-slate-500 z-10 pb-8">
                Made for the Filecoin AI Blueprints Hackathon · &copy; {new Date().getFullYear()} TrustML Contributors
            </footer>
        </div>
    );
}
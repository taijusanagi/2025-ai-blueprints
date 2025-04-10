"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  LayoutGrid,
  BarChartBig,
  ListTree,
  List,
  ChevronRight,
  ArrowLeft, // Added List, ChevronRight, ArrowLeft
  FileCode,
  User,
  Gauge,
  Clock,
  ExternalLink,
  Activity,
} from "lucide-react";
import {
  Bar,
  BarChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { ethers } from "ethers";
import FederatedTaskManagerABI from "@/abi/FederatedTaskManager.json"; // Save ABI separately

const CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3";

const provider = new ethers.JsonRpcProvider("http://localhost:8545"); // Use appropriate network
const contract = new ethers.Contract(
  CONTRACT_ADDRESS,
  FederatedTaskManagerABI,
  provider
);

const getTasks = async () => {
  const tasks = await contract.getTasks();
  return tasks.map((task: any) => ({
    id: String(task.taskId), // make sure it's string
    schemaHash: task.schemaHash,
    creator: task.creator,
    timestamp: Number(task.timestamp), // convert BigInt to number
    finalModelCID: task.finalModelHash,
    finalAccuracy: Number(task.finalAccuracy) / 10000, // convert + scale
    submissions: task.submissions.map((sub: any) => ({
      modelHash: sub.modelHash,
      submitter: sub.submitter,
      timestamp: Number(sub.timestamp) * 1000, // convert to ms
      accuracy: Number(sub.accuracy) / 10000, // convert + scale
    })),
  }));
};

const generateStorageLink = (cid: string, type: "ipfs") => {
  switch (type) {
    case "ipfs":
      return `https://dweb.link/ipfs/${cid}`;
    default:
      return cid;
  }
};

// Interface for Session Details
interface SessionUpdate {
  worker: string;
  model_hash: string;
  signature: string;
  accuracy: number;
  timestamp: string;
  cid: string;
}

interface SessionDetailData {
  id: string;
  name: string;
  schemaHash: string;
  globalAccuracy: number;
  globalModelCID: string;
  updates: SessionUpdate[];
  status: "Active" | "Completed" | "Paused";
}

// Interface for Session List Item
interface SessionListItem {
  id: string;
  name: string;
  participants: number;
  status: "Active" | "Completed";
}

// --- Helper Functions ---

// Function to shorten strings
const shorten = (str: string, start = 6, end = 4) => {
  if (!str || typeof str !== "string") return "";
  if (str.length <= start + end + 3) return str;
  return `${str.substring(0, start)}...${str.substring(str.length - end)}`;
};

// --- Components ---

// Component to render the list of FL sessions
const SessionList = ({
  sessions,
  onSelectSession,
}: {
  sessions: SessionListItem[];
  onSelectSession: (id: string) => void;
}) => {
  const getStatusColor = (status: SessionListItem["status"]) => {
    switch (status) {
      case "Active":
        return "text-green-400 border-green-400/50 bg-green-500/10";
      case "Completed":
        return "text-blue-400 border-blue-400/50 bg-blue-500/10";
      default:
        return "text-slate-400 border-slate-400/50 bg-slate-500/10";
    }
  };

  return (
    <Card className="bg-slate-800/90 border-slate-700/50">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-xl text-white">
          <List className="w-5 h-5 text-cyan-400" />
          Federated Learning Sessions
        </CardTitle>
        <CardDescription className="text-slate-400">
          Select a session to view its details and progress.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {sessions.map((session) => (
          <button
            key={session.id}
            onClick={() => onSelectSession(session.id)}
            className="w-full text-left p-4 rounded-md border border-slate-700 bg-slate-800 hover:bg-slate-700/50 hover:border-slate-600 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:ring-offset-2 focus:ring-offset-slate-900 cursor-pointer"
          >
            <div className="flex justify-between items-center">
              <div>
                <h3 className="font-semibold text-white">{session.name}</h3>
                <p className="text-sm text-slate-400 mt-1">
                  Participants: {session.participants}
                </p>
              </div>
              <div className="flex items-center gap-3">
                <span
                  className={`text-xs font-medium px-2.5 py-0.5 rounded-full border ${getStatusColor(
                    session.status
                  )}`}
                >
                  {session.status}
                </span>
                <ChevronRight className="w-5 h-5 text-slate-500" />
              </div>
            </div>
          </button>
        ))}
      </CardContent>
    </Card>
  );
};

// Component to render the detailed view of a selected session
const SessionDetail = ({
  sessionData,
  onBack,
  copiedStates,
  setCopiedStates,
}: {
  sessionData: SessionDetailData | undefined;
  onBack: () => void;
  copiedStates: { [key: string]: boolean };
  setCopiedStates: Function;
}) => {
  if (!sessionData) {
    // Handle case where data might not be found (optional)
    return (
      <div className="text-center py-10">
        <p className="text-red-500">Error: Session data not found.</p>
        <Button variant="outline" onClick={onBack} className="mt-4">
          <ArrowLeft className="mr-2 h-4 w-4" /> Back to List
        </Button>
      </div>
    );
  }

  // Status color helper for detail view badges
  const getDetailStatusStyle = (status: SessionDetailData["status"]) => {
    switch (status) {
      case "Active":
        return "bg-green-500/20 text-green-300 border-green-400/30";
      case "Completed":
        return "bg-blue-500/20 text-blue-300 border-blue-400/30";
      case "Paused":
        return "bg-yellow-500/20 text-yellow-300 border-yellow-400/30";
      default:
        return "bg-slate-500/20 text-slate-300 border-slate-400/30";
    }
  };

  return (
    <div className="space-y-8">
      {/* Back Button and Title */}
      <div className="flex items-center justify-between mb-6">
        <Button
          variant="outline"
          size="sm"
          onClick={onBack}
          className="bg-slate-800 border-slate-700 hover:bg-slate-700"
        >
          <ArrowLeft className="mr-2 h-4 w-4" /> Back to List
        </Button>
        <span
          className={`inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 ${getDetailStatusStyle(
            sessionData.status
          )}`}
        >
          <Activity className="w-3 h-3 mr-1.5" /> {sessionData.status}
        </span>
      </div>

      <h1 className="text-3xl font-bold text-white flex items-center gap-3">
        <LayoutGrid className="w-7 h-7 text-cyan-400" />
        {sessionData.name}
      </h1>
      <div className="ml-10 mt-1 text-sm text-slate-400">
        Schema CID:{" "}
        <code className="text-slate-300 font-mono">
          {shorten(sessionData.schemaHash, 10, 6)}
        </code>
      </div>

      {/* Global Stats Section */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="bg-slate-800/90 border-slate-700/50">
          <CardHeader className="pb-2">
            <CardDescription className="text-slate-400">
              Participants
            </CardDescription>
            <CardTitle className="text-3xl text-cyan-300">
              {sessionData.updates ? sessionData.updates.length : 0}
            </CardTitle>
          </CardHeader>
        </Card>
        {sessionData.globalAccuracy > 0 && (
          <>
            <Card className="bg-slate-800/90 border-slate-700/50">
              <CardHeader className="pb-2">
                <CardDescription className="text-slate-400">
                  Global Accuracy
                </CardDescription>
                <CardTitle className="text-3xl text-pink-400">
                  {sessionData.globalAccuracy * 100} %
                </CardTitle>
              </CardHeader>
            </Card>
            <Card className="bg-slate-800/90 border-slate-700/50">
              <CardHeader className="pb-2">
                <CardDescription className="text-slate-400">
                  Global Model CID
                </CardDescription>
                <CardTitle className="text-lg text-slate-300 font-mono flex items-center gap-2">
                  {shorten(sessionData.globalModelCID, 10, 6)}
                </CardTitle>
              </CardHeader>
            </Card>
          </>
        )}
      </section>

      {/* Accuracy Chart Section */}
      <Card className="bg-slate-800/90 border-slate-700/50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-xl text-white">
            <BarChartBig className="w-5 h-5 text-cyan-400" />
            Node Accuracy Distribution
          </CardTitle>
          <CardDescription className="text-slate-400">
            Accuracy of individual node updates compared to the global average.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="w-full h-72 rounded-lg p-4 pt-0">
            {sessionData.updates && sessionData.updates.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={sessionData.updates}
                  margin={{ top: 5, right: 20, left: -10, bottom: 5 }}
                >
                  {/* ... (XAxis, YAxis, Tooltip, Bar, ReferenceLine - same as before, using sessionData) ... */}
                  <XAxis
                    dataKey="worker"
                    stroke="#94a3b8"
                    fontSize={10}
                    tickLine={false}
                    axisLine={false}
                    tickFormatter={(value) => shorten(value)}
                  />
                  <YAxis
                    domain={[0, 1]}
                    tickFormatter={(v) => `${(v * 100).toFixed(0)}%`}
                    stroke="#94a3b8"
                    fontSize={12}
                    tickCount={6}
                    width={40}
                    allowDataOverflow={true}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#1e293b",
                      border: "1px solid #334155",
                      borderRadius: "4px",
                    }}
                    labelStyle={{
                      color: "#cbd5e1",
                      fontSize: "12px",
                      marginBottom: "4px",
                    }}
                    itemStyle={{ color: "#e2e8f0", fontSize: "12px" }}
                    formatter={(value: number, name: string, props: any) => [
                      `${(value * 100).toFixed(2)}%`,
                      `Accuracy (Node: ${shorten(props.payload.worker)})`,
                    ]}
                    cursor={{ fill: "rgba(100, 116, 139, 0.2)" }}
                  />
                  <Bar
                    dataKey="accuracy"
                    fill="#06b6d4"
                    radius={[4, 4, 0, 0]}
                    barSize={40}
                  />
                  {sessionData.globalAccuracy > 0 && (
                    <ReferenceLine
                      y={sessionData.globalAccuracy}
                      stroke="#f472b6"
                      strokeDasharray="4 4"
                      label={{
                        value: `Global Avg (${(
                          sessionData.globalAccuracy * 100
                        ).toFixed(2)}%)`,
                        position: "insideTopRight",
                        fill: "#f472b6",
                        fontSize: 12,
                        dy: -5,
                      }}
                    />
                  )}
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-full text-slate-500">
                No node updates available for this round.
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Node Updates Section */}
      <Card className="bg-slate-800/90 border-slate-700/50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-xl text-white">
            <ListTree className="w-5 h-5 text-cyan-400" />
            Node Updates
          </CardTitle>
          <CardDescription className="text-slate-400">
            Details of individual model updates submitted by participating
            nodes.
          </CardDescription>
        </CardHeader>
        <CardContent className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {sessionData.updates && sessionData.updates.length > 0 ? (
            sessionData.updates.map((update, index) => (
              <Card
                key={index}
                className="bg-slate-800 border border-slate-700 hover:border-slate-600 transition-colors duration-200 shadow-sm hover:shadow-md"
              >
                <CardContent className="p-4 space-y-3 text-sm">
                  {/* ... (Node update card content - same as before, using update.* data) ... */}
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-cyan-300 flex items-center gap-2">
                      <User className="w-4 h-4" /> Node Worker
                    </span>
                  </div>
                  <code className="block text-slate-400 font-mono text-xs break-all">
                    {update.worker}
                  </code>
                  <div className="flex items-center justify-between pt-1">
                    <span className="text-slate-400 flex items-center gap-2">
                      <FileCode className="w-4 h-4" /> Node Model CID:
                    </span>
                  </div>
                  <code className="block text-slate-500 font-mono text-xs break-all">
                    {shorten(update.cid, 20, 19)}
                  </code>
                  <div className="flex justify-between items-center pt-2">
                    <span className="text-slate-400 flex items-center gap-2">
                      <Gauge className="w-4 h-4" /> Accuracy:
                    </span>
                    <span className="font-medium text-white">
                      {update.accuracy}%
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-400 flex items-center gap-2">
                      <Clock className="w-4 h-4" /> Timestamp:
                    </span>
                    <span className="text-slate-400">
                      {new Date(update.timestamp).toLocaleString()}
                    </span>
                  </div>
                </CardContent>
              </Card>
            ))
          ) : (
            <div className="col-span-full text-center text-slate-500 py-6">
              No node updates submitted for this round yet.
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

// --- Main Dashboard Page Component ---

export default function DashboardPage() {
  const [selectedSessionId, setSelectedSessionId] = useState<string | null>(
    null
  );
  const [copiedStates, setCopiedStates] = useState<{ [key: string]: boolean }>(
    {}
  );
  const [sessionList, setSessionList] = useState<SessionListItem[]>([]);
  const [detailedSessions, setDetailedSessions] = useState<SessionDetailData[]>(
    []
  );

  useEffect(() => {
    const fetchTasksFromContract = async () => {
      try {
        const taskList = (await getTasks()).reverse();
        console.log("Fetched tasks:", taskList);

        const sessions: SessionListItem[] = taskList.map((task: any) => ({
          id: task.id,
          name: `Task ${task.id}`,
          participants: task.submissions.length,
          status: task.finalModelCID ? "Completed" : "Active",
        }));

        const detailed: SessionDetailData[] = taskList.map((task: any) => ({
          id: task.id,
          name: `Task ${task.id}`,
          schemaHash: task.schemaHash,
          globalAccuracy: task.finalAccuracy,
          globalModelCID: task.finalModelCID,
          status: task.finalModelCID ? "Completed" : "Active",
          updates: task.submissions.map((sub: any) => ({
            worker: sub.submitter,
            model_hash: sub.modelHash,
            signature: "", // You don't have this on-chain; leave blank or fetch from IPFS if available
            accuracy: sub.accuracy,
            timestamp: sub.timestamp,
            cid: sub.modelHash, // Assuming modelHash is a CID; update if needed
          })),
        }));

        setSessionList(sessions);
        setDetailedSessions(detailed);
      } catch (err) {
        console.error("Error fetching tasks:", err);
      }
    };

    fetchTasksFromContract();
  }, []);

  const handleSelectSession = (id: string) => {
    setCopiedStates({}); // Reset copied states when changing views
    setSelectedSessionId(id);
  };

  const handleGoBack = () => {
    setCopiedStates({}); // Reset copied states when changing views
    setSelectedSessionId(null);
  };

  // Get the detailed data for the selected session
  const currentSessionData = detailedSessions.find(
    (s) => s.id === selectedSessionId
  );

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-black text-slate-200 flex flex-col">
      {/* Consistent Header */}
      <header className="sticky top-0 z-50 w-full bg-slate-900/95 border-b border-slate-700/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto flex justify-between items-center py-4 px-4 sm:px-6 lg:px-8">
          <Link
            href="/"
            className="text-xl font-semibold tracking-tight text-white hover:text-cyan-300 transition-colors duration-200"
          >
            TrustML
          </Link>
          <nav className="flex gap-5 sm:gap-6 text-sm font-medium">
            <Link
              href="https://github.com/taijusanagi/2025-ai-blueprints"
              target="_blank"
              className="text-slate-300 hover:text-cyan-400 transition-colors duration-200"
              rel="noopener noreferrer"
            >
              Docs
            </Link>
            <Link href="/dashboard" className="text-pink-400">
              Dashboard
            </Link>
          </nav>
        </div>
      </header>

      {/* Main Content Area (Conditional Rendering) */}
      <main className="flex-grow w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {selectedSessionId === null ? (
          // Show the list if no session is selected
          <SessionList
            sessions={sessionList}
            onSelectSession={handleSelectSession}
          />
        ) : (
          // Show the detail view for the selected session
          <SessionDetail
            sessionData={currentSessionData}
            onBack={handleGoBack}
            copiedStates={copiedStates}
            setCopiedStates={setCopiedStates}
          />
        )}
      </main>

      {/* Consistent Footer */}
      <footer className="mt-auto text-center text-sm text-slate-500 z-10 pb-8 pt-8">
        {" "}
        {/* Use mt-auto to push footer down */}
        Made for the Filecoin AI Blueprints Hackathon · &copy;{" "}
        {new Date().getFullYear()} TrustML Contributors
      </footer>
    </div>
  );
}

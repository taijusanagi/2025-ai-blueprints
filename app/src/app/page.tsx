import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  ArrowRightCircle,
  ShieldCheck,
  GitBranch,
  DatabaseZap,
  ClipboardCopy,
} from "lucide-react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { atomDark } from "react-syntax-highlighter/dist/cjs/styles/prism";

import Link from "next/link";

export default function TrustMLLandingPage() {
  return (
    // --- Main Container --- (removed overflow-x-hidden)
    <main className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-black text-slate-200 flex flex-col items-center px-4 sm:px-6 pt-0 relative">
      {/* --- Background Effects --- */}
      <div
        aria-hidden="true"
        className="fixed inset-0 -z-10 pointer-events-none"
      >
        {/* Simpler Grid Pattern - using CSS variables instead of complex gradient */}
        <div
          className="absolute inset-0"
          style={{
            backgroundImage:
              "radial-gradient(rgba(100,116,139,0.05) 1px, transparent 1px)",
            backgroundSize: "32px 32px",
          }}
        ></div>
        {/* Static Blobs - fixed position and simplified */}
        <div className="fixed w-72 h-72 md:w-96 md:h-96 bg-cyan-600/5 rounded-full blur-3xl top-0 left-0 opacity-50"></div>
        <div className="fixed w-72 h-72 md:w-96 md:h-96 bg-purple-600/5 rounded-full blur-3xl bottom-0 right-0 opacity-50"></div>
      </div>

      {/* --- Header --- */}
      {/* Replaced backdrop-blur with solid background */}
      <header className="w-full bg-slate-900/95 border-b border-slate-700/50">
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
            <Link
              href="/dashboard"
              className="text-slate-300 hover:text-pink-400 transition-colors duration-200"
            >
              Dashboard
            </Link>
          </nav>
        </div>
      </header>

      {/* --- Hero Section --- */}
      <section className="text-center max-w-4xl pt-24 md:pt-32 z-10 w-full">
        <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold tracking-tight leading-tight text-transparent bg-clip-text bg-gradient-to-r from-white via-slate-200 to-slate-400">
          Build <span className="text-cyan-400">Trustable</span>,{" "}
          <span className="text-pink-400">Decentralized</span> AI
        </h1>
        <p className="mt-6 text-lg md:text-xl text-slate-400 max-w-2xl mx-auto">
          TrustML is a verifiable, multi-node machine learning platform built on
          <span className="text-white font-semibold"> Filecoin </span> and
          <span className="text-white font-semibold"> Akave</span>, enabling
          decentralized AI training with cryptographic integrity and secure
          storage.
        </p>
        <div className="mt-10 flex flex-col sm:flex-row justify-center items-center gap-4">
          <Button
            size="lg"
            className="group bg-gradient-to-r from-cyan-500 to-purple-600 text-white font-semibold shadow-lg hover:from-cyan-400 hover:to-purple-500 transition-all duration-300 ease-in-out transform hover:-translate-y-0.5 w-full sm:w-auto"
            asChild
          >
            <Link href="/dashboard">
              Launch Dashboard
              <ArrowRightCircle className="ml-2 h-5 w-5 transition-transform duration-300 group-hover:translate-x-1" />
            </Link>
          </Button>
          <Button
            size="lg"
            variant="outline"
            className="bg-transparent border border-slate-600 text-slate-300 hover:bg-slate-800 hover:text-white hover:border-slate-500 transition-all duration-300 ease-in-out transform hover:-translate-y-0.5 w-full sm:w-auto"
            asChild
          >
            <Link
              href="https://github.com/taijusanagi/2025-ai-blueprints"
              target="_blank"
              rel="noopener noreferrer"
            >
              GitHub
            </Link>
          </Button>
        </div>
      </section>

      {/* --- Features Section --- */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8 mt-24 md:mt-32 max-w-6xl w-full z-10 px-4">
        {[
          {
            icon: GitBranch,
            title: "Federated Averaging",
            description:
              "Utilizes FedAvg algorithm to securely aggregate verified model contributions across nodes.",
          },
          {
            icon: ShieldCheck,
            title: "Verifiable Training with Privacy",
            description:
              "Each model update is hashed, signed, and anchored on-chain, all without sharing their raw data.",
          },
          {
            icon: DatabaseZap,
            title: "Powered by Filecoin & Akave",
            description:
              "Leverages decentralized storage for robust model weight and metadata persistence and auditability.",
          },
        ].map((feature, index) => (
          <Card
            key={index}
            className="group bg-slate-800/90 border border-slate-700/50 rounded-lg transition-all duration-300 ease-in-out hover:border-slate-600 hover:bg-slate-800 hover:-translate-y-1 shadow-md hover:shadow-lg"
          >
            <CardContent className="p-6">
              <feature.icon
                aria-hidden="true"
                className="w-8 h-8 mb-4 text-cyan-400 group-hover:scale-110 transition-transform duration-300"
              />
              <h2 className="text-xl font-semibold text-white mb-2 transition-colors duration-300 group-hover:text-cyan-300">
                {feature.title}
              </h2>
              <p className="text-slate-400 text-sm">{feature.description}</p>
            </CardContent>
          </Card>
        ))}
      </section>

      {/* --- Call to Action / Installation --- */}
      <section className="mt-24 md:mt-32 text-center max-w-3xl w-full z-10 px-4">
        <h3 className="text-3xl font-bold mb-4 text-white">
          Get Started with TrustML
        </h3>
        <p className="text-slate-400 mb-6">
          Integrate verifiable federated learning into your project with our
          SDK.
        </p>
        <div className="relative bg-slate-900 border border-slate-700 rounded-lg p-6 font-mono text-sm shadow-xl max-w-md mx-auto">
          {/* Terminal Window Bar */}
          <div className="absolute top-3 left-4 flex space-x-1.5">
            <span className="w-3 h-3 rounded-full bg-red-500"></span>
            <span className="w-3 h-3 rounded-full bg-yellow-500"></span>
            <span className="w-3 h-3 rounded-full bg-green-500"></span>
          </div>
          {/* Copy Button */}
          <button
            aria-label="Copy code"
            className="absolute top-3 right-3 p-1.5 bg-slate-700 rounded-md text-slate-400 hover:text-white hover:bg-slate-600 transition-colors duration-200"
          >
            <ClipboardCopy className="w-4 h-4" />
          </button>
          {/* Code Content */}
          <code className="block text-left mt-6 text-green-400 whitespace-nowrap overflow-x-auto">
            <span className="text-slate-500 mr-2">$</span>pip install trustml
          </code>
        </div>
      </section>

      {/* --- How It Works Section (Diagram & Code) --- */}
      <section className="mt-24 md:mt-32 max-w-6xl w-full z-10 px-4 mx-auto">
        <h3 className="text-3xl font-bold mb-10 text-white text-center">
          How TrustML Works
        </h3>

        <div className="flex flex-col lg:flex-row gap-10 lg:gap-12 items-center justify-center">
          {/* Diagram Side */}
          <div className="lg:w-1/2 w-full flex justify-center items-center flex-shrink-0">
            <img
              src="/diagram.png"
              alt="TrustML Architecture Diagram"
              width={500}
              height={400}
              loading="lazy"
              className="rounded-lg shadow-xl border border-slate-700/50 bg-slate-800/30 object-contain"
            />
          </div>

          {/* Code Example Side */}
          <div className="lg:w-1/2 w-full">
            <div className="relative bg-slate-900 border border-slate-700 rounded-lg shadow-xl font-mono text-sm">
              <div className="flex items-center justify-between px-4 py-2 border-b border-slate-700">
                <span className="text-xs text-slate-400">example.py</span>
                <button
                  aria-label="Copy code"
                  className="p-1.5 bg-slate-700 rounded-md text-slate-400 hover:text-white hover:bg-slate-600 transition-colors duration-200"
                >
                  <ClipboardCopy className="w-4 h-4" />
                </button>
              </div>

              <SyntaxHighlighter
                language="python"
                style={atomDark}
                customStyle={{
                  margin: 0,
                  padding: "1rem",
                  backgroundColor: "transparent",
                }}
              >
                {`import trustml

# Sample schema
schema = {
  "task": "iris_classification",
  "input_shape": [4],
  "num_classes": 3,
  "features": ["sepal length", "sepal width", "petal length", "petal width"],
  "model_architecture": [
    {"type": "Dense", "units": 10, "activation": "relu"},
    {"type": "Dense", "units": 3, "activation": "softmax"}
  ]
}

# 1. Create a federated task
sdk = trustml.FederatedLearningSDK(...)
sdk.create_task(task_id, schema)

# 2. Train and submit local model (your data is private, never exposed)
model = sdk.build_model_from_schema(sdk.get_task_schema(task_id))
model.fit(X_train, y_train, epochs=5)
_, acc = model.evaluate(X_test, y_test)  # submit acc
sdk.submit_model(task_id, model.get_weights(), acc)

# 3. Aggregate and submit final model
agg_path = sdk.aggregate_models(task_id)
model.load_weights(agg_path)
_, final_acc = model.evaluate(X, y)  # final acc
sdk.submit_final_model(task_id, agg_path, final_acc)

`}
              </SyntaxHighlighter>
            </div>
          </div>
        </div>
      </section>

      <section className="mt-24 md:mt-32 max-w-6xl w-full z-10 px-4 mx-auto">
        <h3 className="text-3xl font-bold mb-10 text-white text-center">
          Technical Deep Dive
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Filecoin Card */}
          <Card className="group bg-slate-800/90 border border-slate-700/50 rounded-lg transition-all duration-300 ease-in-out hover:border-slate-600 hover:bg-slate-800 shadow-md hover:shadow-lg flex flex-col">
            {" "}
            {/* Added flex flex-col */}
            <CardContent className="p-6 flex-grow">
              {" "}
              {/* Added flex-grow */}
              <GitBranch
                aria-hidden="true"
                className="w-8 h-8 mb-4 text-cyan-400 group-hover:scale-110 transition-transform duration-300"
              />
              <h4 className="text-xl font-semibold text-white mb-3 transition-colors duration-300 group-hover:text-cyan-300">
                Filecoin: Immutable Ledger
              </h4>
              <p className="text-slate-400 text-sm mb-3">
                Filecoin provides the verifiable foundation. A smart contract
                records metadata (participants, rounds) and Content Identifiers
                (CIDs) pointing to proofs stored immutably on Filecoin.
              </p>
              <ul className="list-disc list-outside text-slate-400 text-sm space-y-1 pl-5 mb-3">
                <li>
                  <span className="font-semibold text-slate-300">
                    Proofs Include:
                  </span>{" "}
                  Hash of model update (integrity), participant's signature
                  (authenticity).
                </li>
                <li>
                  <span className="font-semibold text-slate-300">Benefit:</span>{" "}
                  Creates a tamper-proof, verifiable audit trail for every
                  contribution, enabling reproducible AI pipelines.
                </li>
              </ul>
              <p className="text-slate-400 text-sm">
                This complements federated learning's privacy by ensuring
                process integrity and transparency.
              </p>
            </CardContent>
          </Card>

          {/* Akave Card */}
          <Card className="group bg-slate-800/90 border border-slate-700/50 rounded-lg transition-all duration-300 ease-in-out hover:border-slate-600 hover:bg-slate-800 shadow-md hover:shadow-lg flex flex-col">
            {" "}
            {/* Added flex flex-col */}
            <CardContent className="p-6 flex-grow">
              {" "}
              {/* Added flex-grow */}
              <DatabaseZap
                aria-hidden="true"
                className="w-8 h-8 mb-4 text-pink-400 group-hover:scale-110 transition-transform duration-300" // Changed color to pink
              />
              <h4 className="text-xl font-semibold text-white mb-3 transition-colors duration-300 group-hover:text-pink-300">
                {" "}
                {/* Changed hover color */}
                Akave: Resilient Model Storage
              </h4>
              <p className="text-slate-400 text-sm mb-3">
                Akave offers decentralized storage optimized for AI artifacts
                like model weights and schemas, enhancing resilience and
                availability.
              </p>
              <ul className="list-disc list-outside text-slate-400 text-sm space-y-1 pl-5 mb-3">
                <li>
                  <span className="font-semibold text-slate-300">
                    Mechanism:
                  </span>{" "}
                  Uses content-addressing for data consistency. The SDK handles
                  efficient uploads and downloads.
                </li>
                <li>
                  <span className="font-semibold text-slate-300">Benefit:</span>{" "}
                  Provides low-latency access needed for aggregation and bridges
                  standard AI tools (TensorFlow) with robust Web3 storage.
                </li>
              </ul>
              <p className="text-slate-400 text-sm">
                This decouples AI workflows from centralized bottlenecks,
                enabling more flexible and interoperable data pipelines.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* --- Footer --- */}
      <footer className="mt-28 md:mt-36 text-center text-sm text-slate-500 z-10 pb-8">
        Made for the Filecoin AI Blueprints Hackathon · &copy;{" "}
        {new Date().getFullYear()} TrustML Contributors
      </footer>
    </main>
  );
}

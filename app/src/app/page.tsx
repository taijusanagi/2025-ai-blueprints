import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { ArrowRightCircle } from "lucide-react";
import Link from "next/link";

export default function TrustMLLandingPage() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-[#0f0c29] via-[#302b63] to-[#24243e] text-white flex flex-col items-center px-6 pt-0 pb-16 relative overflow-hidden">
      {/* Fancy Background Effect */}
      <div className="absolute inset-0 -z-10 pointer-events-none">
        <div className="absolute w-96 h-96 bg-pink-500/20 rounded-full blur-3xl top-[-5rem] left-[-5rem] animate-pulse"></div>
        <div className="absolute w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl bottom-[-5rem] right-[-5rem] animate-pulse"></div>
      </div>

      {/* Header */}
      <header className="w-full flex justify-between items-center py-6 px-4 md:px-10 text-white text-sm z-10">
        <div className="text-lg font-bold tracking-wide">TrustML</div>
        <nav className="flex gap-6">
          <Link href="/docs" className="hover:text-cyan-300 transition-colors">Docs</Link>
          <Link href="/dashboard" className="hover:text-pink-300 transition-colors">Dashboard</Link>
        </nav>
      </header>

      <section className="text-center max-w-4xl pt-20">
        <h1 className="text-4xl md:text-6xl font-extrabold leading-tight">
          Build <span className="text-cyan-400">Trustable</span>, <span className="text-pink-400">Decentralized</span> AI
        </h1>
        <p className="mt-6 text-lg md:text-xl text-gray-300 max-w-2xl mx-auto">
          TrustML lets multiple nodes train ML models with verified contributions. Powered by Filecoin, Merkle trees, and smart contracts.
        </p>
        <div className="mt-10 flex justify-center gap-4">
          <Button size="lg" className="bg-gradient-to-r from-cyan-400 to-purple-500 text-black font-semibold shadow-lg hover:from-cyan-300 hover:to-purple-400 transition-transform hover:scale-105">
            Launch Dashboard <ArrowRightCircle className="ml-2 h-5 w-5" />
          </Button>
          <Button size="lg" className="border border-white text-white hover:bg-white hover:text-black transition-all hover:scale-105">
            GitHub
          </Button>
        </div>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-20 max-w-5xl w-full">
        <Card className="bg-white/5 backdrop-blur-md border border-white/10 transition-transform hover:scale-105">
          <CardContent className="p-6">
            <h2 className="text-xl font-bold text-white mb-2">🔐 Verifiable Training</h2>
            <p className="text-gray-200">Each model update is signed, hashed, and stored on-chain and on Filecoin.</p>
          </CardContent>
        </Card>
        <Card className="bg-white/5 backdrop-blur-md border border-white/10 transition-transform hover:scale-105">
          <CardContent className="p-6">
            <h2 className="text-xl font-bold text-white mb-2">🌍 Federated Averaging</h2>
            <p className="text-gray-200">TrustML uses FedAvg to combine only verified contributions across nodes.</p>
          </CardContent>
        </Card>
        <Card className="bg-white/5 backdrop-blur-md border border-white/10 transition-transform hover:scale-105">
          <CardContent className="p-6">
            <h2 className="text-xl font-bold text-white mb-2">📦 Powered by Filecoin</h2>
            <p className="text-gray-200">Model weights and metadata are stored on decentralized storage for auditability.</p>
          </CardContent>
        </Card>
      </section>

      <section className="mt-28 text-center">
        <h3 className="text-2xl font-semibold mb-4 text-white">🧪 Try It in Your Project</h3>
        <p className="text-gray-300 mb-4">Install the SDK and start verifying your federated training jobs:</p>
        <div className="relative inline-block bg-black/30 border border-white/20 px-6 py-4 rounded text-green-400 font-mono text-sm text-left shadow-lg">
          <div className="absolute top-0 left-0 w-[2px] h-full bg-green-400 animate-blink"></div>
          <code className="whitespace-nowrap">
            <span className="animate-typewriter">pip install trustml</span>
          </code>
        </div>
      </section>

      <section className="mt-20 max-w-4xl text-left">
        <h3 className="text-2xl font-semibold mb-4 text-white text-center">🚀 Example: Using TrustML with TensorFlow</h3>
        <pre className="bg-black/40 rounded p-4 text-sm text-green-300 font-mono overflow-x-auto">
{`import trustml
import tensorflow as tf

# Define your local model
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

# Load your local data
x_train, y_train = trustml.utils.load_partition("node1")

# Train locally
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=1)

# Submit weights to aggregator
trustml.submit_update(model.get_weights())

# Fetch global model after FedAvg
global_weights = trustml.fetch_global_model()
model.set_weights(global_weights)`}
        </pre>
      </section>

      <footer className="mt-24 text-sm text-gray-400">
        Made for the Filecoin AI Blueprints Hackathon · 2025
      </footer>
    </main>
  );
}

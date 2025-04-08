import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card"; // Assuming Card/CardContent are simple wrappers like divs
import { ArrowRightCircle, ShieldCheck, GitBranch, DatabaseZap, ClipboardCopy } from "lucide-react";
import Link from "next/link";

export default function TrustMLLandingPage() {
  return (
    // --- Main Container ---
    <main className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-black text-slate-200 flex flex-col items-center px-4 sm:px-6 pt-0 pb-16 relative overflow-x-hidden">

      {/* --- Background Effects --- */}
      <div aria-hidden="true" className="absolute inset-0 -z-10 pointer-events-none">
        {/* Subtle Grid Pattern */}
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_rgba(100,116,139,0.05)_1px,_transparent_1px)] [background-size:32px_32px]"></div>
        {/* Animated Blobs */}
        <div className="absolute w-72 h-72 md:w-96 md:h-96 bg-cyan-600/10 rounded-full blur-3xl filter top-[-6rem] left-[-6rem] animate-pulse duration-3000 opacity-70"></div>
        <div className="absolute w-72 h-72 md:w-96 md:h-96 bg-purple-600/10 rounded-full blur-3xl filter bottom-[-6rem] right-[-6rem] animate-pulse duration-4000 opacity-70"></div>
      </div>

      {/* --- Header --- */}
      <header className="w-full sticky top-0 z-50 backdrop-blur-lg bg-slate-900/75 border-b border-slate-700/50">
        <div className="max-w-7xl mx-auto flex justify-between items-center py-4 px-4 sm:px-6 lg:px-8">
          <Link href="/" className="text-xl font-semibold tracking-tight text-white hover:text-cyan-300 transition-colors duration-200">
            TrustML
          </Link>
          <nav className="flex gap-5 sm:gap-6 text-sm font-medium">
            <Link href="/docs" className="text-slate-300 hover:text-cyan-400 transition-colors duration-200">Docs</Link>
            <Link href="/dashboard" className="text-slate-300 hover:text-pink-400 transition-colors duration-200">Dashboard</Link>
          </nav>
        </div>
      </header>

      {/* --- Hero Section --- */}
      <section className="text-center max-w-4xl pt-24 md:pt-32 z-10">
        <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold tracking-tight leading-tight text-transparent bg-clip-text bg-gradient-to-r from-white via-slate-200 to-slate-400">
          Build <span className="text-cyan-400">Trustable</span>, <span className="text-pink-400">Decentralized</span> AI
        </h1>
        <p className="mt-6 text-lg md:text-xl text-slate-400 max-w-2xl mx-auto">
          TrustML enables verifiable, multi-node machine learning model training, secured by Filecoin, Merkle proofs, and smart contracts.
        </p>
        <div className="mt-10 flex flex-col sm:flex-row justify-center items-center gap-4">
          <Button
            size="lg"
            className="group bg-gradient-to-r from-cyan-500 to-purple-600 text-white font-semibold shadow-lg hover:shadow-xl hover:shadow-cyan-500/30 hover:from-cyan-400 hover:to-purple-500 transition-all duration-300 ease-in-out transform hover:-translate-y-0.5 w-full sm:w-auto"
            asChild // Use asChild if Button wraps a Link
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
             <Link href="https://github.com" target="_blank" rel="noopener noreferrer"> {/* Replace with actual GitHub link */}
               GitHub
             </Link>
          </Button>
        </div>
      </section>

      {/* --- Features Section --- */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8 mt-24 md:mt-32 max-w-6xl w-full z-10">
        {[
          { icon: ShieldCheck, title: "Verifiable Training", description: "Each model update is signed, cryptographically hashed, and anchored on-chain & Filecoin." },
          { icon: GitBranch, title: "Federated Averaging", description: "Utilizes FedAvg algorithm to securely aggregate verified model contributions across nodes." },
          { icon: DatabaseZap, title: "Powered by Filecoin", description: "Leverages decentralized storage for robust model weight and metadata persistence and auditability." }
        ].map((feature, index) => (
          <Card key={index} className="group bg-slate-800/40 backdrop-blur-md border border-slate-700/50 rounded-lg transition-all duration-300 ease-in-out hover:border-slate-600 hover:bg-slate-800/60 hover:-translate-y-1 shadow-md hover:shadow-lg">
            <CardContent className="p-6">
              <feature.icon aria-hidden="true" className="w-8 h-8 mb-4 text-cyan-400 group-hover:scale-110 transition-transform duration-300" />
              <h2 className="text-xl font-semibold text-white mb-2 transition-colors duration-300 group-hover:text-cyan-300">{feature.title}</h2>
              <p className="text-slate-400 text-sm">{feature.description}</p>
            </CardContent>
          </Card>
        ))}
      </section>

      {/* --- Call to Action / Installation --- */}
      <section className="mt-24 md:mt-32 text-center max-w-3xl w-full z-10">
        <h3 className="text-3xl font-bold mb-4 text-white">Get Started with TrustML</h3>
        <p className="text-slate-400 mb-6">Integrate verifiable federated learning into your project with our SDK.</p>
        <div className="relative bg-slate-900 border border-slate-700 rounded-lg p-6 font-mono text-sm shadow-xl max-w-md mx-auto">
          {/* Terminal Window Bar */}
          <div className="absolute top-3 left-4 flex space-x-1.5">
              <span className="w-3 h-3 rounded-full bg-red-500"></span>
              <span className="w-3 h-3 rounded-full bg-yellow-500"></span>
              <span className="w-3 h-3 rounded-full bg-green-500"></span>
          </div>
          {/* Copy Button (Visual Only) */}
           <button aria-label="Copy code" className="absolute top-3 right-3 p-1.5 bg-slate-700 rounded-md text-slate-400 hover:text-white hover:bg-slate-600 transition-colors duration-200">
              <ClipboardCopy className="w-4 h-4" />
           </button>
           {/* Code Content */}
          <code className="block text-left mt-6 text-green-400 whitespace-nowrap overflow-x-auto">
            <span className="text-slate-500 mr-2">$</span>pip install trustml
          </code>
        </div>
      </section>

      {/* --- How It Works Section (Diagram & Code) --- */}
      <section className="mt-24 md:mt-32 max-w-6xl w-full z-10">
        <h3 className="text-3xl font-bold mb-10 text-white text-center">How TrustML Works with TensorFlow</h3>
        <div className="flex flex-col lg:flex-row gap-10 lg:gap-12 items-start">

          {/* Diagram Side */}
          <div className="lg:w-1/2 w-full flex justify-center items-center flex-shrink-0">
             {/* Placeholder - Replace with actual Image component or img tag */}
             <img
              src="/diagram.png" // Use a placeholder or your actual diagram path
              alt="TrustML Architecture Diagram"
              width={500}
              height={400}
              className="rounded-lg shadow-xl border border-slate-700/50 bg-slate-800/30 object-contain" // Added background for visibility if SVG/transparent
            />
          </div>

          {/* Code Example Side */}
          <div className="lg:w-1/2 w-full">
            <div className="relative bg-slate-900/80 backdrop-blur-sm border border-slate-700 rounded-lg shadow-xl font-mono text-sm">
              {/* Code Block Header */}
               <div className="flex items-center justify-between px-4 py-2 border-b border-slate-700">
                  <span className="text-xs text-slate-400">example.py</span>
                  <button aria-label="Copy code" className="p-1.5 bg-slate-700 rounded-md text-slate-400 hover:text-white hover:bg-slate-600 transition-colors duration-200">
                      <ClipboardCopy className="w-4 h-4" />
                  </button>
               </div>
              {/* Code Content Area */}
              <pre className="p-4 text-slate-300 overflow-x-auto">
{`import trustml
import tensorflow as tf

# 1. Define your local model architecture
model = tf.keras.models.Sequential([
  tf.keras.layers.Dense(64, activation='relu'),
  tf.keras.layers.Dense(10, activation='softmax')
])

# 2. Load node-specific training data
(x_train, y_train), _ = trustml.load_partition("node-01")

# 3. Compile and train locally
model.compile(
  optimizer='adam',
  loss='sparse_categorical_crossentropy',
  metrics=['accuracy']
)
model.fit(x_train, y_train, epochs=1, verbose=0)

# 4. Securely submit weights for aggregation
# (Handles hashing, signing, Filecoin upload)
cid = trustml.submit_update(model.get_weights())
print(f"Update submitted. CID: {cid}")

# 5. Fetch verified global model (post-FedAvg)
global_weights = trustml.fetch_global_model()
if global_weights:
  model.set_weights(global_weights)
  print("Global model weights applied.")
`}
              </pre>
            </div>
          </div>
        </div>
      </section>

      {/* --- Footer --- */}
      <footer className="mt-28 md:mt-36 text-center text-sm text-slate-500 z-10 pb-8">
        Made for the Filecoin AI Blueprints Hackathon · &copy; {new Date().getFullYear()} TrustML Contributors
      </footer>

    </main>
  );
}

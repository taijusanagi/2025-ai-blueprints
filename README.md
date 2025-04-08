# TrustML
Verifiable Federated Learning with Filecoin

## 🔥 Project Summary

TrustML is a verifiable federated learning platform powered by Filecoin and smart contracts. It enables trustable, decentralized machine learning by allowing multiple nodes to train locally, submit verifiable updates, and collaborate securely to build a global model.

## 🌐 Problem

In federated learning, multiple participants contribute to a shared model without revealing their raw data. However, there's no way to prove that each participant's update is valid, nor to audit the final model’s lineage.

## 💡 Solution

TrustML solves this by combining:

- Federated Averaging (FedAvg) to merge decentralized model updates
- Digital signatures and hashing to verify integrity of each model update
- Merkle Trees to anchor all updates per training round
- Filecoin/IPFS to store model weights and metadata
- Smart contracts to store proof of contributions
- Only verified updates are included in the aggregation, ensuring the global model is tamper-resistant and auditable.

## 🧠 Key Features

- Decentralized Training: Each node trains on local data
- On-chain Verification: Smart contract stores update hashes and Merkle roots
- Storage on Filecoin: All model weights + metadata CIDs stored on Filecoin
- Trustable Aggregation: Only verified weights are included in FedAvg
- Dashboard: Visualizes updates, training rounds, and lineage

## 🎯 Use Case: Federated + Verifiable Training

- Nodes train locally on private datasets
- Nodes hash + sign their model weights
- Nodes upload models to Filecoin/IPFS
- Smart contract stores CID + hash + signature + Merkle root
- Aggregator verifies all updates
- FedAvg is performed on verified models
- Final model is stored and published to Filecoin

## 🧱 Example Metadata (Stored in Filecoin)

```
{
  "round": 2,
  "worker": "0xabc...",
  "model_hash": "0x123...",
  "signature": "0xfed...",
  "accuracy": 0.9231,
  "timestamp": "2025-04-07T12:34:56Z"
}
```

## 🛠 Architecture

- Python SDK for training, hashing, signing, uploading
- Merkle tree aggregator and verifier
- Smart contract (Solidity) for proof registry
- IPFS for data storage
- Frontend dashboard (Next.js)

## 🚀 Tech Stack

- Python (training, aggregation)
- Solidity (TrustML smart contract)
- IPFS + Web3.Storage (Filecoin backend)
- Next.js (dashboard UI)

## 🏆 Prize Fit

This project is built for the "Hack the Data Layer for AI" track:

✅ Data Provenance

✅ Attribution

✅ Efficient AI Collaboration

✅ Modular + Interchain Design

📎 Demo Assets

🎥 Demo video: [link to be added]

🌐 Dashboard: [demo site link]

🧾 Smart Contract: [Explorer / testnet link]

🖼 Architecture Diagram: [Included in submission]

## 🙌 Thank you

This project is made possible by Encode Club & Filecoin ecosystem.
Let's make federated learning trustable, decentralized, and open.


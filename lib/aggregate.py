#!/usr/bin/env python3
"""
Aggregate models submitted to a federated learning task and submit final model
"""

import argparse
import json
import os
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from trustml import FederatedLearningSDK


def main():
    parser = argparse.ArgumentParser(description="Aggregate and evaluate federated models, then submit final model")
    parser.add_argument("--task_id", required=True, help="Task ID to aggregate models from")
    parser.add_argument("--ipfs_api", default="/ip4/127.0.0.1/tcp/5001", help="IPFS API endpoint")
    parser.add_argument("--filecoin_rpc", default="http://localhost:8545", help="Filecoin RPC endpoint")
    parser.add_argument("--contract_address", default="0x5FbDB2315678afecb367f032d93F642f64180aa3", help="Address of the deployed contract (default: local dev address)")
    parser.add_argument("--contract_abi", default="./abi/FederatedTaskManager.json", help="Path to contract ABI JSON file (default: ./abi/FederatedTaskManager.json)")
    parser.add_argument("--output", default=None, help="Output file for aggregated model weights")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")

    args = parser.parse_args()

    # Set random seed
    np.random.seed(args.seed)
    tf.random.set_seed(args.seed)

    if not args.output:
        args.output = f"aggregated_model_{args.task_id}.weights.h5"

    with open(args.contract_abi, 'r') as f:
        contract_abi = json.load(f)

    sdk = FederatedLearningSDK(
        ipfs_api=args.ipfs_api,
        filecoin_rpc=args.filecoin_rpc,
        contract_address=args.contract_address,
        contract_abi=contract_abi
    )

    print(f"🔄 Aggregating models for task ID: {args.task_id}...")
    try:
        aggregated_model_path = sdk.aggregate_models(args.task_id, args.output)
        print(f"✅ Models aggregated and saved to: {aggregated_model_path}")
    except ValueError as e:
        print(f"❌ Error: {e}")
        return

    # Load schema and rebuild model
    schema = sdk.get_task_schema(args.task_id)
    model = sdk.build_model_from_schema(schema)
    model.load_weights(aggregated_model_path)

    # Evaluate on Iris dataset
    print(f"📊 Evaluating model on Iris dataset...")
    iris = load_iris()
    X, y = iris.data, iris.target
    X = StandardScaler().fit_transform(X)

    loss, acc = model.evaluate(X, y, verbose=0)
    print(f"📈 Evaluation completed. Loss: {loss:.4f}, Accuracy: {acc:.4f}")

    predictions = np.argmax(model.predict(X), axis=1)
    from sklearn.metrics import confusion_matrix, classification_report
    print("\nConfusion Matrix:")
    print(confusion_matrix(y, predictions))

    print("\nClassification Report:")
    print(classification_report(y, predictions, target_names=iris.target_names))

    # Submit final model
    print(f"🚀 Submitting final aggregated model to the blockchain...")
    try:
        tx_hash = sdk.submit_final_model(args.task_id, aggregated_model_path)
        print(f"✅ Final model submitted successfully. Tx hash: {tx_hash}")
    except Exception as e:
        print(f"❌ Submission failed: {e}")


if __name__ == "__main__":
    main()

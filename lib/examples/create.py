#!/usr/bin/env python3
"""
Create a federated learning task for iris classification
"""

import argparse
import json
from federated_learning_sdk import FederatedLearningSDK

# Task schema for iris classification
IRIS_SCHEMA = {
    "task": "iris",
    "features": ["sepal_length", "sepal_width", "petal_length", "petal_width"],
    "input_shape": [4],
    "num_classes": 3,
    "model_architecture": [
        {"type": "Dense", "units": 10, "activation": "relu"},
        {"type": "Dense", "units": 3, "activation": "softmax"}
    ]
}

def main():
    parser = argparse.ArgumentParser(description="Create a federated learning task for Iris classification")
    parser.add_argument("--ipfs_api", default="/ip4/127.0.0.1/tcp/5001", help="IPFS API endpoint")
    parser.add_argument("--filecoin_rpc", default="http://localhost:8545", help="Filecoin RPC endpoint")
    parser.add_argument("--contract_address", required=True, help="Address of the deployed contract")
    parser.add_argument("--contract_abi", required=True, help="Path to contract ABI JSON file")
    parser.add_argument("--task_id", default=None, help="Custom task ID (optional)")
    parser.add_argument("--output", default="task_info.json", help="Output file to save task information")
    
    args = parser.parse_args()
    
    # Load contract ABI
    with open(args.contract_abi, 'r') as f:
        contract_abi = json.load(f)
    
    # Initialize SDK
    sdk = FederatedLearningSDK(
        ipfs_api=args.ipfs_api,
        filecoin_rpc=args.filecoin_rpc,
        contract_address=args.contract_address,
        contract_abi=contract_abi
    )
    
    # Create task with Iris schema
    print("Creating federated learning task for Iris classification...")
    task_info = sdk.create_task(IRIS_SCHEMA, task_id=args.task_id)
    
    # Save task information to file
    with open(args.output, 'w') as f:
        json.dump(task_info, f, indent=2)
    
    print(f"Task created successfully!")
    print(f"Task ID: {task_info['task_id']}")
    print(f"Schema IPFS Hash: {task_info['schema_hash']}")
    print(f"Transaction Hash: {task_info['tx_hash']}")
    print(f"Task information saved to {args.output}")

if __name__ == "__main__":
    main()

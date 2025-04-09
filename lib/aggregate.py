#!/usr/bin/env python3
"""
Aggregate models submitted to a federated learning task
"""

import argparse
import json
import os
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from sdk import FederatedLearningSDK

def main():
    parser = argparse.ArgumentParser(description="Aggregate models submitted to a federated learning task")
    parser.add_argument("--task_id", required=True, help="Task ID to aggregate models from")
    parser.add_argument("--ipfs_api", default="/ip4/127.0.0.1/tcp/5001", help="IPFS API endpoint")
    parser.add_argument("--filecoin_rpc", default="http://localhost:8545", help="Filecoin RPC endpoint")
    parser.add_argument("--contract_address", required=True, help="Address of the deployed contract")
    parser.add_argument("--contract_abi", required=True, help="Path to contract ABI JSON file")
    parser.add_argument("--output", default=None, help="Output file for aggregated model weights")
    parser.add_argument("--evaluate", action="store_true", help="Evaluate the aggregated model")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    
    args = parser.parse_args()
    
    # Set random seed for reproducibility
    np.random.seed(args.seed)
    tf.random.set_seed(args.seed)
    
    # Set output filename if not provided
    if not args.output:
        args.output = f"aggregated_model_{args.task_id}.weights.h5"
    
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
    
    print(f"Aggregating models for task ID: {args.task_id}")
    
    # Perform federated averaging and save the result
    try:
        aggregated_model_path = sdk.aggregate_models(args.task_id, args.output)
        print(f"Models aggregated successfully!")
        print(f"Aggregated model saved to: {aggregated_model_path}")
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    # Evaluate aggregated model if requested
    if args.evaluate:
        # Get task schema to build the model
        schema = sdk.get_task_schema(args.task_id)
        
        # Build model from schema
        model = sdk.build_model_from_schema(schema)
        model.load_weights(aggregated_model_path)
        
        # Load Iris dataset for evaluation
        print("Evaluating aggregated model on Iris dataset...")
        iris = load_iris()
        X = iris.data
        y = iris.target
        
        # Standardize features
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
        
        # Evaluate model
        loss, accuracy = model.evaluate(X, y, verbose=0)
        print(f"Aggregated model performance:")
        print(f"Loss: {loss:.4f}")
        print(f"Accuracy: {accuracy:.4f}")
        
        # Additional evaluation: confusion matrix
        predictions = np.argmax(model.predict(X), axis=1)
        from sklearn.metrics import classification_report, confusion_matrix
        
        print("\nConfusion Matrix:")
        print(confusion_matrix(y, predictions))
        
        print("\nClassification Report:")
        print(classification_report(y, predictions, target_names=iris.target_names))

if __name__ == "__main__":
    main()

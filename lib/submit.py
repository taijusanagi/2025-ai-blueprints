#!/usr/bin/env python3
"""
Train a model on local Iris data and submit to a federated learning task
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
    parser = argparse.ArgumentParser(description="Train a model on Iris data and submit to a federated learning task")
    parser.add_argument("--task_id", required=True, help="Task ID to submit the model to")
    parser.add_argument("--ipfs_api", default="/ip4/127.0.0.1/tcp/5001", help="IPFS API endpoint")
    parser.add_argument("--filecoin_rpc", default="http://localhost:8545", help="Filecoin RPC endpoint")
    parser.add_argument("--contract_address", required=True, help="Address of the deployed contract")
    parser.add_argument("--contract_abi", required=True, help="Path to contract ABI JSON file")
    parser.add_argument("--test_split", type=float, default=0.2, help="Test split ratio (default: 0.2)")
    parser.add_argument("--epochs", type=int, default=50, help="Training epochs (default: 50)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    
    args = parser.parse_args()
    
    # Set random seed for reproducibility
    np.random.seed(args.seed)
    tf.random.set_seed(args.seed)
    
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
    
    # Get task schema
    print(f"Getting schema for task ID: {args.task_id}")
    schema = sdk.get_task_schema(args.task_id)
    print(f"Task: {schema['task']}")
    
    # Load Iris dataset
    print("Loading Iris dataset...")
    iris = load_iris()
    X = iris.data
    y = iris.target
    
    # Split data (simulate having only part of the dataset)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_split, random_state=args.seed
    )
    
    # Standardize features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    # Build model from schema using SDK's helper method
    print("Building model according to task schema...")
    model = sdk.build_model_from_schema(schema)
    
    # Print model summary
    model.build((None, schema["input_shape"][0]))
    model.summary()
    
    # Train model on local data
    print(f"Training model for {args.epochs} epochs...")
    history = model.fit(
        X_train, y_train,
        epochs=args.epochs,
        batch_size=32,
        validation_data=(X_test, y_test),
        verbose=1
    )
    
    # Evaluate model
    test_loss, test_acc = model.evaluate(X_test, y_test)
    print(f"Test accuracy: {test_acc:.4f}")
    
    # Save model weights
    weights_file = f"model_weights_{args.task_id}.weights.h5"
    model.save_weights(weights_file)
    print(f"Model weights saved to {weights_file}")
    
    # Submit trained model to the task
    print("Submitting trained model to the blockchain...")
    tx_hash = sdk.submit_model(args.task_id, weights_file)
    
    print(f"Model submitted successfully!")
    print(f"Transaction hash: {tx_hash}")

if __name__ == "__main__":
    main()

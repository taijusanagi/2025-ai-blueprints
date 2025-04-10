#!/usr/bin/env python3
"""
Train a model on a selected sklearn dataset and submit to a federated learning task
"""

import argparse
import json
import os
from datetime import datetime
import numpy as np
from sklearn.datasets import load_iris, load_wine, load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from trustml import FederatedLearningSDK

def get_dataset(dataset_name):
    """
    Load a dataset by name.
    
    Args:
        dataset_name (str): Name of the dataset to load ('iris', 'wine', or 'breast_cancer')
        
    Returns:
        tuple: (X, y, target_names) where X is the feature data, y is the target data,
               and target_names are the class labels
    """
    if dataset_name.lower() == 'iris':
        data = load_iris()
    elif dataset_name.lower() == 'wine':
        data = load_wine()
    elif dataset_name.lower() == 'breast_cancer':
        data = load_breast_cancer()
    else:
        raise ValueError(f"Dataset '{dataset_name}' not supported. Choose from: iris, wine, breast_cancer")
        
    return data.data, data.target, data.target_names

def main():
    parser = argparse.ArgumentParser(description="Train a model on selected dataset and submit to a federated learning task")
    parser.add_argument("--task_id", required=True, help="Task ID to submit the model to")
    parser.add_argument("--dataset", default="iris", choices=["iris", "wine", "breast_cancer"], 
                        help="Dataset to use (default: iris)")
    parser.add_argument("--provider", default="akave", help="Storage provider")
    parser.add_argument("--ipfs_api", default="/ip4/127.0.0.1/tcp/5001", help="IPFS API endpoint")
    parser.add_argument("--akave_api_url", default="http://localhost:8000", help="Akave API URL")
    parser.add_argument("--bucket_id", default="myBucket", help="Bucket ID for Akave")
    parser.add_argument("--filecoin_rpc", default="http://localhost:8545", help="Filecoin RPC endpoint")
    parser.add_argument("--contract_address", default="0x5FbDB2315678afecb367f032d93F642f64180aa3", 
                        help="Address of the deployed contract (default: local dev address)")
    parser.add_argument("--contract_abi", default="./abi/FederatedTaskManager.json", 
                        help="Path to contract ABI JSON file (default: ./abi/FederatedTaskManager.json)")
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
        provider=args.provider,
        ipfs_api=args.ipfs_api,
        bucket_id=args.bucket_id,
        akave_api_url=args.akave_api_url,
        filecoin_rpc=args.filecoin_rpc,
        contract_address=args.contract_address,
        contract_abi=contract_abi
    )
    
    # Get task schema
    print(f"Getting schema for task ID: {args.task_id}")
    schema = sdk.get_task_schema(args.task_id)
    print(f"Task: {schema['task']}")
    
    # Load selected dataset
    print(f"Loading {args.dataset} dataset...")
    X, y, target_names = get_dataset(args.dataset)
    print(f"Dataset shape: X={X.shape}, y={y.shape}, classes={len(target_names)}")
    
    # Verify that the model architecture is compatible with the dataset
    input_dim = X.shape[1]
    if input_dim != schema["input_shape"][0]:
        print(f"Warning: Dataset has {input_dim} features but model expects {schema['input_shape'][0]}.")
        print("Checking if we can adjust the model input layer...")
        
        # If using the first Dense layer, we might be able to adjust it
        if schema["model_architecture"][0]["type"] == "Dense":
            print(f"Adjusting input shape to match dataset: {input_dim}")
            schema["input_shape"][0] = input_dim
        else:
            raise ValueError(f"Model architecture is not compatible with selected dataset. Expected {schema['input_shape'][0]} features, got {input_dim}.")
    
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
    os.makedirs("models", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    weights_file = f"models/{args.task_id}_{args.dataset}_{timestamp}_submitted.weights.h5"
    model.save_weights(weights_file)
    print(f"Model weights saved to {weights_file}")
    
    # Submit trained model to the task
    print("Submitting trained model to the blockchain...")
    tx_hash = sdk.submit_model(args.task_id, weights_file, test_acc)
    
    print(f"Model submitted successfully!")
    print(f"Transaction hash: {tx_hash}")

if __name__ == "__main__":
    main()
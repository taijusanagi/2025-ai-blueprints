#!/usr/bin/env python3
"""
Aggregate models submitted to a federated learning task and submit final model
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
from sklearn.metrics import confusion_matrix, classification_report


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
    parser = argparse.ArgumentParser(description="Aggregate and evaluate federated models, then submit final model")
    parser.add_argument("--task_id", required=True, help="Task ID to aggregate models from")
    parser.add_argument("--dataset", default="iris", choices=["iris", "wine", "breast_cancer"], 
                        help="Dataset to use for evaluation (default: iris)")
    parser.add_argument("--ipfs_api", default="/ip4/127.0.0.1/tcp/5001", help="IPFS API endpoint")
    parser.add_argument("--filecoin_rpc", default="http://localhost:8545", help="Filecoin RPC endpoint")
    parser.add_argument("--contract_address", default="0x5FbDB2315678afecb367f032d93F642f64180aa3", 
                        help="Address of the deployed contract (default: local dev address)")
    parser.add_argument("--contract_abi", default="./abi/FederatedTaskManager.json", 
                        help="Path to contract ABI JSON file (default: ./abi/FederatedTaskManager.json)")
    parser.add_argument("--output", default=None, help="Output file for aggregated model weights")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")

    args = parser.parse_args()

    # Set random seed
    np.random.seed(args.seed)
    tf.random.set_seed(args.seed)

    if not args.output:
        args.output = f"aggregated_model_{args.task_id}_{args.dataset}.weights.h5"

    with open(args.contract_abi, 'r') as f:
        contract_abi = json.load(f)

    sdk = FederatedLearningSDK(
        provider="akave",

        # ipfs_api=args.ipfs_api,
        filecoin_rpc=args.filecoin_rpc,
        contract_address=args.contract_address,
        contract_abi=contract_abi
    )

    print(f"🔄 Aggregating models for task ID: {args.task_id}...")
    try:
        os.makedirs("models", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        aggregated_model_path = sdk.aggregate_models(
            args.task_id, 
            f"models/{args.task_id}_{args.dataset}_{timestamp}_aggregated.weights.h5"
        )
        print(f"✅ Models aggregated and saved to: {aggregated_model_path}")
    except ValueError as e:
        print(f"❌ Error: {e}")
        return

    # Load schema and rebuild model
    schema = sdk.get_task_schema(args.task_id)
    model = sdk.build_model_from_schema(schema)
    model.load_weights(aggregated_model_path)

    # Load selected dataset for evaluation
    print(f"📊 Evaluating model on {args.dataset} dataset...")
    X, y, target_names = get_dataset(args.dataset)
    
    # Check if model input shape matches dataset features
    input_dim = X.shape[1]
    if input_dim != schema["input_shape"][0]:
        print(f"Warning: Dataset has {input_dim} features but model was trained with {schema['input_shape'][0]}.")
        if schema["model_architecture"][0]["type"] == "Dense":
            print("Adjusting model for evaluation...")
            # Create a new model with the correct input shape
            adjusted_schema = schema.copy()
            adjusted_schema["input_shape"][0] = input_dim
            model = sdk.build_model_from_schema(adjusted_schema)
            # We can't use the weights properly in this case
            print("⚠️ Model architecture doesn't match dataset features. Evaluation may be inaccurate.")
        else:
            print("❌ Cannot evaluate model - architecture incompatible with dataset.")
            return
    
    # Standardize features
    X = StandardScaler().fit_transform(X)

    # Evaluate model
    loss, acc = model.evaluate(X, y, verbose=0)
    print(f"📈 Evaluation completed. Loss: {loss:.4f}, Accuracy: {acc:.4f}")

    # Generate predictions and evaluation metrics
    predictions = np.argmax(model.predict(X), axis=1)
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y, predictions))

    print("\nClassification Report:")
    print(classification_report(y, predictions, target_names=target_names))

    # Submit final model
    print(f"🚀 Submitting final aggregated model to the blockchain...")
    try:
        tx_hash = sdk.submit_final_model(args.task_id, aggregated_model_path, acc)
        print(f"✅ Final model submitted successfully. Tx hash: {tx_hash}")
    except Exception as e:
        print(f"❌ Submission failed: {e}")


if __name__ == "__main__":
    main()
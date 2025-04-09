#!/usr/bin/env python3
"""
Create a federated learning task for various sklearn datasets
"""
import sys
import os
import argparse
import json
from sklearn.datasets import load_iris, load_wine, load_breast_cancer
from trustml import FederatedLearningSDK

def get_dataset_info(dataset_name):
    """
    Get dataset information including feature names, input shape, and number of classes.
    
    Args:
        dataset_name (str): Name of the dataset ('iris', 'wine', or 'breast_cancer')
        
    Returns:
        dict: Dataset metadata including features, shape, and classes
    """
    if dataset_name.lower() == 'iris':
        data = load_iris()
        return {
            "name": "iris",
            "features": data.feature_names,
            "input_shape": [data.data.shape[1]],
            "num_classes": len(data.target_names)
        }
    elif dataset_name.lower() == 'wine':
        data = load_wine()
        return {
            "name": "wine",
            "features": data.feature_names,
            "input_shape": [data.data.shape[1]],
            "num_classes": len(data.target_names)
        }
    elif dataset_name.lower() == 'breast_cancer':
        data = load_breast_cancer()
        return {
            "name": "breast_cancer",
            "features": data.feature_names,
            "input_shape": [data.data.shape[1]],
            "num_classes": len(data.target_names)
        }
    else:
        raise ValueError(f"Dataset '{dataset_name}' not supported. Choose from: iris, wine, breast_cancer")

def create_model_architecture(dataset_info, model_complexity="simple"):
    """
    Create an appropriate model architecture based on dataset characteristics.
    
    Args:
        dataset_info (dict): Dataset metadata from get_dataset_info()
        model_complexity (str): 'simple', 'medium', or 'complex'
        
    Returns:
        list: Model architecture layers as dictionaries
    """
    input_dim = dataset_info["input_shape"][0]
    num_classes = dataset_info["num_classes"]
    
    # Simple architecture
    if model_complexity == "simple":
        return [
            {"type": "Dense", "units": 10, "activation": "relu"},
            {"type": "Dense", "units": num_classes, "activation": "softmax"}
        ]
    # Medium complexity
    elif model_complexity == "medium":
        return [
            {"type": "Dense", "units": 32, "activation": "relu"},
            {"type": "Dropout", "rate": 0.2},
            {"type": "Dense", "units": 16, "activation": "relu"},
            {"type": "Dense", "units": num_classes, "activation": "softmax"}
        ]
    # Complex architecture
    elif model_complexity == "complex":
        return [
            {"type": "Dense", "units": 64, "activation": "relu"},
            {"type": "Dropout", "rate": 0.3},
            {"type": "Dense", "units": 32, "activation": "relu"},
            {"type": "Dropout", "rate": 0.2},
            {"type": "Dense", "units": 16, "activation": "relu"},
            {"type": "Dense", "units": num_classes, "activation": "softmax"}
        ]
    else:
        raise ValueError(f"Unknown model complexity: {model_complexity}")

def main():
    parser = argparse.ArgumentParser(description="Create a federated learning task for a selected dataset")
    parser.add_argument("--dataset", default="iris", choices=["iris", "wine", "breast_cancer"], 
                       help="Dataset to use (default: iris)")
    parser.add_argument("--model_complexity", default="simple", choices=["simple", "medium", "complex"],
                       help="Model architecture complexity (default: simple)")
    parser.add_argument("--ipfs_api", default="/ip4/127.0.0.1/tcp/5001", help="IPFS API endpoint")
    parser.add_argument("--filecoin_rpc", default="http://localhost:8545", help="Filecoin RPC endpoint")
    parser.add_argument("--contract_address", default="0x5FbDB2315678afecb367f032d93F642f64180aa3", 
                       help="Address of the deployed contract (default: local dev address)")
    parser.add_argument("--contract_abi", default="./abi/FederatedTaskManager.json", 
                       help="Path to contract ABI JSON file (default: ./abi/FederatedTaskManager.json)")
    parser.add_argument("--task_id", default=None, help="Custom task ID (optional)")
    parser.add_argument("--output", default=None, 
                       help="Output file to save task information (default: task_info_{dataset}_{complexity}.json)")
    
    args = parser.parse_args()
    
    # Set default output filename if not provided
    if not args.output:
        args.output = f"task_info_{args.dataset}_{args.model_complexity}.json"
    
    # Load contract ABI
    try:
        with open(args.contract_abi, 'r') as f:
            contract_abi = json.load(f)
    except FileNotFoundError:
        print(f"Error: Contract ABI file '{args.contract_abi}' not found.")
        return 1
    except json.JSONDecodeError:
        print(f"Error: Contract ABI file '{args.contract_abi}' is not valid JSON.")
        return 1
    
    # Initialize SDK
    sdk = FederatedLearningSDK(
        ipfs_api=args.ipfs_api,
        filecoin_rpc=args.filecoin_rpc,
        contract_address=args.contract_address,
        contract_abi=contract_abi
    )
    
    try:
        # Get dataset information
        dataset_info = get_dataset_info(args.dataset)
        print(f"Dataset: {args.dataset}")
        print(f"Features: {len(dataset_info['features'])}")
        print(f"Number of classes: {dataset_info['num_classes']}")
        
        # Create model architecture based on dataset and complexity
        model_architecture = create_model_architecture(dataset_info, args.model_complexity)
        
        # Create task schema
        schema = {
            "task": f"{args.dataset}_classification",
            "features": dataset_info["features"],
            "input_shape": dataset_info["input_shape"],
            "num_classes": dataset_info["num_classes"],
            "model_architecture": model_architecture
        }
        
        # Print schema information
        print("\nTask Schema:")
        print(f"Task: {schema['task']}")
        print(f"Input Shape: {schema['input_shape']}")
        print(f"Number of Classes: {schema['num_classes']}")
        print(f"Model Architecture: {len(schema['model_architecture'])} layers")
        
        # Create task
        print(f"\nCreating federated learning task for {args.dataset} classification...")
        task_info = sdk.create_task(schema, task_id=args.task_id)
        
        # Save task information to file
        with open(args.output, 'w') as f:
            json.dump(task_info, f, indent=2)
        
        print(f"\nTask created successfully!")
        print(f"Task ID: {task_info['task_id']}")
        print(f"Schema IPFS Hash: {task_info['schema_hash']}")
        print(f"Transaction Hash: {task_info['tx_hash']}")
        print(f"Task information saved to {args.output}")
        
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

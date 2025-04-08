"""
Aggregator for Federated Learning tasks.

This module provides functionality to:
1. Create tasks with schema
2. Aggregate training data from nodes
3. Use the SDK to federate average weights
"""

import json
import time
import os
import numpy as np
import tensorflow as tf
from sdk import FederatedLearningSDK


class FederatedLearningAggregator:
    """Aggregator for Federated Learning tasks."""
    
    def __init__(self, sdk=None, ipfs_api="/ip4/127.0.0.1/tcp/5001", filecoin_rpc="http://localhost:8545",
                 contract_address=None, contract_abi=None):
        """
        Initialize the Aggregator with SDK or connection parameters.
        
        Args:
            sdk (FederatedLearningSDK): Existing SDK instance
            ipfs_api (str): IPFS API endpoint
            filecoin_rpc (str): Filecoin RPC endpoint
            contract_address (str): Address of the deployed smart contract
            contract_abi (dict): ABI of the deployed smart contract
        """
        if sdk:
            self.sdk = sdk
        else:
            self.sdk = FederatedLearningSDK(
                ipfs_api=ipfs_api,
                filecoin_rpc=filecoin_rpc,
                contract_address=contract_address,
                contract_abi=contract_abi
            )
        
        self.tasks = {}
        self.node_results = {}
        self.aggregated_models = {}
    
    def create_task(self, task_schema, reward=0):
        """
        Create a new federated learning task.
        
        Args:
            task_schema (dict): The task schema
            reward (int): Reward amount for completing the task
            
        Returns:
            dict: Task information including task_id, schema_hash, and tx_hash
        """
        # Validate schema
        self._validate_schema(task_schema)
        
        # Create and upload task
        task_info = self.sdk.create_and_upload_task(task_schema, reward)
        
        # Store task locally
        self.tasks[task_info['task_id']] = {
            'schema': task_schema,
            'schema_hash': task_info['schema_hash'],
            'tx_hash': task_info['tx_hash'],
            'status': 'created',
            'nodes': [],
            'results': []
        }
        
        print(f"Task created with ID: {task_info['task_id']}")
        
        return task_info
    
    def _validate_schema(self, schema):
        """
        Validate a task schema.
        
        Args:
            schema (dict): The task schema
            
        Raises:
            ValueError: If schema is invalid
        """
        required_fields = ['task', 'features', 'input_shape', 'num_classes', 'model_architecture']
        
        for field in required_fields:
            if field not in schema:
                raise ValueError(f"Schema missing required field: {field}")
        
        if not isinstance(schema['model_architecture'], list) or len(schema['model_architecture']) == 0:
            raise ValueError("Schema must contain a non-empty model_architecture list")
        
        for layer in schema['model_architecture']:
            if 'type' not in layer:
                raise ValueError("Each layer in model_architecture must have a 'type'")
    
    def register_node(self, task_id, node_id):
        """
        Register a node for a task.
        
        Args:
            task_id (str): Task ID
            node_id (str): Node ID
            
        Returns:
            bool: Success status
        """
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        if node_id not in self.tasks[task_id]['nodes']:
            self.tasks[task_id]['nodes'].append(node_id)
            print(f"Node {node_id} registered for task {task_id}")
        
        return True
    
    def receive_node_result(self, task_id, node_id, weights_file=None, weights_hash=None, metrics=None):
        """
        Receive training result from a node.
        
        Args:
            task_id (str): Task ID
            node_id (str): Node ID
            weights_file (str): Path to weights file
            weights_hash (str): IPFS hash of weights
            metrics (dict): Training metrics
            
        Returns:
            bool: Success status
        """
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        if node_id not in self.tasks[task_id]['nodes']:
            self.register_node(task_id, node_id)
        
        # Initialize node results for this task if not exists
        if task_id not in self.node_results:
            self.node_results[task_id] = {}
        
        # Store result
        self.node_results[task_id][node_id] = {
            'weights_file': weights_file,
            'weights_hash': weights_hash,
            'metrics': metrics,
            'timestamp': time.time()
        }
        
        # Add to task results
        self.tasks[task_id]['results'].append({
            'node_id': node_id,
            'weights_hash': weights_hash,
            'metrics': metrics,
            'timestamp': time.time()
        })
        
        print(f"Received result from node {node_id} for task {task_id}")
        
        return True
    
    def aggregate_results(self, task_id, min_nodes=1, download_if_needed=True):
        """
        Aggregate results from nodes for a task.
        
        Args:
            task_id (str): Task ID
            min_nodes (int): Minimum number of nodes required
            download_if_needed (bool): Whether to download weights from IPFS if needed
            
        Returns:
            dict: Aggregation result
        """
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        if task_id not in self.node_results or len(self.node_results[task_id]) < min_nodes:
            raise ValueError(f"Not enough node results for task {task_id}")
        
        # Get task schema
        schema = self.tasks[task_id]['schema']
        
        # Build model from schema
        model = self.sdk.build_model_from_schema(schema)
        
        # Collect weights from nodes
        weight_files = []
        for node_id, result in self.node_results[task_id].items():
            if result['weights_file']:
                weight_files.append(result['weights_file'])
            elif result['weights_hash'] and download_if_needed:
                # Download from IPFS
                downloaded_file = self.sdk.download_model_weights_from_ipfs(
                    result['weights_hash'],
                    f"node_{node_id}_weights.h5"
                )
                weight_files.append(downloaded_file)
        
        if len(weight_files) < min_nodes:
            raise ValueError(f"Not enough weight files available for task {task_id}")
        
        # Load weights
        weight_list = []
        for file in weight_files:
            model = self.sdk.load_model_weights(model, file)
            weight_list.append([w.numpy() for w in model.weights])
        
        # Perform federated averaging
        federated_weights = self.sdk.federated_average(weight_list)
        
        # Apply federated weights to model
        model = self.sdk.apply_federated_weights(model, federated_weights)
        
        # Save aggregated model
        aggregated_file = f"aggregated_model_{task_id}.h5"
        model.save_weights(aggregated_file)
        
        # Upload to IPFS
        aggregated_hash = self.sdk.upload_model_weights_to_ipfs(aggregated_file)
        
        # Store aggregation result
        self.aggregated_models[task_id] = {
            'weights_file': aggregated_file,
            'weights_hash': aggregated_hash,
            'num_nodes': len(weight_files),
            'timestamp': time.time()
        }
        
        # Update task status
        self.tasks[task_id]['status'] = 'aggregated'
        
        print(f"Aggregated results from {len(weight_files)} nodes for task {task_id}")
        
        return {
            'task_id': task_id,
            'weights_file': aggregated_file,
            'weights_hash': aggregated_hash,
            'num_nodes': len(weight_files)
        }
    
    def get_task_status(self, task_id):
        """
        Get status of a task.
        
        Args:
            task_id (str): Task ID
            
        Returns:
            dict: Task status
        """
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        task = self.tasks[task_id]
        
        return {
            'task_id': task_id,
            'status': task['status'],
            'num_nodes': len(task['nodes']),
            'num_results': len(task['results']),
            'aggregated': task_id in self.aggregated_models
        }
    
    def get_all_tasks(self):
        """
        Get all tasks.
        
        Returns:
            dict: All tasks
        """
        return {task_id: self.get_task_status(task_id) for task_id in self.tasks}
    
    def evaluate_aggregated_model(self, task_id, x_test, y_test):
        """
        Evaluate an aggregated model on test data.
        
        Args:
            task_id (str): Task ID
            x_test (numpy.ndarray): Test features
            y_test (numpy.ndarray): Test labels
            
        Returns:
            dict: Evaluation metrics
        """
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        if task_id not in self.aggregated_models:
            raise ValueError(f"No aggregated model for task {task_id}")
        
        # Get task schema
        schema = self.tasks[task_id]['schema']
        
        # Build model from schema
        model = self.sdk.build_model_from_schema(schema)
        
        # Load aggregated weights
        model = self.sdk.load_model_weights(model, self.aggregated_models[task_id]['weights_file'])
        
        # Evaluate model
        evaluation = model.evaluate(x_test, y_test)
        
        metrics = {}
        for i, metric_name in enumerate(model.metrics_names):
            metrics[metric_name] = float(evaluation[i])
        
        return metrics

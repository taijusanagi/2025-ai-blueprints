"""
Node for Federated Learning tasks.

This module provides functionality to:
1. Fetch tasks from Filecoin smart contracts
2. Use local data for machine learning
3. Train models based on task schema
4. Submit results back to the network
"""

import json
import os
import time
import numpy as np
import tensorflow as tf
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sdk import FederatedLearningSDK


class FederatedLearningNode:
    """Node for Federated Learning tasks."""
    
    def __init__(self, node_id=None, sdk=None, ipfs_api="/ip4/127.0.0.1/tcp/5001", filecoin_rpc="http://localhost:8545",
                 contract_address=None, contract_abi=None):
        """
        Initialize the Node with SDK or connection parameters.
        
        Args:
            node_id (str): Unique identifier for this node
            sdk (FederatedLearningSDK): Existing SDK instance
            ipfs_api (str): IPFS API endpoint
            filecoin_rpc (str): Filecoin RPC endpoint
            contract_address (str): Address of the deployed smart contract
            contract_abi (dict): ABI of the deployed smart contract
        """
        # Generate a node ID if not provided
        self.node_id = node_id or f"node_{int(time.time())}"
        
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
        self.models = {}
        self.training_results = {}
    
    def fetch_task(self, task_id=None, schema_hash=None):
        """
        Fetch a task from the network.
        
        Args:
            task_id (str): Task ID
            schema_hash (str): IPFS hash of the task schema
            
        Returns:
            dict: Task schema
        """
        if not schema_hash and not task_id:
            raise ValueError("Either task_id or schema_hash must be provided")
        
        # If we have task_id but not schema_hash, get it from the contract
        if task_id and not schema_hash:
            if not self.sdk.contract:
                raise ConnectionError("Smart contract not initialized")
            
            # Get schema hash from contract
            schema_hash = self.sdk.contract.functions.getTaskSchema(task_id).call()
        
        # Get schema from IPFS
        schema = self.sdk.get_task_schema(schema_hash)
        
        # Store task locally
        if task_id:
            self.tasks[task_id] = {
                'schema': schema,
                'schema_hash': schema_hash,
                'status': 'fetched',
                'timestamp': time.time()
            }
        else:
            # Generate a local task ID if not provided
            task_id = f"local_task_{int(time.time())}"
            self.tasks[task_id] = {
                'schema': schema,
                'schema_hash': schema_hash,
                'status': 'fetched',
                'timestamp': time.time()
            }
        
        print(f"Fetched task {task_id} with schema hash {schema_hash}")
        
        return schema
    
    def load_iris_dataset(self):
        """
        Load the Iris dataset for testing.
        
        Returns:
            tuple: (x_train, y_train, x_test, y_test)
        """
        # Load Iris dataset
        iris = datasets.load_iris()
        X = iris.data
        y = iris.target
        
        # Split into train and test sets
        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Standardize features
        scaler = StandardScaler()
        x_train = scaler.fit_transform(x_train)
        x_test = scaler.transform(x_test)
        
        return x_train, y_train, x_test, y_test
    
    def load_dataset(self, task_name, features=None):
        """
        Load a dataset based on task name.
        
        Args:
            task_name (str): Name of the task/dataset
            features (list): List of feature names
            
        Returns:
            tuple: (x_train, y_train, x_test, y_test)
        """
        if task_name.lower() == 'iris':
            return self.load_iris_dataset()
        else:
            raise ValueError(f"Dataset {task_name} not supported")
    
    def train_model(self, task_id, x_train=None, y_train=None, epochs=10, batch_size=32, validation_split=0.2):
        """
        Train a model for a task.
        
        Args:
            task_id (str): Task ID
            x_train (numpy.ndarray): Training features
            y_train (numpy.ndarray): Training labels
            epochs (int): Number of training epochs
            batch_size (int): Batch size
            validation_split (float): Validation split
            
        Returns:
            dict: Training history and metrics
        """
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        # Get task schema
        schema = self.tasks[task_id]['schema']
        
        # Load dataset if not provided
        if x_train is None or y_train is None:
            task_name = schema.get('task', '')
            features = schema.get('features', [])
            x_train, y_train, x_test, y_test = self.load_dataset(task_name, features)
        
        # Build model from schema
        model = self.sdk.build_model_from_schema(schema)
        
        # Train model
        history = model.fit(
            x_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            verbose=1
        )
        
        # Evaluate model
        evaluation = model.evaluate(x_test, y_test)
        
        metrics = {}
        for i, metric_name in enumerate(model.metrics_names):
            metrics[metric_name] = float(evaluation[i])
        
        # Save model
        weights_file = f"model_weights_{task_id}_{self.node_id}.h5"
        model.save_weights(weights_file)
        
        # Store model and results
        self.models[task_id] = model
        self.training_results[task_id] = {
            'history': history.history,
            'metrics': metrics,
            'weights_file': weights_file,
            'timestamp': time.time()
        }
        
        # Update task status
        self.tasks[task_id]['status'] = 'trained'
        
        print(f"Trained model for task {task_id}")
        
        return {
            'history': history.history,
            'metrics': metrics,
            'weights_file': weights_file
        }
    
    def submit_results(self, task_id, aggregator_endpoint=None):
        """
        Submit training results to the network.
        
        Args:
            task_id (str): Task ID
            aggregator_endpoint (str): Endpoint of the aggregator
            
        Returns:
            dict: Submission result
        """
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        if task_id not in self.training_results:
            raise ValueError(f"No training results for task {task_id}")
        
        # Get training results
        results = self.training_results[task_id]
        
        # Upload weights to IPFS
        weights_hash = self.sdk.upload_model_weights_to_ipfs(results['weights_file'])
        
        # If aggregator endpoint is provided, submit directly
        if aggregator_endpoint:
            import requests
            
            response = requests.post(
                f"{aggregator_endpoint}/submit_result",
                json={
                    'task_id': task_id,
                    'node_id': self.node_id,
                    'weights_hash': weights_hash,
                    'metrics': results['metrics']
                }
            )
            
            if response.status_code == 200:
                print(f"Results submitted to aggregator for task {task_id}")
                submission_result = response.json()
            else:
                print(f"Failed to submit results to aggregator: {response.text}")
                submission_result = {'success': False, 'error': response.text}
        else:
            # Otherwise, just return the hash for manual submission
            submission_result = {
                'task_id': task_id,
                'node_id': self.node_id,
                'weights_hash': weights_hash,
                'metrics': results['metrics']
            }
            print(f"Results ready for submission for task {task_id}")
        
        # Update task status
        self.tasks[task_id]['status'] = 'submitted'
        self.tasks[task_id]['weights_hash'] = weights_hash
        
        return submission_result
    
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
        
        status = {
            'task_id': task_id,
            'status': task['status'],
            'schema_hash': task['schema_hash'],
            'timestamp': task['timestamp']
        }
        
        if task_id in self.training_results:
            status['metrics'] = self.training_results[task_id]['metrics']
            status['weights_file'] = self.training_results[task_id]['weights_file']
        
        if 'weights_hash' in task:
            status['weights_hash'] = task['weights_hash']
        
        return status
    
    def get_all_tasks(self):
        """
        Get all tasks.
        
        Returns:
            dict: All tasks
        """
        return {task_id: self.get_task_status(task_id) for task_id in self.tasks}
    
    def process_task(self, task_id=None, schema_hash=None, epochs=10, batch_size=32, submit=True, aggregator_endpoint=None):
        """
        Process a task end-to-end: fetch, train, and submit.
        
        Args:
            task_id (str): Task ID
            schema_hash (str): IPFS hash of the task schema
            epochs (int): Number of training epochs
            batch_size (int): Batch size
            submit (bool): Whether to submit results
            aggregator_endpoint (str): Endpoint of the aggregator
            
        Returns:
            dict: Processing result
        """
        # Fetch task
        schema = self.fetch_task(task_id, schema_hash)
        
        # If task_id was not provided, get it from the tasks dict
        if not task_id:
            for tid, task in self.tasks.items():
                if task['schema_hash'] == schema_hash:
                    task_id = tid
                    break
        
        # Train model
        training_result = self.train_model(task_id, epochs=epochs, batch_size=batch_size)
        
        # Submit results if requested
        if submit:
            submission_result = self.submit_results(task_id, aggregator_endpoint)
            return {
                'task_id': task_id,
                'training': training_result,
                'submission': submission_result
            }
        else:
            return {
                'task_id': task_id,
                'training': training_result
            }

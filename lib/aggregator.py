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
    
    def create_task(self, task_schema, reward=0):
        """
        Create a new federated learning task.
        
        Args:
            task_schema (dict): The task schema
            reward (int): Reward amount for completing the task
            
        Returns:
            dict: Task information including task_id, schema_hash, and tx_hash
        """
        
        # Create and upload task
        task_info = self.sdk.create_and_upload_task(task_schema, reward)        
        print(f"Task created with ID: {task_info['task_id']}")
        
        return task_info

    def aggregate_task_submissions(self, task_id):
        """
        Aggregate model submissions for a task using federated averaging.

        Args:
            task_id (str): ID of the task to aggregate

        Returns:
            str: IPFS hash of the aggregated model weights
        """
        print(f"Fetching model submissions for task {task_id}...")
        model_hashes = self.sdk.get_submissions(task_id)

        if not model_hashes:
            raise ValueError(f"No model submissions found for task {task_id}")

        print(f"Found {len(model_hashes)} submissions. Downloading and aggregating...")

        schema_hash = self.sdk.get_task_schema_hash_from_contract(task_id)
        schema = self.sdk.get_task_schema(schema_hash)

        model_weights_list = []
        for model_hash in model_hashes:
            weights_file = self.sdk.download_model_weights_from_ipfs(model_hash)
            model = self.sdk.build_model_from_schema(schema)
            model = self.sdk.load_model_weights(model, weights_file)
            model_weights_list.append(model.get_weights())

        federated_weights = self.sdk.federated_average(model_weights_list)

        aggregated_model = self.sdk.build_model_from_schema(schema)
        aggregated_model.set_weights(federated_weights)

        weights_file = f"aggregated_{task_id}.h5"
        self.sdk.save_model_weights(aggregated_model, weights_file)
        aggregated_hash = self.sdk.upload_model_weights_to_ipfs(weights_file)

        print(f"Aggregated model uploaded to IPFS: {aggregated_hash}")
        return aggregated_hash
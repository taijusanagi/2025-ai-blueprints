"""
SDK for Federated Learning with IPFS and Filecoin integration.

This module provides functionality to:
1. Upload schema to IPFS
2. Upload tasks to Filecoin smart contracts
3. Integrate with TensorFlow models
"""

import json
import os
import time
import ipfshttpclient
import requests
from web3 import Web3
import tensorflow as tf
import numpy as np


class FederatedLearningSDK:
    """SDK for Federated Learning with IPFS and Filecoin integration."""
    
    def __init__(self, ipfs_api="/ip4/127.0.0.1/tcp/5001", filecoin_rpc="http://localhost:8545", 
                 contract_address=None, contract_abi=None):
        """
        Initialize the SDK with IPFS and Filecoin connection parameters.
        
        Args:
            ipfs_api (str): IPFS API endpoint
            filecoin_rpc (str): Filecoin RPC endpoint
            contract_address (str): Address of the deployed smart contract
            contract_abi (dict): ABI of the deployed smart contract
        """
        self.ipfs_api = ipfs_api
        self.filecoin_rpc = filecoin_rpc
        self.contract_address = contract_address
        self.contract_abi = contract_abi
        
        # Initialize connections
        try:
            self.ipfs_client = ipfshttpclient.connect(ipfs_api)
            print("Connected to IPFS")
        except Exception as e:
            print(f"Warning: Could not connect to IPFS: {e}")
            self.ipfs_client = None
            
        try:
            self.web3 = Web3(Web3.HTTPProvider(filecoin_rpc))
            if self.web3.is_connected():
                print("Connected to Filecoin network")
                if contract_address and contract_abi:
                    self.contract = self.web3.eth.contract(
                        address=contract_address,
                        abi=contract_abi
                    )
                    print("Smart contract initialized")
                else:
                    self.contract = None
                    print("Warning: Contract address or ABI not provided")
            else:
                print("Warning: Could not connect to Filecoin network")
                self.web3 = None
                self.contract = None
        except Exception as e:
            print(f"Warning: Could not initialize Web3: {e}")
            self.web3 = None
            self.contract = None
    
    def upload_schema_to_ipfs(self, schema):
        """
        Upload a schema to IPFS.
        
        Args:
            schema (dict): The schema to upload
            
        Returns:
            str: IPFS hash of the uploaded schema
        """
        if not self.ipfs_client:
            raise ConnectionError("IPFS client not initialized")
            
        # Convert schema to JSON string
        schema_json = json.dumps(schema)
        
        # Upload to IPFS
        result = self.ipfs_client.add_str(schema_json)
        print(f"Schema uploaded to IPFS with hash: {result}")
        
        return result
    
    def upload_task_to_filecoin(self, task_id, schema_hash, reward=0):
        """
        Upload a task to the Filecoin smart contract.
        
        Args:
            task_id (str): Unique identifier for the task
            schema_hash (str): IPFS hash of the task schema
            reward (int): Reward amount for completing the task
            
        Returns:
            str: Transaction hash
        """
        if not self.web3 or not self.contract:
            raise ConnectionError("Web3 or contract not initialized")
            
        # Get default account
        account = self.web3.eth.accounts[0]
        
        # Upload task to smart contract
        tx_hash = self.contract.functions.createTask(
            task_id,
            schema_hash,
            reward
        ).transact({'from': account, 'value': reward})
        
        # Wait for transaction to be mined
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Task uploaded to Filecoin with tx hash: {receipt.transactionHash.hex()}")
        
        return receipt.transactionHash.hex()
    
    def create_and_upload_task(self, task_schema, reward=0):
        """
        Create a task from schema and upload to IPFS and Filecoin.
        
        Args:
            task_schema (dict): The task schema
            reward (int): Reward amount for completing the task
            
        Returns:
            dict: Task information including IPFS hash and transaction hash
        """
        # Generate a unique task ID
        task_id = f"task_{int(time.time())}"
        
        # Upload schema to IPFS
        schema_hash = self.upload_schema_to_ipfs(task_schema)
        
        # Upload task to Filecoin
        tx_hash = self.upload_task_to_filecoin(task_id, schema_hash, reward)
        
        return {
            "task_id": task_id,
            "schema_hash": schema_hash,
            "tx_hash": tx_hash
        }
    
    def get_task_schema(self, schema_hash):
        """
        Get a task schema from IPFS.
        
        Args:
            schema_hash (str): IPFS hash of the schema
            
        Returns:
            dict: The task schema
        """
        if not self.ipfs_client:
            raise ConnectionError("IPFS client not initialized")
            
        # Get schema from IPFS
        schema_json = self.ipfs_client.cat(schema_hash)
        
        # Parse JSON
        schema = json.loads(schema_json)
        
        return schema
    
    def build_model_from_schema(self, schema):
        """
        Build a TensorFlow model from a schema.
        
        Args:
            schema (dict): The task schema
            
        Returns:
            tf.keras.Model: The built model
        """
        # Create a sequential model
        model = tf.keras.Sequential()
        
        # Add input layer
        input_shape = schema.get("input_shape", [])
        
        # Add layers according to the schema
        for layer_config in schema.get("model_architecture", []):
            layer_type = layer_config.get("type")
            
            if layer_type == "Dense":
                units = layer_config.get("units", 10)
                activation = layer_config.get("activation", "relu")
                model.add(tf.keras.layers.Dense(units=units, activation=activation))
            elif layer_type == "Conv2D":
                filters = layer_config.get("filters", 32)
                kernel_size = layer_config.get("kernel_size", (3, 3))
                activation = layer_config.get("activation", "relu")
                model.add(tf.keras.layers.Conv2D(filters=filters, kernel_size=kernel_size, activation=activation))
            elif layer_type == "MaxPooling2D":
                pool_size = layer_config.get("pool_size", (2, 2))
                model.add(tf.keras.layers.MaxPooling2D(pool_size=pool_size))
            elif layer_type == "Flatten":
                model.add(tf.keras.layers.Flatten())
            elif layer_type == "Dropout":
                rate = layer_config.get("rate", 0.5)
                model.add(tf.keras.layers.Dropout(rate=rate))
        
        # Compile the model
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def save_model_weights(self, model, filename="model_weights.h5"):
        """
        Save model weights to a file.
        
        Args:
            model (tf.keras.Model): The model
            filename (str): Output filename
            
        Returns:
            str: Path to the saved weights file
        """
        model.save_weights(filename)
        return filename
    
    def load_model_weights(self, model, filename="model_weights.h5"):
        """
        Load model weights from a file.
        
        Args:
            model (tf.keras.Model): The model
            filename (str): Input filename
            
        Returns:
            tf.keras.Model: The model with loaded weights
        """
        model.load_weights(filename)
        return model
    
    def upload_model_weights_to_ipfs(self, weights_file):
        """
        Upload model weights to IPFS.
        
        Args:
            weights_file (str): Path to the weights file
            
        Returns:
            str: IPFS hash of the uploaded weights
        """
        if not self.ipfs_client:
            raise ConnectionError("IPFS client not initialized")
            
        # Upload to IPFS
        with open(weights_file, 'rb') as f:
            result = self.ipfs_client.add(f)
            
        print(f"Model weights uploaded to IPFS with hash: {result['Hash']}")
        
        return result['Hash']
    
    def download_model_weights_from_ipfs(self, weights_hash, output_file="downloaded_weights.h5"):
        """
        Download model weights from IPFS.
        
        Args:
            weights_hash (str): IPFS hash of the weights
            output_file (str): Output filename
            
        Returns:
            str: Path to the downloaded weights file
        """
        if not self.ipfs_client:
            raise ConnectionError("IPFS client not initialized")
            
        # Download from IPFS
        self.ipfs_client.get(weights_hash)
        
        # Move to the desired location
        os.rename(weights_hash, output_file)
        
        return output_file
    
    def federated_average(self, weight_list):
        """
        Perform federated averaging on a list of model weights.
        
        Args:
            weight_list (list): List of model weight arrays
            
        Returns:
            list: Averaged model weights
        """
        # Convert to numpy arrays if needed
        weight_arrays = []
        for weights in weight_list:
            if isinstance(weights, str):
                # If weights are provided as filenames, load them
                model = tf.keras.Sequential([tf.keras.layers.Dense(1, input_shape=(1,))])
                model.load_weights(weights)
                weight_arrays.append([w.numpy() for w in model.weights])
            else:
                weight_arrays.append(weights)
        
        # Calculate average weights
        avg_weights = []
        for weights_per_layer in zip(*weight_arrays):
            avg_weights.append(np.mean(weights_per_layer, axis=0))
        
        return avg_weights
    
    def apply_federated_weights(self, model, federated_weights):
        """
        Apply federated weights to a model.
        
        Args:
            model (tf.keras.Model): The model
            federated_weights (list): Federated weights
            
        Returns:
            tf.keras.Model: The model with applied weights
        """
        for i, layer in enumerate(model.layers):
            layer.set_weights([federated_weights[i]])
        
        return model

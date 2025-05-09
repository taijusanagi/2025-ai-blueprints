import json
import io
import os
import time
import ipfshttpclient
from web3 import Web3
import tensorflow as tf
import numpy as np
import requests
import mimetypes
from eth_account import Account

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.bool_):
            return bool(obj)
        return super(NumpyEncoder, self).default(obj)

class FederatedLearningSDK:
    """Streamlined SDK for Federated Learning with IPFS and Filecoin integration."""
    
    def __init__(self, provider="ipfs", bucket_id="myBucket", akave_api_url="http://localhost:8000",
                 ipfs_api="/ip4/127.0.0.1/tcp/5001", filecoin_rpc="https://rpc.ankr.com/filecoin_testnet", 
                 contract_address=None, contract_abi=None, private_key=None):
        self.provider = provider
        self.bucket_id = bucket_id
        self.akave_api_url = akave_api_url
        self.ipfs_api = ipfs_api
        
        # Get private key from parameter or environment variable
        self.private_key = private_key or os.getenv("PRIVATE_KEY")
        self.account_address = None
        
        # Initialize connections
        if provider == "ipfs":
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
                
                # Set up account from private key if provided
                if self.private_key:
                    # Ensure the private key has 0x prefix
                    if not self.private_key.startswith('0x'):
                        self.private_key = '0x' + self.private_key
                    account = Account.from_key(self.private_key)
                    self.account_address = account.address
                    print(f"Using account: {self.account_address}")
                
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
    
    def _get_account(self):
        """
        Get the account address to use for transactions.
        
        Returns:
            str: Account address
        """
        if self.account_address:
            return self.account_address
        
        # Fallback to using the first account (only works with unlocked accounts)
        if self.web3 and self.web3.eth.accounts:
            return self.web3.eth.accounts[0]
        
        raise ValueError("No account available. Please provide a private key via parameter or PRIVATE_KEY environment variable.")
    
    def _sign_and_send_transaction(self, function_call):
        """
        Sign a transaction with the private key and send it.
        
        Args:
            function_call: Contract function call
            
        Returns:
            str: Transaction hash
        """
        if not self.web3:
            raise ConnectionError("Web3 not initialized")
        
        account_address = self._get_account()
        
        # If using private key, sign transaction
        if self.private_key:
            # Get transaction details
            tx = function_call.build_transaction({
                'from': account_address,
                'nonce': self.web3.eth.get_transaction_count(account_address),
                'gas': 100000000,  # Gas limit, adjust as needed
                'gasPrice': self.web3.eth.gas_price
            })
            
            # Sign transaction (private_key is an instance variable, not local)
            signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
            
            # Send transaction
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        else:
            # If no private key, use default account (requires unlocked account)
            tx_hash = function_call.transact({'from': account_address})
        
        # Wait for transaction to be mined
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt
    
    def upload(self, content, is_file=False, name=None):
        if self.provider == "ipfs":
            return self.upload_to_ipfs(content, is_file)
        elif self.provider == "akave":
            return self.upload_to_akave(content, is_file, name)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def upload_to_ipfs(self, content, is_file=False):
        """
        Upload content to IPFS.
        
        Args:
            content: Content to upload (string or file path)
            is_file (bool): Whether content is a file path
            
        Returns:
            str: IPFS hash of the uploaded content
        """
        if not self.ipfs_client:
            raise ConnectionError("IPFS client not initialized")
            
        if is_file:
            with open(content, 'rb') as f:
                result = self.ipfs_client.add(f)
                return result['Hash']
        else:
            # Assume content is a string or JSON
            if isinstance(content, dict):
                content = json.dumps(content)
            return self.ipfs_client.add_str(content)
        
    def upload_to_akave(self, content, is_file=False, name=None):
        if not self.akave_api_url or not self.bucket_id:
            raise ValueError("Akave API URL and bucket ID must be provided")

        # Default filename and MIME type
        if is_file:
            ext = os.path.splitext(name or content)[1]
            mime = mimetypes.types_map.get(ext, 'application/octet-stream')
            filename = name or os.path.basename(content)
        else:
            filename = name
            mime = "application/json"

        # Prepare file-like object
        if is_file:
            file_data = open(content, 'rb')
            files = {'file': (filename, file_data, mime)}
        else:
            if isinstance(content, dict):
                content = json.dumps(content, cls=NumpyEncoder)
            file_data = io.BytesIO(content.encode('utf-8'))
            files = {'file': (filename, file_data, mime)}

        try:
            response = requests.post(
                f"{self.akave_api_url}/buckets/{self.bucket_id}/files",
                files=files
            )
        finally:
            if is_file:
                file_data.close()

        try:
            res_json = response.json()
            if res_json.get("success") and "data" in res_json:
                return res_json["data"]["RootCID"]
            else:
                raise Exception(f"Akave upload failed: {res_json}")
        except ValueError:
            print("Response Text:", response.text)
            raise Exception("Akave upload failed: Invalid JSON response")

    def download(self, identifier, name, output_path=None):
        """
        Download content based on provider.

        Args:
            identifier (str): IPFS hash or filename depending on the provider.
            output_path (str, optional): Path to save the file (for file-based downloads).

        Returns:
            bytes or str: Content of the file or path to the saved file.
        """
        if self.provider == "ipfs":
            return self.download_from_ipfs(identifier, output_path)
        elif self.provider == "akave":
            return self.download_from_akave(name, output_path)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def download_from_ipfs(self, content_hash, output_path=None):
        """
        Download content from IPFS.
        
        Args:
            content_hash (str): IPFS hash of the content
            output_path (str): Path to save the content (for files)
            
        Returns:
            Content or path to downloaded file
        """
        if not self.ipfs_client:
            raise ConnectionError("IPFS client not initialized")
        
        if output_path:
            # Download as file
            self.ipfs_client.get(content_hash)
            # Move to desired location
            os.rename(content_hash, output_path)
            return output_path
        else:
            # Return as data
            return self.ipfs_client.cat(content_hash)
        
    def download_from_akave(self, filename, output_path=None):
        """
        Download a file from Akave.

        Args:
            filename (str): The name of the file to download.
            output_path (str, optional): Path to save the downloaded file.

        Returns:
            bytes or str: Content of the file or path to the saved file.
        """
        if not self.akave_api_url or not self.bucket_id:
            raise ValueError("Akave API URL and bucket ID must be provided")

        download_url = f"{self.akave_api_url}/buckets/{self.bucket_id}/files/{filename}/download"
        response = requests.get(download_url)

        if response.status_code != 200:
            raise Exception(f"Failed to download file: {response.status_code}, {response.text}")

        if output_path:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return output_path
        else:
            return response.content

    
    # --- Common Operations ---
    def build_model_from_schema(self, schema):
        """
        Build a TensorFlow model from a schema.
        
        Args:
            schema (dict): The task schema
            
        Returns:
            tf.keras.Model: The built model
        """
        model = tf.keras.Sequential()
        input_shape = schema.get("input_shape")
        
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
        
        model.build(input_shape=(None, *input_shape))
        # Compile the model
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    # --- Aggregator Operations ---
    
    def create_task(self, schema, task_id=None):
        """
        Create a task and upload it to the Filecoin smart contract.
        
        Args:
            schema (dict): The task schema (model architecture, etc.)
            task_id (str, optional): Custom task ID, generated if not provided
            
        Returns:
            dict: Task information including IDs and hashes
        """
        if not self.web3 or not self.contract:
            raise ConnectionError("Web3 or contract not initialized")
        
        # Generate task ID if not provided
        if not task_id:
            task_id = f"task_{int(time.time())}"
        
        # Upload schema to IPFS
        schema_hash = self.upload(schema, name=task_id)
        
        # Create task on the blockchain
        receipt = self._sign_and_send_transaction(
            self.contract.functions.createTask(task_id, schema_hash)
        )
        
        return {
            "task_id": task_id,
            "schema_hash": schema_hash,
            "tx_hash": receipt.transactionHash.hex()
        }
    
    def aggregate_models(self, task_id, output_file="aggregated_model.weights.h5"):
        """
        Fetch all model submissions for a task and perform federated averaging.
        
        Args:
            task_id (str): ID of the task
            output_file (str): Path to save the aggregated model weights
            
        Returns:
            str: Path to the aggregated model weights file
        """
        # Get all tasks
        all_tasks = self.contract.functions.getTasks().call()
        
        # Find the specific task and its submissions
        task_data = None
        for task in all_tasks:
            if task[0] == task_id:  # task_id is the first element
                task_data = {
                    "task_id": task[0],
                    "schema_hash": task[1],
                    "creator": task[2],
                    "timestamp": task[3],
                    "submissions": []
                }
                
                # Extract submissions if any
                if len(task) > 4 and task[4]:
                    for submission in task[4]:
                        task_data["submissions"].append({
                            "model_hash": submission[0],
                            "modelMetadata": submission[1],
                            "submitter": submission[2],
                            "timestamp": submission[3]
                        })
                break
        
        if not task_data:
            raise ValueError(f"Task {task_id} not found")
        
        if not task_data["submissions"]:
            raise ValueError(f"No submissions found for task {task_id}")
            
        # Get the schema to build the model
        schema_json = self.download(task_data["schema_hash"], task_id)
        schema = json.loads(schema_json)
        
        # Build model from schema
        model = self.build_model_from_schema(schema)
        
        # Download and collect all model weights
        all_weights = []
        temp_dir = f"temp_models_{task_id}"
        os.makedirs(temp_dir, exist_ok=True)
        
        for i, submission in enumerate(task_data["submissions"]):
            model_hash = submission["model_hash"]
            model_name = submission["modelMetadata"]
            temp_file = os.path.join(temp_dir, f"model_{i}.weights.h5")
            
            # Download model weights
            self.download(model_hash, model_name, temp_file)
            
            # Load weights and collect
            model.load_weights(temp_file)
            all_weights.append([layer.get_weights() for layer in model.layers])  # Get all weights including biases
        
        # Perform federated averaging
        averaged_weights = self._federated_average(all_weights)
        
        # Apply averaged weights to model
        for i, layer in enumerate(model.layers):
            layer.set_weights(averaged_weights[i])  # Set all weights including biases
        
        # Save aggregated model
        model.save_weights(output_file)
        
        # Clean up temp files
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)
        
        return output_file
    
    # --- Node Operations ---
    
    def get_task_schema(self, task_id):
        """
        Get the schema for a specific task.
        
        Args:
            task_id (str): The task ID
            
        Returns:
            dict: The task schema
        """
        # Get all tasks
        all_tasks = self.contract.functions.getTasks().call()
        
        # Find the specific task
        schema_hash = None
        for task in all_tasks:
            if task[0] == task_id:  # task_id is the first element
                schema_hash = task[1]  # schema_hash is the second element
                break
        
        if not schema_hash:
            raise ValueError(f"Task {task_id} not found")
        
        # Get schema from IPFS
        schema_json = self.download(schema_hash, task_id)
        
        # Parse and return
        return json.loads(schema_json)
    
    def submit_model(self, task_id, model_weights_file, accuracy: float):
        """
        Submit trained model weights for a task.
        
        Args:
            task_id (str): ID of the task to submit to
            model_weights_file (str): Path to the saved weights file (.h5)
            accuracy (float): Model accuracy (0.0 to 1.0)
            
        Returns:
            str: Transaction hash
        """
        if not self.web3 or not self.contract:
            raise ConnectionError("Web3 or contract not initialized")
        
        # Upload weights to IPFS
        name = os.path.basename(model_weights_file)
        model_hash = self.upload(model_weights_file, is_file=True, name=name)
        
        # Submit to blockchain
        receipt = self._sign_and_send_transaction(
            self.contract.functions.submitModel(
                task_id,
                model_hash,
                name,
                int(accuracy * 10000)
            )
        )
        
        return receipt.transactionHash.hex()
    
    def submit_final_model(self, task_id, final_model_weights_file, accuracy: float):
        """
        Submit the final aggregated model to the smart contract.

        Args:
            task_id (str): The task ID for which to submit the final model.
            final_model_weights_file (str): Path to the final aggregated model weights (.h5)
            accuracy (float): Model accuracy (0.0 to 1.0)

        Returns:
            str: Transaction hash of the submission
        """
        if not self.web3 or not self.contract:
            raise ConnectionError("Web3 or contract not initialized")

        # Upload final weights to IPFS
        final_model_hash = self.upload(final_model_weights_file, is_file=True, name=final_model_weights_file)

        # Submit the final model on-chain
        receipt = self._sign_and_send_transaction(
            self.contract.functions.submitFinalModel(
                task_id,
                final_model_hash,
                final_model_weights_file,
                int(accuracy * 10000)
            )
        )

        return receipt.transactionHash.hex()
    
    # --- Helper Methods ---
    def _federated_average(self, weight_list):
        """
        Perform federated averaging on a list of model weights.
        
        Args:
            weight_list (list): List of model weight arrays
            
        Returns:
            list: Averaged model weights
        """
        # Calculate average weights
        num_models = len(weight_list)
        num_layers = len(weight_list[0])
        
        # Initialize averaged weights structure
        avg_weights = []
        
        # For each layer
        for layer_idx in range(num_layers):
            # Get weights for this layer from all models
            layer_weights = [model_weights[layer_idx] for model_weights in weight_list]
            
            # Each layer might have multiple weight tensors (weights and biases)
            # Initialize list to hold averaged tensors for this layer
            avg_layer_weights = []
            
            # For each weight tensor in the layer
            for weight_idx in range(len(layer_weights[0])):
                # Extract the same weight tensor from all models
                weight_tensors = [model_layer_weights[weight_idx] for model_layer_weights in layer_weights]
                
                # Compute average
                avg_tensor = np.mean(weight_tensors, axis=0)
                avg_layer_weights.append(avg_tensor)
            
            avg_weights.append(avg_layer_weights)
        
        return avg_weights
    
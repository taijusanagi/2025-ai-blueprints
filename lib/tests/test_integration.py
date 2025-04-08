"""
Integration test for the Federated Learning Library.

This script demonstrates how the SDK, Aggregator, and Node components work together.
Since we don't have actual IPFS and Filecoin networks available for testing,
this example uses mock connections and local file operations.
"""

import os
import json
import sys
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules
from sdk import FederatedLearningSDK
from aggregator import FederatedLearningAggregator
from node import FederatedLearningNode

# Create a directory for test files
os.makedirs("test_files", exist_ok=True)

# Load the example task schema
with open("../examples/iris_task_schema.json", "r") as f:
    task_schema = json.load(f)

print("Loaded task schema:", task_schema)

# Create mock SDK (without actual IPFS/Filecoin connections)
class MockSDK(FederatedLearningSDK):
    def __init__(self):
        # Skip actual connections
        self.ipfs_client = None
        self.web3 = None
        self.contract = None
        self.schemas = {}
        self.weights = {}
    
    def upload_schema_to_ipfs(self, schema):
        # Mock IPFS upload by storing locally and returning a fake hash
        schema_hash = f"schema_{hash(json.dumps(schema))}"
        self.schemas[schema_hash] = schema
        return schema_hash
    
    def get_task_schema(self, schema_hash):
        # Return schema from local storage
        return self.schemas.get(schema_hash, {})
    
    def upload_model_weights_to_ipfs(self, weights_file):
        # Mock IPFS upload by storing file path and returning a fake hash
        weights_hash = f"weights_{hash(weights_file)}"
        self.weights[weights_hash] = weights_file
        return weights_hash
    
    def download_model_weights_from_ipfs(self, weights_hash, output_file):
        # Mock IPFS download by copying the file
        import shutil
        source_file = self.weights.get(weights_hash)
        if source_file:
            shutil.copy(source_file, output_file)
        return output_file
    
    def upload_task_to_filecoin(self, task_id, schema_hash, reward=0):
        # Mock Filecoin upload by returning a fake transaction hash
        return f"tx_{hash(task_id + schema_hash)}"

# Initialize our components with the mock SDK
sdk = MockSDK()
aggregator = FederatedLearningAggregator(sdk=sdk)
node1 = FederatedLearningNode(node_id="node1", sdk=sdk)
node2 = FederatedLearningNode(node_id="node2", sdk=sdk)

print("\n=== Testing Federated Learning Workflow ===\n")

# Step 1: Aggregator creates a task
print("Step 1: Creating task...")
task_info = aggregator.create_task(task_schema)
task_id = task_info['task_id']
schema_hash = task_info['schema_hash']
print(f"Task created with ID: {task_id}")
print(f"Schema hash: {schema_hash}")

# Step 2: Nodes fetch the task
print("\nStep 2: Nodes fetching task...")
node1_schema = node1.fetch_task(task_id=task_id, schema_hash=schema_hash)
node2_schema = node2.fetch_task(task_id=task_id, schema_hash=schema_hash)
print(f"Node 1 fetched task: {node1.get_task_status(task_id)['status']}")
print(f"Node 2 fetched task: {node2.get_task_status(task_id)['status']}")

# Step 3: Nodes train models with their own data
print("\nStep 3: Nodes training models...")
# Load Iris dataset
iris = datasets.load_iris()
X = iris.data
y = iris.target

# Split into two parts to simulate different nodes having different data
X1, X2, y1, y2 = train_test_split(X, y, test_size=0.5, random_state=42)

# Further split each node's data into train/test
X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, test_size=0.2, random_state=42)
X2_train, X2_test, y2_train, y2_test = train_test_split(X2, y2, test_size=0.2, random_state=42)

# Standardize features
scaler1 = StandardScaler()
X1_train = scaler1.fit_transform(X1_train)
X1_test = scaler1.transform(X1_test)

scaler2 = StandardScaler()
X2_train = scaler2.fit_transform(X2_train)
X2_test = scaler2.transform(X2_test)

# Train models
node1_result = node1.train_model(task_id, X1_train, y1_train, epochs=5, batch_size=8)
node2_result = node2.train_model(task_id, X2_train, y2_train, epochs=5, batch_size=8)

print(f"Node 1 training metrics: {node1_result['metrics']}")
print(f"Node 2 training metrics: {node2_result['metrics']}")

# Step 4: Nodes submit results
print("\nStep 4: Nodes submitting results...")
node1_submission = node1.submit_results(task_id)
node2_submission = node2.submit_results(task_id)

print(f"Node 1 submission: {node1_submission}")
print(f"Node 2 submission: {node2_submission}")

# Step 5: Aggregator receives results
print("\nStep 5: Aggregator receiving results...")
aggregator.receive_node_result(
    task_id, 
    node1.node_id, 
    weights_file=node1.training_results[task_id]['weights_file'],
    weights_hash=node1_submission['weights_hash'],
    metrics=node1.training_results[task_id]['metrics']
)

aggregator.receive_node_result(
    task_id, 
    node2.node_id, 
    weights_file=node2.training_results[task_id]['weights_file'],
    weights_hash=node2_submission['weights_hash'],
    metrics=node2.training_results[task_id]['metrics']
)

print(f"Aggregator task status: {aggregator.get_task_status(task_id)}")

# Step 6: Aggregator performs federated averaging
print("\nStep 6: Aggregator performing federated averaging...")
aggregation_result = aggregator.aggregate_results(task_id, min_nodes=2)

print(f"Aggregation result: {aggregation_result}")

# Step 7: Evaluate the aggregated model
print("\nStep 7: Evaluating the aggregated model...")
# Combine test data from both nodes for evaluation
X_test = np.vstack([X1_test, X2_test])
y_test = np.concatenate([y1_test, y2_test])

# Evaluate
metrics = aggregator.evaluate_aggregated_model(task_id, X_test, y_test)

print(f"Aggregated model evaluation metrics: {metrics}")
print("\n=== Federated Learning Workflow Completed Successfully ===\n")

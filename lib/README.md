# Federated Learning Library

A Python library for federated learning with IPFS and Filecoin integration.

## Overview

This library provides a complete solution for federated learning with three main components:

1. **SDK** - Handles IPFS schema uploads and Filecoin smart contract integration
2. **Aggregator** - Creates tasks with schema and aggregates training results
3. **Node** - Fetches tasks and uses local data for machine learning

The library is compatible with TensorFlow and supports federated averaging of model weights.

## Installation

```bash
pip install -r requirements.txt
```

## Components

### SDK (sdk.py)

The SDK component provides functionality to:
- Upload schema to IPFS
- Upload tasks to Filecoin smart contracts
- Build TensorFlow models from schema
- Save and load model weights
- Perform federated averaging

### Aggregator (aggregator.py)

The Aggregator component provides functionality to:
- Create tasks with schema
- Register nodes for tasks
- Receive training results from nodes
- Aggregate results using federated averaging
- Evaluate aggregated models

### Node (node.py)

The Node component provides functionality to:
- Fetch tasks from the network
- Load local datasets (currently supports Iris dataset)
- Train models based on task schema
- Submit results back to the network

## Task Schema

Tasks are defined using a JSON schema that specifies the dataset, features, and model architecture. Example:

```json
{
  "task": "iris",
  "features": ["sepal_length", "sepal_width", "petal_length", "petal_width"],
  "input_shape": [4],
  "num_classes": 3,
  "model_architecture": [
    {"type": "Dense", "units": 10, "activation": "relu"},
    {"type": "Dense", "units": 3, "activation": "softmax"}
  ]
}
```

## Usage Examples

### Setting up the SDK

```python
from sdk import FederatedLearningSDK

# Initialize SDK with IPFS and Filecoin connection parameters
sdk = FederatedLearningSDK(
    ipfs_api="/ip4/127.0.0.1/tcp/5001",
    filecoin_rpc="http://localhost:8545",
    contract_address="0x123...",
    contract_abi={}
)
```

### Creating a Task (Aggregator)

```python
from aggregator import FederatedLearningAggregator

# Initialize Aggregator with SDK
aggregator = FederatedLearningAggregator(sdk=sdk)

# Create a task
task_schema = {
    "task": "iris",
    "features": ["sepal_length", "sepal_width", "petal_length", "petal_width"],
    "input_shape": [4],
    "num_classes": 3,
    "model_architecture": [
        {"type": "Dense", "units": 10, "activation": "relu"},
        {"type": "Dense", "units": 3, "activation": "softmax"}
    ]
}

task_info = aggregator.create_task(task_schema)
task_id = task_info['task_id']
schema_hash = task_info['schema_hash']
```

### Training a Model (Node)

```python
from node import FederatedLearningNode

# Initialize Node with SDK
node = FederatedLearningNode(node_id="node1", sdk=sdk)

# Fetch task
node.fetch_task(task_id=task_id, schema_hash=schema_hash)

# Train model with local data
training_result = node.train_model(task_id)

# Submit results
submission_result = node.submit_results(task_id)
```

### Aggregating Results (Aggregator)

```python
# Receive results from nodes
aggregator.receive_node_result(
    task_id, 
    node_id="node1", 
    weights_file="model_weights.h5",
    weights_hash="hash123",
    metrics={"accuracy": 0.95}
)

# Aggregate results
aggregation_result = aggregator.aggregate_results(task_id, min_nodes=1)

# Evaluate aggregated model
metrics = aggregator.evaluate_aggregated_model(task_id, x_test, y_test)
```

### Complete Workflow Example

See `tests/test_integration.py` for a complete example of the federated learning workflow.

## API Reference

### SDK (FederatedLearningSDK)

#### Initialization
```python
sdk = FederatedLearningSDK(
    ipfs_api="/ip4/127.0.0.1/tcp/5001",
    filecoin_rpc="http://localhost:8545",
    contract_address=None,
    contract_abi=None
)
```

#### Methods
- `upload_schema_to_ipfs(schema)` - Upload a schema to IPFS
- `upload_task_to_filecoin(task_id, schema_hash, reward=0)` - Upload a task to Filecoin
- `create_and_upload_task(task_schema, reward=0)` - Create and upload a task
- `get_task_schema(schema_hash)` - Get a task schema from IPFS
- `build_model_from_schema(schema)` - Build a TensorFlow model from a schema
- `save_model_weights(model, filename)` - Save model weights to a file
- `load_model_weights(model, filename)` - Load model weights from a file
- `upload_model_weights_to_ipfs(weights_file)` - Upload model weights to IPFS
- `download_model_weights_from_ipfs(weights_hash, output_file)` - Download model weights from IPFS
- `federated_average(weight_list)` - Perform federated averaging on model weights
- `apply_federated_weights(model, federated_weights)` - Apply federated weights to a model

### Aggregator (FederatedLearningAggregator)

#### Initialization
```python
aggregator = FederatedLearningAggregator(
    sdk=None,
    ipfs_api="/ip4/127.0.0.1/tcp/5001",
    filecoin_rpc="http://localhost:8545",
    contract_address=None,
    contract_abi=None
)
```

#### Methods
- `create_task(task_schema, reward=0)` - Create a new federated learning task
- `register_node(task_id, node_id)` - Register a node for a task
- `receive_node_result(task_id, node_id, weights_file, weights_hash, metrics)` - Receive training result from a node
- `aggregate_results(task_id, min_nodes=1, download_if_needed=True)` - Aggregate results from nodes
- `get_task_status(task_id)` - Get status of a task
- `get_all_tasks()` - Get all tasks
- `evaluate_aggregated_model(task_id, x_test, y_test)` - Evaluate an aggregated model

### Node (FederatedLearningNode)

#### Initialization
```python
node = FederatedLearningNode(
    node_id=None,
    sdk=None,
    ipfs_api="/ip4/127.0.0.1/tcp/5001",
    filecoin_rpc="http://localhost:8545",
    contract_address=None,
    contract_abi=None
)
```

#### Methods
- `fetch_task(task_id=None, schema_hash=None)` - Fetch a task from the network
- `load_iris_dataset()` - Load the Iris dataset for testing
- `load_dataset(task_name, features=None)` - Load a dataset based on task name
- `train_model(task_id, x_train=None, y_train=None, epochs=10, batch_size=32, validation_split=0.2)` - Train a model for a task
- `submit_results(task_id, aggregator_endpoint=None)` - Submit training results to the network
- `get_task_status(task_id)` - Get status of a task
- `get_all_tasks()` - Get all tasks
- `process_task(task_id=None, schema_hash=None, epochs=10, batch_size=32, submit=True, aggregator_endpoint=None)` - Process a task end-to-end

## License

MIT

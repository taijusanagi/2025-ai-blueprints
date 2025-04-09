#!/bin/bash

# Allowed values
VALID_DATASETS=("iris" "wine" "breast_cancer")
VALID_COMPLEXITY=("simple" "medium" "complex")

# Prompt for task ID
read -p "Enter a name for the task: " INPUT
TASK_ID=$INPUT

# Prompt for dataset
read -p "Enter the dataset name (iris, wine, breast_cancer): " DATASET

# Validate dataset
if [[ ! " ${VALID_DATASETS[@]} " =~ " ${DATASET} " ]]; then
    echo "❌ Invalid dataset: '$DATASET'"
    echo "✅ Allowed values: iris, wine, breast_cancer"
    exit 1
fi

# Prompt for model complexity
read -p "Enter model complexity (simple, medium, complex): " MODEL_COMPLEXITY

# Validate model complexity
if [[ ! " ${VALID_COMPLEXITY[@]} " =~ " ${MODEL_COMPLEXITY} " ]]; then
    echo "❌ Invalid model complexity: '$MODEL_COMPLEXITY'"
    echo "✅ Allowed values: simple, medium, complex"
    exit 1
fi

echo "Using task ID: $TASK_ID"
echo "Using dataset: $DATASET"
echo "Using model complexity: $MODEL_COMPLEXITY"

# Run the Python scripts with all arguments
python create.py --task_id "$TASK_ID" --dataset "$DATASET" --model_complexity "$MODEL_COMPLEXITY"
python submit.py --task_id "$TASK_ID" --dataset "$DATASET"
python submit.py --task_id "$TASK_ID" --dataset "$DATASET"
python submit.py --task_id "$TASK_ID" --dataset "$DATASET"
# python aggregate.py --task_id "$TASK_ID" --dataset "$DATASET"

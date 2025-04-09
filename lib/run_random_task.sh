#!/bin/bash

# Allowed datasets
VALID_DATASETS=("iris" "wine" "breast_cancer")

# Prompt for task ID
read -p "Enter a name for the task: " INPUT
TASK_ID=$INPUT

# Prompt for dataset name
read -p "Enter the dataset name (iris, wine, breast_cancer): " DATASET

# Validate dataset
if [[ ! " ${VALID_DATASETS[@]} " =~ " ${DATASET} " ]]; then
    echo "❌ Invalid dataset: '$DATASET'"
    echo "✅ Allowed values: iris, wine, breast_cancer"
    exit 1
fi

echo "Using task ID: $TASK_ID"
echo "Using dataset: $DATASET"

python create.py --task_id "$TASK_ID" --dataset "$DATASET"
python submit.py --task_id "$TASK_ID" --dataset "$DATASET"
python submit.py --task_id "$TASK_ID" --dataset "$DATASET"
python submit.py --task_id "$TASK_ID" --dataset "$DATASET"
python aggregate.py --task_id "$TASK_ID" --dataset "$DATASET"

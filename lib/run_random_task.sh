#!/bin/bash

# Prompt user for a task name or ID suffix
read -p "Enter a name for the task: " INPUT

TASK_ID=$INPUT

echo "Using task ID: $TASK_ID"

python create.py --task_id "$TASK_ID"
python submit.py --task_id "$TASK_ID"
python submit.py --task_id "$TASK_ID"
python submit.py --task_id "$TASK_ID"
python aggregate.py --task_id "$TASK_ID"
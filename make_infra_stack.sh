#! /bin/sh

MODELS_FILES_DIR=$1
MODEL=$2

# Read variable from the file
json_data=$(cat domain/${MODEL}_domain.json)

# Define variables for model
PROJECT_NAME=$(echo $json_data | jq -r '.project_name')
MODEL_CLASS_NAME=$(echo $json_data | jq -r '.model_class_name')
MODEL_NAME=$(echo $json_data | jq -r '.model_name')
MODEL_PARTITION_KEY=$(echo $json_data | jq -r '.model_partition_key')

# Get stack template
cookiecutter gh:danilmunoz1996/sls-basic-infra-stack-template --no-input project_name="$PROJECT_NAME-stack" \
model="$MODEL_NAME" \
model_class_name="$MODEL_CLASS_NAME"
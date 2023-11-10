#! /bin/sh

MODELS_FILES_DIR=$1
MODEL=$2

# Read variable from the file
json_data=$(cat domain/${MODEL}_domain.json)

export PROJECT_NAME=$(echo $json_data | jq -r '.project_name')
export MODEL_CLASS_NAME=$(echo $json_data | jq -r '.model_class_name')
export MODEL_NAME=$(echo $json_data | jq -r '.model_name')
export MODEL_PARTITION_KEY=$(echo $json_data | jq -r '.model_partition_key')


# Use cookiecutter for creating the project
cookiecutter gh:danilmunoz1996/sls-crud-cookiecutter-template --no-input project_name="$PROJECT_NAME" \
model_class_name="$MODEL_CLASS_NAME" \
model_name="$MODEL_NAME" \
model_partition_key="$MODEL_PARTITION_KEY"

mv $PROJECT_NAME backend/$PROJECT_NAME

# copy the domain class to the project
cd backend/$PROJECT_NAME/src/
mkdir domain
cd ../../../
mv $MODELS_FILES_DIR/$MODEL_CLASS_NAME.js backend/$PROJECT_NAME/src/domain/$MODEL_CLASS_NAME.js

# remove the domain.json file
# rm ${1}_domain.json

# # go to the project
# cd $PROJECT_NAME

# # install dependencies
# npm install

# # deploy the project
# sls deploy
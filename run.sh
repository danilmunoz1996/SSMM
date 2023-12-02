#! /bin/sh

# MODELS FILES FOLDER
MODELS_CLASS_FILES_DIR=$1

# MODELS_FILE_NAME
MODELS_FILE_NAME=$2

# PROJECT NAME
PROJECT_NAME=$3

# deploy?
DEPLOY=$4

# Check if domain dir exists
if [ -d "domain" ]; then
    rm -rf domain
fi

# Create Folder for Domain Classes
mkdir domain

# Check if $MODELS_FILE_NAME exisTS, when exists, delete it
if [ -f "$MODELS_FILE_NAME" ]; then
    rm $MODELS_FILE_NAME
fi

# Domain Classes Definition
python get_domain_classes.py $MODELS_FILE_NAME

# Create Folder for Models Class Files
mkdir $MODELS_CLASS_FILES_DIR

# Domain Class Files Creation
python backend_class_files_generator.py $MODELS_CLASS_FILES_DIR $MODELS_FILE_NAME

# API SERVICE CREATION

# Check if Services dir exists
if [ -d "services" ]; then
    rm -rf services
fi

# Create Folder for Services
mkdir services

python make_class_api.py $MODELS_FILE_NAME


# For each model in models.json execute backend.sh
models=$(cat ${MODELS_FILE_NAME})

# Check if backend dir exists
if [ -d "backend" ]; then
    rm -rf backend
fi

# Make backend dir
mkdir backend

for element in $(echo "${models}" | jq -r '.[]'); do
    ./make_backend.sh $MODELS_CLASS_FILES_DIR $element
done

# generate infra stack files
python make_infra_stack_file.py $MODELS_FILE_NAME

# Delete MODELS_CLASS_FILES_DIR
rm -rf $MODELS_CLASS_FILES_DIR
# create and deploy infraestructure
./infra.sh $MODELS_FILE_NAME $DEPLOY

# Check if project name dir exists
if [ -d "$PROJECT_NAME" ]; then
    rm -rf $PROJECT_NAME
fi

# Move backend, and infrastructure to project name dir
mkdir $PROJECT_NAME
mv backend $PROJECT_NAME/backend
mv infrastructure $PROJECT_NAME/infrastructure

# if deploy is true, deploy microservices

if [ "$DEPLOY" = true ] ; then
    for element in $(echo "${models}" | jq -r '.[]'); do
        cd backend/$element-service
        npm i
        sls deploy
        cd ..
        cd ..
    done
fi
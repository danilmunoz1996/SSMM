#! /bin/sh

# MODELS FILES FOLDER
MODELS_CLASS_FILES_DIR=$1

# MODELS_FILE_NAME
MODELS_FILE_NAME=$2

# Create domain directory
mkdir domain

# Domain Classes Definition
python get_domain_classes.py $MODELS_FILE_NAME

# Create Folder for Models Class Files
mkdir $MODELS_CLASS_FILES_DIR

# Domain Class Files Creation
python backend_class_files_generator.py $MODELS_CLASS_FILES_DIR $MODELS_FILE_NAME



# For each model in models.json execute backend.sh
models=$(cat ${MODELS_FILE_NAME})

# Make backend dir
mkdir backend

for element in $(echo "${models}" | jq -r '.[]'); do
    echo "${element}"
    ./make_backend.sh $MODELS_CLASS_FILES_DIR $element
    ./make_infra_stack.sh $MODELS_CLASS_FILES_DIR $element
done

# Delete MODELS_CLASS_FILES_DIR
rm -rf $MODELS_CLASS_FILES_DIR
# create and deploy infraestructure
./infra.sh $MODELS_FILE_NAME

# deploy microservices
#for element in $(echo "${models}" | jq -r '.[]'); do
#    echo "${element}"
#    cd $element-service
#    npm i
#    sls deploy
#    cd ..
# done
#! /bin/sh


# MODELS FILE NAME
MODELS_FILE_NAME=$1

# DEPLOY?
DEPLOY=$2

# Check if infrastructure dir exists
if [ -d "infrastructure" ]; then
    rm -rf infrastructure
fi

# Get infra template
cookiecutter gh:danilmunoz1996/sls-crud-infra --no-input project_name="infrastructure"

# Get created stacks
models=$(cat ${MODELS_FILE_NAME})

for element in $(echo "${models}" | jq -r '.[]'); do
    echo "${element}"
    mv $element-service-stack/$element-stack.ts infrastructure/lib/$element-stack.ts
    rm -rf $element-service-stack
done

# generate project.ts file
python generate_infra_project_file.py $MODELS_FILE_NAME

# move project.ts file to infrastructure/lib/project.ts
mv project.ts infrastructure/bin/project.ts

# deploy the project

if [ "$DEPLOY" = true ] ; then
    # go to infrastructure
    cd infrastructure

    # install dependencies
    npm install

    # deploy
    cdk deploy --all --require-approval never
fi
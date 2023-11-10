import json
import sys

def getModels(fileName):
    with open(fileName, 'r') as f:
        return json.load(f)
    
def getDomainClassVariables(model):
    with open("domain/" + model + "_domain.json", 'r') as f:
        return json.load(f)


def generateBackendClassFile(models_class_files_dir, model):
    model_class_variables = getDomainClassVariables(model)
    model_class_name = model_class_variables["model_class_name"]
    pk_name = model_class_variables["model_partition_key"]
    columns = model_class_variables["columns"]

    content = f"""const {{ v4: uuidv4 }} = require('uuid');

    class {model_class_name} {{
        constructor({{ {', '.join(columns)} }}) {{
            this.createdAt = Date.now().toString();
    """

    for column in columns:
        content += f"       this.{column} = {column} || null;\n"

    content += f"""
            this.{pk_name} = uuidv4() + '_' + this.createdAt;
        }}

        toItem() {{
            return {{
                {pk_name}: this.{pk_name},
                createdAt: this.createdAt,
                {', '.join([f'{column}: this.{column}' for column in columns])},
            }};
        }}

        pk() {{
            return this.{pk_name};
        }}

        static sortKey(key) {{
            return key.split('_')[1];
        }}

        static getKeys(pk) {{
            return {{
                {pk_name}: pk,
                createdAt: {model_class_name}.sortKey(pk)
            }};
        }}
            
    }}

    module.exports = {model_class_name};
    """

    with open(f"{models_class_files_dir}/{model_class_name}.js", 'w') as f:
        f.write(content)

if __name__ == "__main__":
    models_class_files_dir = sys.argv[1]
    models_file_name = sys.argv[2]
    # check if extension is .json
    if models_file_name[-5:] != ".json":
        print("Error: models file must be a .json file")
        exit(1)
    models = getModels(models_file_name)
    for model in models:
        generateBackendClassFile(models_class_files_dir, model)
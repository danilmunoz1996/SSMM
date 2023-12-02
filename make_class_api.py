import sys
import json

# Plantilla para el servicio JS
template = """
import ApiService from "./ApiService";

const URL = import.meta.env.VITE_APP_-MODEL_CLASS_NAME-UPPER-_API_URL;
const MODEL = import.meta.env.VITE_APP_-MODEL_CLASS_NAME-UPPER-_API_MODEL;

class -MODEL_CLASS_NAME-CAPITALIZED-Service extends ApiService {
    constructor() {
        super(URL, MODEL);
    }

    async all() {
        const data = await this.getAll();

        return data;
    }

    async create(data) {
        const { ATTRIBUTES } = data;

        const model = await this.create({
            ATTRIBUTES
        });

        return model;
    }

    async get(id) {
        const data = await this.get(id);

        return data;
    }

    async update(id, data) {
        const { ATTRIBUTES } = data;

        const model = await this.update(id, {
            ATTRIBUTES
        });

        return model;
    }

    async remove(id) {
        const model = await this.remove(id);

        return model;
    }
}

export default -MODEL_CLASS_NAME-CAPITALIZED-Service;
"""

def getModels(fileName):
    with open(fileName, 'r') as f:
        return json.load(f)
    
def getDomainClassAttributes(model):
    with open("domain/" + model + "_domain.json", 'r') as f:
        return json.load(f)

def generate_service_file(dir, model_class_name):
    # REPLACE ALL OCURRENCES OF -MODEL_CLASS_NAME-
    service_template = template.replace('-MODEL_CLASS_NAME-UPPER-', model_class_name.upper())
    service_template = service_template.replace('-MODEL_CLASS_NAME-CAPITALIZED-', model_class_name.capitalize())
    model_attributes = getDomainClassAttributes(model_class_name)['columns']
    attributes_str = ', '.join(model_attributes)
    service_code = service_template.replace('ATTRIBUTES', attributes_str)
    with open(f"{dir}/{model_class_name.capitalize()}Service.js", 'w') as service_file:
        service_file.write(service_code)

if __name__ == "__main__":
    models_file_name = sys.argv[1]
    # check if extension is .json
    if models_file_name[-5:] != ".json":
        print("Error: models file must be a .json file")
        exit(1)
    models = getModels(models_file_name)
    for model in models:
        generate_service_file("services", model)

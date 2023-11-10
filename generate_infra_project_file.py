import json
import sys

def getModels(fileName):
    with open(f"{fileName}", 'r') as f:
        return json.load(f)
    
def getDomainClassVariables(model):
    with open("domain/" + model + "_domain.json", 'r') as f:
        return json.load(f)
    

def generate_project_file(models):

    inicio = '''#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';\n'''
    fin = '''
const app = new cdk.App();\n'''

    importaciones = ''
    instancias = ''

    for model in models:
        model_class_variables = getDomainClassVariables(model)
        model_class_name = model_class_variables["model_class_name"]
        model_name = model_class_variables["model_name"]
        importaciones += "import { "+ model_class_name + "Stack" +" } from '../lib/"+ model_name +"-stack';\n"
        instancias += f'new {model_class_name}Stack(app, \'{model_class_name}Stack\', {{}});\n'
    
    return inicio + importaciones + fin + instancias



if __name__ == "__main__":
    models_file_name = sys.argv[1]
    models = getModels(models_file_name)
    code = generate_project_file(models)
    with open('project.ts', 'w') as f:
        f.write(code)


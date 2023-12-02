import sys
import json


def write_domain_class_variables(model, columns, indexes=[]):
    class_variables = {
        "project_name": model + "-service",
        "model_class_name": model.capitalize(),
        "model_name": model,
        "model_partition_key": model + "Id",
        "columns": columns,
        "indexes": indexes,
    }
    with open("domain/" + model + "_domain.json", 'w') as f:
        print("Writing domain/" + model + "_domain.json")
        json.dump(class_variables, f)

def getColumnsFromUser(model):
    columns = ['createdBy', 'updatedAt', 'updatedBy', 'deletedAt', 'deletedBy']
    while True:
        column = input("Agrega una columna para "+ model +"(ingresa 'OK' para terminar): ")
        if column == "OK":
            break
        columns.append(column)
    return columns

def getIndexesFromUser(model):
    indexes = []
    while True:
        index = input("Agrega un indice para "+ model +"(ingresa 'OK' para terminar): ")
        if index == "OK":
            break
        indexes.append(index)
    return indexes

def getModelsFromUser():
    models = []
    while True:
        model = input("Agrega un modelo (ingresa 'OK' para terminar): ")
        if model == "OK":
            break
        models.append(model)
    return models

if __name__ == "__main__":
    models_file_name = sys.argv[1]
    # check if extension is .json
    if models_file_name[-5:] != ".json":
        print("Error: models file must be a .json file")
        exit(1)

    models = getModelsFromUser()
    for model in models:
        print("Modelo: " + model)
        columns = getColumnsFromUser(model)
        indexes = getIndexesFromUser(model)
        write_domain_class_variables(model, columns, indexes)

    # write models to models.json
    with open(models_file_name, 'w') as f:
        json.dump(models, f)


    
import sys
import json

# Plantilla para el archivo de stack CDK
cdk_template_with_indexes = """
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { aws_dynamodb as dynamodb } from 'aws-cdk-lib';

const model_lower = '{model_lower}';
const model = '{model_capitalized}'

const TABLE_NAME = model;
const TABLE_PK = model_lower + 'Id';
const TABLE_SK = 'createdAt';

export class {model_capitalized}Stack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // model's table
    const table = new dynamodb.Table(this, TABLE_NAME, {
      partitionKey: { name: TABLE_PK, type: dynamodb.AttributeType.STRING },
      sortKey: { name: TABLE_SK, type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    // generate exports names for table
  
    new cdk.CfnOutput(this, model + 'TableName', {
      value: table.tableName,
      exportName: model + 'TableName'
    });

    new cdk.CfnOutput(this, model + 'TableArn', {
      value: table.tableArn,
      exportName: model + 'TableArn'
    });

    {indices_code}
  }
}
"""

cdk_template = """
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { aws_dynamodb as dynamodb } from 'aws-cdk-lib';

const model_lower = '{model_lower}';
const model = '{model_capitalized}'

const TABLE_NAME = model;
const TABLE_PK = model_lower + 'Id';
const TABLE_SK = 'createdAt';

export class {model_capitalized}Stack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // model's table
    const table = new dynamodb.Table(this, TABLE_NAME, {
      partitionKey: { name: TABLE_PK, type: dynamodb.AttributeType.STRING },
      sortKey: { name: TABLE_SK, type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    // generate exports names for table
  
    new cdk.CfnOutput(this, model + 'TableName', {
      value: table.tableName,
      exportName: model + 'TableName'
    });

    new cdk.CfnOutput(this, model + 'TableArn', {
      value: table.tableArn,
      exportName: model + 'TableArn'
    });
  }
}
"""

# Función para generar código de índices
def generate_indices_code(indices):
    code = ""
    for index in indices:
        code += f"""
    // Create a {index} GSI for the table
    const {index}IndexName = '{index}';
    table.addGlobalSecondaryIndex({{
      indexName: {index}IndexName,
      partitionKey: {{ name: '{index}', type: dynamodb.AttributeType.STRING }},
    }});

    // generate exports names for GSI
    new cdk.CfnOutput(this, model + '{index}IndexArn', {{
      value: table.tableArn + '/index/' + {index}IndexName,
      exportName: model + '{index}IndexArn'
    }});
    """
    return code

def getModels(fileName):
    with open(fileName, 'r') as f:
        return json.load(f)
    
def getDomainClassVariables(model):
    with open("domain/" + model + "_domain.json", 'r') as f:
        return json.load(f)

def generate_cdk_file(model_name):
    model_lower = model_name.lower()
    model_capitalized = model_name.capitalize()
    cdk_code = cdk_template.replace('{model_lower}', model_lower).replace('{model_capitalized}', model_capitalized)
    file_name = model_name + '-stack.ts'
    with open(file_name, 'w') as file:
        file.write(cdk_code)

def generate_cdk_file_with_indexes(model_name, indices):
    model_lower = model_name.lower()
    model_capitalized = model_name.capitalize()
    indices_code = generate_indices_code(indices)
    cdk_code = cdk_template_with_indexes.replace('{model_lower}', model_lower).replace('{model_capitalized}', model_capitalized).replace('{indices_code}', indices_code)
    file_name = model_name + '-stack.ts'
    with open(file_name, 'w') as file:
        file.write(cdk_code)

if __name__ == "__main__":
    models_file_name = sys.argv[1]
    models_data = getModels(models_file_name)
    for model in models_data:
        indices = getDomainClassVariables(model)['indexes']
        if len(indices) == 0:
            generate_cdk_file(model)
        else:
            generate_cdk_file_with_indexes(model, indices)

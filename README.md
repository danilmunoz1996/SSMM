# SSMM
Simple Serverless Microservice Maker


## Prerequisites
- [Node.js](https://nodejs.org/en/) (v18.15.0 or higher)
- [Serverless Framework](https://www.npmjs.com/package/serverless) (v3.38.0 or higher)
- [AWS CLI](https://aws.amazon.com/cli/) (v2.2.47 or higher)
- [CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html) (v2.83 or higher)

## How to use
1. Clone this repo

2. run shell script
```bash
$ sh run.sh [dir_to_save_models] [file_to_save_models] [want_to_deploy]
```

## Example
```bash
$ sh run.sh MODELS_CLASSES models.json true
```
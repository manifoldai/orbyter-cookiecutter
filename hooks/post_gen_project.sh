#! /bin/bash
# This script performs all of the optional operations dependent on provided details such as API keys.

function jsonValue() {
KEY=$1
num=$2
awk -F"[,:}]" '{for(i=1;i<=NF;i++){if($i~/'$KEY'\042/){print $(i+1)}}}' | tr -d '"' | sed -n ${num}p
}


# Environment
FILE=.env
echo "Building env file ${FILE}"
echo "" >> $FILE
echo "# Environment variables to be read by dockers containers. Do not use quotes" >> $FILE
# mlflow
echo "MLFLOW_TRACKING_URI={{ cookiecutter.mlflow_uri }}" >> $FILE
echo "MLFLOW_ARTIFACT_LOCATION={{ cookiecutter.mlflow_artifact }}" >> $FILE

FILE=env_template
echo "Building env file ${FILE}"
echo "# DO NOT PUT SECRETS IN THIS FILE" >> $FILE
echo "" >> $FILE
echo "# Environment variables to be read by dockers containers. Do not use quotes" >> $FILE
# mlflow
echo "MLFLOW_TRACKING_URI={{ cookiecutter.mlflow_uri }}" >> $FILE
echo "MLFLOW_ARTIFACT_LOCATION={{ cookiecutter.mlflow_artifact }}" >> $FILE

# Push scaffolded repo to GitHub
echo "Making initial commit"
git init
git add .
git commit -m "Scaffold repo"

echo "All set! Run 'make dev-start' to spin up your containers."

#/bin/bash
#
# autoformat.sh
# 
# Runs all autoformaters
# Run this from CI job docker container
set -ex

echo 'Running isort'
isort -rc /mnt/{{ cookiecutter.repo_name.replace("-", "_") }}

echo 'Running black'
black /mnt/{{ cookiecutter.repo_name.replace("-", "_") }}

echo 'Finished auto formatting'

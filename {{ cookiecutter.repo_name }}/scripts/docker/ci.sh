#/bin/bash
# 
# Local tests of CI jobs
# Run this from CI job docker container
set -ex

echo 'Running black'
black --check /mnt/{{ cookiecutter.repo_name }}

echo 'Running flake'
flake8 /mnt/{{ cookiecutter.repo_name }}

echo 'Running pytest'
pytest /mnt/{{ cookiecutter.repo_name }}

echo 'Finished tests'

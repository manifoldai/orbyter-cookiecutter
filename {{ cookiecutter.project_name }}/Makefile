.PHONY: help, ci-black, ci-flake8, ci-test, isort, black, docs, dev-start, dev-stop

## Ensure this is the same name as in docker-compose.yml file
CONTAINER_NAME="{{ cookiecutter.package_name }}_jupyter_${USER}"

PROJECT={{ cookiecutter.package_name }}

PROJ_DIR="/mnt/{{ cookiecutter.package_name }}"
VERSION_FILE:=VERSION
COMPOSE_FILE=docker/docker-compose.yml
TAG:=$(shell cat ${VERSION_FILE})

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

git-tag:  ## Tag in git, then push tag up to origin
	git tag $(TAG)
	git push origin $(TAG)

## Test lint compliance using black. Config in pyproject.toml file
ci-black: dev-start
	docker exec -t $(CONTAINER_NAME) black --check $(PROJ_DIR)

## Test lint compliance using flake8. Config in tox.ini file
ci-flake8: dev-start
	docker exec -t $(CONTAINER_NAME) flake8 $(PROJ_DIR)

## Runs unit tests using pytest
ci-test: dev-start
	docker exec -t $(CONTAINER_NAME) pytest $(PROJ_DIR)

## Runs unit tests, with an interactive IPDB session at the first failure
ci-test-interactive: dev-start
	docker exec -it $(CONTAINER_NAME) pytest $(PROJ_DIR)  -x --pdb --pdbcls=IPython.terminal.debugger:Pdb

## Runs mypy type checker
ci-mypy: dev-start
	docker exec -t $(CONTAINER_NAME) mypy --ignore-missing-imports --show-error-codes $(PROJ_DIR)

## Check black, flake8, and run unit tests
ci: ci-black ci-flake8 ci-test ci-mypy
	@echo "CI successful"

## Runs isort to sorts imports
isort: dev-start
	docker exec -t $(CONTAINER_NAME) isort -rc $(PROJ_DIR)  --profile black

## Runs black auto-linter
black: dev-start
	docker exec -t $(CONTAINER_NAME) black $(PROJ_DIR)

## Formats repo; runs black and isort on all files
format: isort black
	@echo "Formatting complete"

## Deprecated. Here to support old workflow
lint: format

## Primary make command for devs, spins up containers
dev-start:
	docker-compose -f $(COMPOSE_FILE) --project-name $(PROJECT) up -d --no-recreate

## Spin down active containers
dev-stop:
	docker-compose -f $(COMPOSE_FILE) --project-name $(PROJECT) down

## Rebuild images for dev containers (useful when Dockerfile/requirements are updated)
dev-rebuild:
	docker-compose -f $(COMPOSE_FILE) --project-name $(PROJECT) up -d --build

## Exec into docker bash terminal
bash: dev-start
	docker exec -it $(CONTAINER_NAME) bash

## Build docs using Sphinx and copy to docs folder (this makes it easy to publish to gh-pages)
docs:
	docker exec -e GRANT_SUDO=yes $(CONTAINER_NAME) bash -c "cd docsrc; make html"
	@cp -a docsrc/_build/html/. docs

## Provides an interactive ipython prompt
ipython:
	docker exec -it $(CONTAINER_NAME) ipython

## Clean out temp/compiled python files
clean:
	find . -name __pycache__ -delete
	find . -name "*.pyc" -delete

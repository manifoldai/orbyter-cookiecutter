.PHONY: help, ci-black, ci-flake8, ci-test, isort, black, docs, dev-start, dev-stop

## Ensure this is the same name as in docker-compose.yml file
CONTAINER_NAME="{{ cookiecutter.package_name }}_develop_${USER}"

PROJECT={{ cookiecutter.package_name }}

PROJ_DIR="/mnt/{{ cookiecutter.package_name }}"
VERSION_FILE:=VERSION
COMPOSE_FILE=docker/docker-compose.yml
TAG:=$(shell cat ${VERSION_FILE})

# takes advantage of the makefile structure (command; ## documentation)
# to generate help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

git-tag:  ## Tag in git, then push tag up to origin
	git tag $(TAG)
	git push origin $(TAG)


ci-black: dev-start ## Test lint compliance using black. Config in pyproject.toml file
	docker exec -t $(CONTAINER_NAME) black --check $(PROJ_DIR)


ci-flake8: dev-start ## Test lint compliance using flake8. Config in tox.ini file
	docker exec -t $(CONTAINER_NAME) flake8 $(PROJ_DIR)


ci-test: dev-start ## Runs unit tests using pytest
	docker exec -t $(CONTAINER_NAME) pytest $(PROJ_DIR)


ci-test-interactive: dev-start ## Runs unit tests with interactive IPDB session at the first failure
	docker exec -it $(CONTAINER_NAME) pytest $(PROJ_DIR)  -x --pdb --pdbcls=IPython.terminal.debugger:Pdb


ci-mypy: dev-start ## Runs mypy type checker
	docker exec -t $(CONTAINER_NAME) mypy --ignore-missing-imports --show-error-codes $(PROJ_DIR)


ci: ci-black ci-flake8 ci-test ci-mypy ## Check black, flake8, and run unit tests
	@echo "CI successful"


isort: dev-start ## Runs isort to sorts imports
	docker exec -t $(CONTAINER_NAME) isort -rc $(PROJ_DIR)  --profile black


black: dev-start ## Runs black auto-linter
	docker exec -t $(CONTAINER_NAME) black $(PROJ_DIR)


format: isort black ## Formats repo by running black and isort on all files
	@echo "Formatting complete"


lint: format ## Deprecated. Here to support old workflow


.env: ## make an .env file
	touch .env

dev-start: .env ## Primary make command for devs, spins up containers
	docker-compose -f $(COMPOSE_FILE) --project-name $(PROJECT) up -d --no-recreate


dev-stop: ## Spin down active containers
	docker-compose -f $(COMPOSE_FILE) --project-name $(PROJECT) down

nb: ## Opens Jupyterlab in the browser
	docker port $(CONTAINER_NAME) | grep 8888 | awk -F ":" '{print "http://localhost:"$$2}' | xargs open

# Useful when Dockerfile/requirements are updated)
dev-rebuild: .env ## Rebuild images for dev containers
	docker-compose -f $(COMPOSE_FILE) --project-name $(PROJECT) up -d --build

bash: dev-start ## Provides an interactive bash shell in the container
	docker exec -it $(CONTAINER_NAME) bash


dvc-init: dev-start ## initialize DVC
	docker exec -it $(CONTAINER_NAME) dvc init

# makes it easy to publish to gh-pages
docs: dev-start ## Build docs using Sphinx and copy to docs folder
	docker exec -e GRANT_SUDO=yes $(CONTAINER_NAME) bash -c "cd docsrc; make html"
	@cp -a docsrc/_build/html/. docs
	@echo "Documentation copied to ./docs. Open ./docs/index.html and take a look."


ipython: dev-start ## Provides an interactive ipython prompt
	docker exec -it $(CONTAINER_NAME) ipython


clean: ## Clean out temp/compiled python files
	find . -name __pycache__ -delete
	find . -name "*.pyc" -delete
